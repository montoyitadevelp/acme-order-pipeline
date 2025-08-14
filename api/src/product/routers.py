from fastapi import APIRouter, Depends, Query, status, HTTPException
from fastapi_pagination import Page
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Params
from src.product.services import ProductService
from src.config.database import get_db
from src.product.schemas import ProductSearchSchema

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=ProductSearchSchema, status_code=status.HTTP_200_OK)
async def get_products(
    sku: str | None = Query(None, description="Filter products by SKU"),
    params: Params = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all products with optional SKU filter and pagination
    """
    try:
        service = ProductService(db)
        result = await service.get_search_products(sku, params)
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
