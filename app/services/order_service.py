from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.models import Product, Order, OrderItem
from app.schemas import OrderStatus, OrderItemCreate
from repositories.product_repository import get_product_by_id_db


class OrderReserv:
    """
    Класс для работы с количеством товара
    """
    @staticmethod
    async def reserve_product(
        session: AsyncSession,
        product_id: int,
        quantity_needed: int
    ) -> Product:
        product = await get_product_by_id_db(session, product_id)
        if not product or product.quantity < quantity_needed:
            raise ValueError(
                'Недостаточно товара на складе или товар не найден.'
            )
        product.quantity -= quantity_needed
        return product


class OrderFactory:
    @staticmethod
    async def create_order(
        session: AsyncSession,
        items_data: List[OrderItemCreate]
    ) -> Order:
        """
        Создает заказ на основе списка товаров, введенных пользовавтелем.
        """
        order = Order(status=OrderStatus.in_process)

        for item_data in items_data:
            product_id = item_data.model_dump()['product_id']
            quantity_needed = item_data.model_dump()['quantity']
            product = await OrderReserv.reserve_product(
                session,
                product_id,
                quantity_needed
            )

            order_item = OrderItem(
                product=product,
                order_quantity=quantity_needed
            )
            order.items.append(order_item)
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order


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
