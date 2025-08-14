from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate 
from fastapi_pagination import Params
from src.product.models import Product
from sqlalchemy.orm import selectinload




class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_product_by_sku(self, sku: str | None):
        try:
            query = select(Product).options(selectinload(Product.inventory)).where(Product.sku == sku) 
            return query
        except Exception as e:
            raise ValueError({
                "message": "Error retrieving product by SKU",
                "error": str(e),
                "method": "ProductService.get_product_by_sku",
            })

    async def get_all_products_with_relationships(self):
        """
            Retrieve all products.
        """
        try:
            query = select(Product).options(selectinload(Product.inventory))
            return query
        except Exception as e:
            raise ValueError({
                "message": "Error retrieving all products",
                "error": str(e),
                "method": "ProductService.get_all_products",
            })

    async def get_search_products(self, sku: str | None, params: Params):
        """
        Retrieve products by SKU.
        """
        try:
            product = await self.get_all_products_with_relationships()
            if sku:
                product = await self.get_product_by_sku(sku)
            paginate_query = await paginate(conn=self.db, query=product, params=params)
            for i in paginate_query.items:
                i.available_quantity = i.inventory.available_quantity if i.inventory else 0
            return paginate_query
        except Exception as e:
            raise ValueError({
                "message": "Error retrieving search products",
                "error": str(e),
                "method": "ProductService.get_search_products",
            })
            
            

