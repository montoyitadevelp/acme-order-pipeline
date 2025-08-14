import datetime
import asyncio
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.product.models import Product
from src.order.exceptions import OrderInventoryError, OrderProductNotFound, OrderNotFound
from src.order.constants import TAX_RATE
from src.utils.general import generate_short_uuid
from src.order.event.producer import KafkaProducer
from fastapi_pagination import Params
from fastapi_pagination.ext.motor import apaginate
from src.inventory.models import Inventory


class OrderService:
    def __init__(self, db: AsyncSession, mongo_db, kafka_producer: KafkaProducer):
        self.db = db
        self.mongo_db = mongo_db
        self.producer = kafka_producer

    async def get_orders_by_user(self, user_id: str, params: Params = Params()):
        """
        Retrieve paginated orders for a specific user.
        Returns simplified structure with order_id, status, total, created_at
        """
        try:
            query_filter = {"customer.user_id": user_id}
            paginated = await apaginate(
                self.mongo_db.orders,
                query_filter,
                params=params,
                sort=[("created_at", -1)]
            )
            paginated.items = [
                {
                    "order_id": o.get("order_id"),
                    "status": o.get("status"),
                    "total": float(o.get("pricing", {}).get("total", 0)),
                    "created_at": o.get("created_at").isoformat()
                }
                for o in paginated.items
            ]
            return paginated
        except Exception as e:
            raise ValueError({
                "message": "Failed to fetch user orders",
                "user_id": user_id,
                "error": str(e)
            })

    async def get_order_by_id(self, order_id: str):
        """Retrieve an order by its ID."""
        order_doc = await self.mongo_db.orders.find_one({"order_id": order_id})
        if not order_doc:
            raise OrderNotFound(f"Order with ID '{order_id}' not found.")
        return order_doc

    async def _fetch_product_and_inventory(self, sku: str):
        """
        Fetch product and its inventory details by SKU.
        """
        try:
            result = await self.db.execute(
                select(Product)
                .options(selectinload(Product.inventory))
                .where(Product.sku == sku)
            )
            product = result.scalars().first()
            if not product:
                raise OrderProductNotFound(f"Product with SKU '{sku}' not found.")
            if not product.inventory:
                raise OrderInventoryError(f"Inventory for SKU '{sku}' not found.")
            return product, product.inventory
        except (OrderProductNotFound, OrderInventoryError):
            raise
        except Exception as e:
            raise ValueError({
                "message": "Failed to fetch product and inventory",
                "method": "OrderService._fetch_product_and_inventory",
                "error": str(e)
            })

    async def create_order(self, customer: dict, items: list[dict]):
        """
        Create a new order.
        """
        order_id = f"ORD-{generate_short_uuid()}"
        subtotal = Decimal("0")
        reserved_items = []

        try:
            for item in items:
                product, inventory = await self._fetch_product_and_inventory(item["sku"])

                max_purchasable = inventory.available_quantity - inventory.reserved_quantity
                if item["quantity"] > max_purchasable:
                    raise OrderInventoryError(
                        f"Insufficient inventory for {item['sku']}. "
                        f"Requested: {item['quantity']}, "
                        f"Available: {inventory.available_quantity}, "
                    )

                inventory.available_quantity -= item["quantity"]
                inventory.reserved_quantity += item["quantity"]
                self.db.add(inventory)

                reserved_items.append({
                    "sku": item["sku"],
                    "quantity": item["quantity"],
                    "price": float(product.price)
                })
                subtotal += Decimal(str(product.price)) * Decimal(str(item["quantity"]))
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e

        tax = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
        total = (subtotal + tax).quantize(Decimal("0.01"))

        order_doc = {
            "order_id": order_id,
            "status": "pending",
            "customer": customer,
            "items": reserved_items,
            "pricing": {"subtotal": float(subtotal), "tax": float(tax), "total": float(total)},
            "payment": {"status": "pending", "transaction_id": generate_short_uuid()},
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
        }
        try:
            await self.mongo_db.orders.insert_one(order_doc)
        except Exception as e:
            await self._release_reserved_inventory(reserved_items)
            raise Exception(f"Order persistence failed: {str(e)}")

        asyncio.create_task(
            self._process_payment_and_publish(order_id, reserved_items, total, customer)
        )

        return {
            "order_id": order_id,
            "status": "pending",
            "estimated_total": float(total),
            "created_at": datetime.datetime.now().isoformat(),
            "message": "Order created successfully and is pending processing"
        }

    async def _process_payment_and_publish(self, order_id, reserved_items, total, customer):
        """Background task to handle payment and Kafka publishing"""
        try:
            payment_success = await self._simulate_payment()

            if payment_success:
                await self.mongo_db.orders.update_one(
                    {"order_id": order_id},
                    {"$set": {"status": "processing", "payment.status": "completed", "updated_at": datetime.datetime.now()}}
                )
            else:
                await self.mongo_db.orders.update_one(
                    {"order_id": order_id},
                    {"$set": {"status": "cancelled", "payment.status": "failed", "updated_at": datetime.datetime.now()}}
                )
                await self._release_reserved_inventory(reserved_items)
                return

            # Publish event asynchronously
            try:
                await self.producer.publish_order_created(order_id, customer, reserved_items)
                final_status = "confirmed"
            except Exception:
                final_status = "processing"

            # Update final status
            await self.mongo_db.orders.update_one(
                {"order_id": order_id},
                {"$set": {"status": final_status, "updated_at": datetime.datetime.now()}}
            )

        except Exception:
            await self.mongo_db.orders.update_one(
                {"order_id": order_id},
                {"$set": {"status": "error", "updated_at": datetime.datetime.now()}}
            )
            await self._release_reserved_inventory(reserved_items)

    async def _release_reserved_inventory(self, reserved_items: list[dict]):
        """Release reserved inventory in case of failure"""
        for item in reserved_items:
            product, inventory = await self._fetch_product_and_inventory(item["sku"])
            inventory.available_quantity += item["quantity"]
            inventory.reserved_quantity -= item["quantity"]
            self.db.add(inventory)
        await self.db.commit()

    async def _simulate_payment(self) -> bool:
        import random
        await asyncio.sleep(1)  # Simulate payment
        return random.random() > 0.55
