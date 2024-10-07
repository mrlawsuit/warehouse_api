from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, update, delete

from models import Product
from config import DATABASE_URL
from schemas import ProductCreate

engine = create_async_engine(DATABASE_URL, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)


# корутины для таблицы товаров

async def create_product_db(product: ProductCreate):
    # print(product.model_dump())
    async with async_session() as session:
        new_product = product.model_dump()
        # print(f'product table {type(Product(**new_product))}')
        # print(f'variable new product {type(new_product)}')
        session.add(Product(**new_product))
        await session.commit()


async def get_products_db():
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        # print(products)
    return products


async def get_product_description_db(id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Product.description).where(Product.id == id)
        )
        description = result.scalars().one_or_none()
        # print(description)
    return description


async def update_product_discription_db(id: int, new_description: str):
    async with async_session() as session:
        updated = await session.execute(
            update(Product)
            .where(Product.id == id)
            .values(description=new_description)
        )
        await session.commit()
        print(updated)
    return updated

async def delete_product_db(id: int):
    async with async_session() as session:
        await session.execute(
            delete(Product)
            .where(Product.id == id)
        )
        await session.commit()
