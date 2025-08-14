from fastapi import APIRouter
from src.order import routers as order_routers
from src.health import routers as health_routers
from src.product import routers as product_routers
from src.inventory import routers as inventory_routers

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(order_routers.router)
main_router.include_router(health_routers.router)
main_router.include_router(product_routers.router)
main_router.include_router(inventory_routers.router)
