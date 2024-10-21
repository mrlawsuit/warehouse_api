from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import OrderItemCreate, OrderStatus
from app.database import OrderFactory
import app.database as database

router = APIRouter()


@router.post('/orders')
async def create_order(
    items_data: List[OrderItemCreate],
    session: AsyncSession = Depends(database.get_session)
):
    await OrderFactory.create_order(session, items_data)


@router.get('/orders')
async def get_orders(session: AsyncSession = Depends(database.get_session)):
    orders = await database.get_orders_db(session)
    return orders


@router.get('/orders/{id}')
async def get_order_by_id(
    id: int,
    session: AsyncSession = Depends(database.get_session)
):
    order = await database.get_order_by_id_db(session, id)
    return order


@router.patch('/orders/{id}/status')
async def order_status_refresh(
    id: int,
    new_status: OrderStatus,
    session: AsyncSession = Depends(database.get_session)
):
    await database.order_status_refresh_db(session, id, new_status)
