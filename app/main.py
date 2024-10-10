from typing import List

from fastapi import FastAPI, HTTPException, Depends, status
from schemas import OrderCreate, ProductCreate, OrderItemCreate, OrderStatus

import database
from database import OrderFactory

app = FastAPI()



# эндпоинты для products
@app.post('/products')
async def create_product(product: ProductCreate):
    await database.create_product_db(product)


@app.get('/products')
async def get_products():
    products = await database.get_products_db()
    return products

@app.get('/products/{id}')
async def get_product_description(id: int):
    description = await database.get_product_description_db(id)
    return description

@app.put('/products/{id}')
async def update_product_description(id: int, new_description: str):
    updated = await database.update_product_discription_db(id, new_description)
    print(f'this is description: {new_description}')
    print(f'this is update: {updated}')
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    return {'message': 'Description updated successfully'}


@app.delete('/products/{id}')
async def delete_product(id: int):
    await database.delete_product_db(id)


# эндпоинты для orders
@app.post('/orders')
async def create_order(items_data: List[OrderItemCreate]):
    await OrderFactory.create_order(items_data)


@app.get('/orders')
async def get_orders():
    orders = await database.get_orders_db()
    return orders


@app.get('/orders/{id}')
async def get_order_by_id(id: int):
    order = await database.get_order_by_id_db(id)
    return order

@app.patch('/orders/{id}/status')
async def order_status_refresh(id: int, new_status: OrderStatus):
    await database.order_status_refresh_db(id, new_status)
