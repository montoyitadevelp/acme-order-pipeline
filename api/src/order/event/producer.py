import uuid
import datetime
import asyncio
from typing import Optional, Set
from aiokafka import AIOKafkaProducer
from google.protobuf.timestamp_pb2 import Timestamp
from src.config.settings import settings as s
from src.order.proto import order_events_pb2


class KafkaProducer:
    def __init__(self):
        self._producer: Optional[AIOKafkaProducer] = None
        self._bootstrap_servers = s.KAFKA_BOOTSTRAP_SERVERS
        self._started = False
        self._lock = asyncio.Lock()  # Prevent concurrent starts
        self._pending_tasks: Set[asyncio.Task] = set()  # Track background tasks

    async def start(self):
        """Start Kafka producer with retry and lock"""
        async with self._lock:
            if self._started and self._producer:
                return
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    if self._producer:
                        try:
                            await self._producer.stop()
                        except Exception:
                            pass
                        self._producer = None
                    self._producer = AIOKafkaProducer(
                        bootstrap_servers=self._bootstrap_servers,
                        retry_backoff_ms=300,
                        request_timeout_ms=10000,
                        enable_idempotence=True,
                    )
                    await self._producer.start()
                    self._started = True
                    return
                except Exception as e:
                    self._producer = None
                    self._started = False
                    if attempt == max_retries - 1:
                        raise Exception(f"Failed to start Kafka producer after {max_retries} attempts: {e}")
                    await asyncio.sleep(2 ** attempt)

    async def stop(self):
        """Stop Kafka producer safely after all tasks complete"""
        if self._producer and self._started:
            # Wait for pending tasks
            if self._pending_tasks:
                await asyncio.wait(self._pending_tasks, return_when=asyncio.ALL_COMPLETED)
            try:
                await self._producer.stop()
            finally:
                self._started = False
                self._producer = None

    async def is_healthy(self) -> bool:
        return self._started

    async def publish_order_created(self, order_id: str, customer: dict, items: list, background: bool = True):
        """Publish order created event, optionally in background"""
        if not await self.is_healthy():
            await self.start()
        if not await self.is_healthy():
            raise ValueError({
                "message": "Kafka producer is not available",
                "method": "KafkaProducer.publish_order_created"
            })

        async def _send():
            try:
                event = order_events_pb2.OrderEvent()
                event.event_id = str(uuid.uuid4())
                event.order_id = order_id
                event.event_type = order_events_pb2.ORDER_CREATED
                ts = Timestamp()
                ts.FromDatetime(datetime.datetime.utcnow())
                event.timestamp.CopyFrom(ts)

                oc = order_events_pb2.OrderCreated()
                oc.order_id = order_id
                oc.customer.user_id = customer["user_id"]
                oc.customer.email = customer["email"]

                for item in items:
                    oi = order_events_pb2.OrderItem()
                    oi.sku = item["sku"]
                    oi.quantity = item["quantity"]
                    oc.items.append(oi)

                event.order_created.CopyFrom(oc)
          
            except Exception as e:
                # Log properly
                print(f"Failed to publish order {order_id} event: {e}")

        if background:
            task = asyncio.create_task(_send())
            self._pending_tasks.add(task)
            task.add_done_callback(lambda t: self._pending_tasks.discard(t))
            return task
        else:
            await _send()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()
