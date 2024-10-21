from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Integer, FLOAT

from .base_model import Base
from .order_items_model import OrderItem


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(FLOAT)
    quantity: Mapped[int] = mapped_column(Integer)

    order_items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='product')