from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import ProductCreate
import app.database as database


router = APIRouter()


@router.post('/products')
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(database.get_session)
):
    await database.create_product_db(session, product)


@router.get('/products')
async def get_products(session: AsyncSession = Depends(database.get_session)):
    products = await database.get_products_db(session)
    return products


@router.get('/products/{id}')
async def get_product_description(
    id: int,
    session: AsyncSession = Depends(database.get_session)
):
    description = await database.get_product_description_db(session, id)
    return description


@router.put('/products/{id}')
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
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found'
        )
    return {'message': 'Description updated successfully'}


@router.delete('/products/{id}')
async def delete_product(
    id: int,
    session: AsyncSession = Depends(database.get_session)
):
    await database.delete_product_db(session, id)
