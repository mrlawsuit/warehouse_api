from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.models import Product
from app.schemas import ProductCreate


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
