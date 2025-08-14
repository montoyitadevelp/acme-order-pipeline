
from typing import AsyncGenerator
from src.order.event.producer import KafkaProducer
from src.config.settings import settings as s
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


async def get_kafka_producer() -> AsyncGenerator[KafkaProducer, None]:
    producer = KafkaProducer()
    try:
        await producer.start()
        yield producer
    finally:
        await producer.stop()
# MongoDB setup
mongo_client = AsyncIOMotorClient(s.MONGO_URI)
mongo_db = mongo_client[s.MONGO_INITDB_DATABASE]

async def get_mongo_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """
    Yields an AsyncIOMotorDatabase object for direct collection access.
    """
    yield mongo_db