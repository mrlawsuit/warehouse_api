from typing import List, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy import select, update, delete

from app.models import Product, Order, OrderItem
from app.config import DATABASE_URL
from app.schemas import ProductCreate, OrderStatus, OrderItemCreate

engine = create_async_engine(DATABASE_URL, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


# корутины для таблицы товаров

async def create_product_db(
        session: AsyncSession,
        product: ProductCreate
) -> None:
    new_product = product.model_dump()
    session.add(Product(**new_product))
    await session.commit()


async def get_products_db(session: AsyncSession) -> List[Product]:
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return products


async def get_product_description_db(
        session: AsyncSession,
        id: int
) -> Product:
    result = await session.execute(
        select(Product.description).where(Product.id == id)
    )
    description = result.scalars().one_or_none()
    return description


async def update_product_discription_db(
        session: AsyncSession,
        id: int,
        new_description: str
) -> Product:
    updated = await session.execute(
        update(Product)
        .where(Product.id == id)
        .values(description=new_description)
    )
    await session.commit()
    print(updated)
    return updated


async def delete_product_db(session: AsyncSession, id: int) -> None:
    await session.execute(
        delete(Product)
        .where(Product.id == id)
    )
    await session.commit()


async def get_product_by_id_db(session: AsyncSession, id: int) -> Product:
    result = await session.execute(select(Product).where(Product.id == id))
    product = result.scalar_one_or_none()
    if not product:
        raise ValueError('Такого товара нет в базе')
    return product


# инфраструктура для таблицы заказов

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
