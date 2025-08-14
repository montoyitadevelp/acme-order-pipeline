from aiokafka import AIOKafkaConsumer
from src.order.proto import order_events_pb2
from src.order.constants import KAFKA_TOPIC

class KafkaWorker:
    def __init__(self, mongo_db, pg_sessionmaker, kafka_producer):
        self.mongo_db = mongo_db
        self.pg_sessionmaker = pg_sessionmaker
        self.producer = kafka_producer
        self.consumer = AIOKafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=self.producer._bootstrap_servers,
            group_id="order_processors"
        )

    async def start(self):
        await self.consumer.start()
        await self.producer.start()
        try:
            async for msg in self.consumer:
                if msg.value is not None: 
                    await self.handle_message(msg.value)
        finally:
            await self.consumer.stop()
            await self.producer.stop()

    async def handle_message(self, payload: bytes):
        event = order_events_pb2.OrderEvent()
        event.ParseFromString(payload)

        # Idempotency check
        processed = await self.mongo_db.processed_events.find_one({"event_id": event.event_id})

        if processed:
            return

        if event.event_type == order_events_pb2.ORDER_CREATED:
            async with self.pg_sessionmaker() as session:
                from src.order.services import OrderService
                service = OrderService(session, self.mongo_db, self.producer)
                await service.create_order(
                    {"user_id": event.order_created.customer.user_id,
                     "email": event.order_created.customer.email},
                    [{"sku": it.sku, "quantity": it.quantity} for it in event.order_created.items]
                )
