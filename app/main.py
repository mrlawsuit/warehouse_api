from fastapi import FastAPI

from app.routers import products_router, orders_router

app = FastAPI()

app.include_router(products_router.router)
app.include_router(orders_router.router)
