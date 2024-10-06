from fastapi import FastAPI, HTTPException, Depends
from schemas import OrderCreate, ProductCreate

import database


app = FastAPI()



# эндпоинты для products
@app.post('/products/')
async def create_product(product:ProductCreate):
    await database.create_product(product)


@app.get('/products/')
async def get_products():
    products = await database.get_products()
    return products