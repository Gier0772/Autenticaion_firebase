from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, models, schemas
from .database import Base, engine, get_db

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/products/", response_model=list[schemas.Product])
async def read_products(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    products = await crud.get_products(db, skip=skip, limit=limit)
    return products

@app.post("/products/", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_product(db=db, product=product)

@app.get("/products/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(product_id: int, product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    db_product = await crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", response_model=schemas.Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    db_product = await crud.delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

