import pytest
from httpx import AsyncClient

from app.main import app
from app.schemas import ProductCreate, OrderItemCreate


@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        product_data = ProductCreate(name='Product 1', description='test product', price=10.5, quantity=5)
        response = await client.post('/products/', json=product_data.model_dump())
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_products():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        response = await client.get('/products')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_product_description():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get('/products/1')  # перед этим необходимо будет создать продук с таким айдишником 
        assert response.status_code == 200
        assert 'description' in response.json()

@pytest.mark.asyncio
async def test_update_product_description():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        new_description = 'Updated description'
        response = await client.put('/products/1', json={'new_description': new_description})
        assert response.status_code == 200
        print(f'THIS IS RESPONSE {response}')
        assert response.json()['message'] == 'Description updated successfully'

@pytest.mark.asyncio
async def test_create_order():
    async with AsyncClient(app=app, base_url='http://localhost:8000') as client:
        order_data = [OrderItemCreate(product_id=2, quantity=2)]
        response = await client.post('/orders', json=[item.model_dump() for item in order_data])
        assert response.status_code == 200

