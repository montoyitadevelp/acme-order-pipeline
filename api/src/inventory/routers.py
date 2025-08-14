from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.database import get_db
from src.inventory.services import InventoryService
from src.inventory.schemas import InventoryReadSchema
from src.inventory.exceptions import InventoryNotFound

router = APIRouter(prefix="/products", tags=["Inventory"])

@router.get("/{sku}/inventory", response_model=InventoryReadSchema, status_code=status.HTTP_200_OK)
async def get_product_inventory(
    sku: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve inventory for a specific product by SKU.
    """
    try:
        service = InventoryService(db)
        inventory = await service.get_inventory_by_sku(sku)
        return inventory
    except InventoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
