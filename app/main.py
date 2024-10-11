from typing import List

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProductCreate, OrderItemCreate, OrderStatus
import app.database as database
from app.database import OrderFactory

app = FastAPI()


# эндпоинты для products
@app.post('/products')
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(database.get_session)
):
    await database.create_product_db(session, product)


@app.get('/products')
async def get_products(session: AsyncSession = Depends(database.get_session)):
    products = await database.get_products_db(session)
    return products


@app.get('/products/{id}')
async def get_product_description(
    id: int,
    session: AsyncSession = Depends(database.get_session)
):
    description = await database.get_product_description_db(session, id)
    return description


@app.put('/products/{id}')
async def update_product_description(
    id: int,
    new_description: str,
    session: AsyncSession = Depends(database.get_session)
):
    updated = await database.update_product_discription_db(
        session,
        id,
        new_description
    )
    print(f'this is description: {new_description}')
    print(f'this is update: {updated}')
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    return {'message': 'Description updated successfully'}


@app.delete('/products/{id}')
async def delete_product(
    id: int,
    session: AsyncSession = Depends(database.get_session)
):
    await database.delete_product_db(session, id)


# эндпоинты для orders
@app.post('/orders')
async def create_order(
    items_data: List[OrderItemCreate],
    session: AsyncSession = Depends(database.get_session)
):
    await OrderFactory.create_order(session, items_data)


@app.get('/orders')
async def get_orders(session: AsyncSession = Depends(database.get_session)):
    orders = await database.get_orders_db(session)
    return orders


@app.get('/orders/{id}')
async def get_order_by_id(
    id: int,
    session: AsyncSession = Depends(database.get_session)
):
    order = await database.get_order_by_id_db(session, id)
    return order


@app.patch('/orders/{id}/status')
async def order_status_refresh(
    id: int,
    new_status: OrderStatus,
    session: AsyncSession = Depends(database.get_session)
):
    await database.order_status_refresh_db(session, id, new_status)
