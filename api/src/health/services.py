from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.order.event.producer import KafkaProducer

class HealthService:
    def __init__(self, db: AsyncSession, mongo_db, kafka_producer: KafkaProducer):
        self.db = db
        self.mongo_db = mongo_db
        self.kafka_producer = kafka_producer

    async def check_pg(self) -> bool:
        try:
            await self.db.execute(select(1))
            return True
        except Exception:
            return False

    async def check_mongo(self) -> bool:
        try:
            await self.mongo_db.list_collection_names()
            return True
        except Exception:
            return False


    async def get_health_status(self, check_sql=True, check_mongo=True, check_kafka=True) -> dict:
        status = "healthy"

        if check_sql and not await self.check_pg():
            status = "sql_unhealthy"
        elif check_mongo and not await self.check_mongo():
            status = "mongo_unhealthy"
        elif await self.kafka_producer.is_healthy():
            status = "kafka_unhealthy"

        return {
            "status": status,
            "timestamp": datetime.now().isoformat() + "Z"
        }
