from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Product
from .schemas import ProductCreate

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()

async def create_product(db: AsyncSession, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalars().first()

async def update_product(db: AsyncSession, product_id: int, product: ProductCreate):
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalars().first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        await db.commit()
        await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalars().first()
    if db_product:
        await db.delete(db_product)
        await db.commit()
    return db_product
