from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.product.models import Product
from src.inventory.schemas import InventoryReadSchema
from src.inventory.exceptions import InventoryNotFound

class InventoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_inventory_by_sku_with_relationships(self, sku):
        """
        Get product with inventory details by SKU.
        """
        try:
            query = (
                select(Product)
                .options(selectinload(Product.inventory))
                .where(Product.sku == sku)
            )
            result = await self.db.execute(query)
            product = result.scalars().first()
            return product
        except Exception as e:
            raise ValueError({
                "message": "Error retrieving inventory by SKU",
                "error": str(e),
                "method": "InventoryService.get_inventory_by_sku_with_relationships",
            })

    async def get_inventory_by_sku(self, sku: str):
        """
        Get inventory details by SKU.
        """
        try:
            product = await self.get_inventory_by_sku_with_relationships(sku)

            if not product:
                raise InventoryNotFound(f"Product with SKU '{sku}' not found.")
            if not product.inventory:
                raise InventoryNotFound(f"No inventory found for product '{sku}'.")

            return {
                "sku": product.sku,
                "product_name": product.name,
                "available_quantity": product.inventory.available_quantity,
                "reserved_quantity": product.inventory.reserved_quantity,
            }
        except InventoryNotFound:
            raise 
        except Exception as e:
            raise ValueError({
                "message": "Failed to fetch inventory",
                "sku": sku,
                "error": str(e),
                "method": "InventoryService.get_inventory_by_sku"
            })
    


