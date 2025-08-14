from fastapi import APIRouter, Depends, status, HTTPException
from datetime import datetime
from src.config.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.order.dependencies import get_mongo_db
from src.order.event.producer import KafkaProducer
from sqlalchemy import select
from src.health.services import HealthService
from src.health.schemas import HealthCheckSchema

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=HealthCheckSchema)
async def health_check(
    db: AsyncSession = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    kafka_producer: KafkaProducer = Depends()
):
    """
    Health check endpoint.
    """
    try:
        service = HealthService(db=db, mongo_db=mongo_db, kafka_producer=kafka_producer)
        result = await service.get_health_status()
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
