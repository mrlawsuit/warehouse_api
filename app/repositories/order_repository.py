from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models import Order
from app.schemas import OrderStatus


async def get_orders_db(session: AsyncSession) -> Order:
    result = await session.execute(select(Order))
    orders = result.scalars().all()
    return orders


async def get_order_by_id_db(session: AsyncSession, id: int) -> Order:
    result = await session.execute(select(Order).where(Order.id == id))
    order = result.scalars().one_or_none()
    if not order:
        raise ValueError('Такого заказа нет в базе')
    return order


async def order_status_refresh_db(
        session: AsyncSession,
        id: int,
        new_status: OrderStatus
):
    updated = await session.execute(
        update(Order)
        .where(Order.id == id)
        .values(status=new_status)
    )
    await session.commit()
    return updated
