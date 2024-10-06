from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select

from models import Product
from config import DATABASE_URL
from schemas import ProductCreate

engine = create_async_engine(DATABASE_URL, echo=True)


async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_product(product: ProductCreate):
    #print(product.model_dump())
    async with async_session() as session:
        new_product = product.model_dump()
        #print(f'product table {type(Product(**new_product))}')
        #print(f'variable new product {type(new_product)}')
        session.add(Product(**new_product))
        await session.commit()

async def get_products():
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        print(products)
    return products