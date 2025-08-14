from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from src.order.schemas import OrderCreateSchema, OrderReadSchema, OrderReadByIdSchema, OrdersUserSearchSchema
from src.order.services import OrderService
from src.order.dependencies import get_mongo_db, get_kafka_producer
from src.order.exceptions import OrderInventoryError, OrderProductNotFound, OrderNotFound
from src.config.database import get_db
from fastapi_pagination import  Params

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderReadSchema)
async def create_order(
    order: OrderCreateSchema = Body(),
    db: AsyncSession = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    kafka_producer=Depends(get_kafka_producer)
):
    """
    1. Validate inventory & reserve
    2. Publish Kafka event
    3. Payment + Mongo persistence handled asynchronously by KafkaWorker
    """
    try:
        service = OrderService(db, mongo_db, kafka_producer)
        customer_dict = order.customer.model_dump()  
        items_dicts = [item.model_dump() for item in order.items]
        result = await service.create_order(customer_dict, items_dicts)
        return result
    except OrderProductNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except OrderInventoryError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderReadByIdSchema)
async def get_order_by_id(
    order_id: str,
    db: AsyncSession = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    kafka_producer=Depends(get_kafka_producer)
):
    """
    Retrieve an order by ID with its products and customer details.
    """
    try:
        service = OrderService(db, mongo_db, kafka_producer)
        result = await service.get_order_by_id(order_id)
        return result
    except OrderNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{user_id}/orders", status_code=status.HTTP_200_OK, response_model=OrdersUserSearchSchema)
async def get_user_orders(
    user_id: str,
    params: Params = Depends(),
    db: AsyncSession = Depends(get_db),
    mongo_db=Depends(get_mongo_db),
    kafka_producer=Depends(get_kafka_producer)
):
    """
    Retrieve all orders for a specific user.
    """
    try:
        service = OrderService(db, mongo_db, kafka_producer)
        return await service.get_orders_by_user(user_id, params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
