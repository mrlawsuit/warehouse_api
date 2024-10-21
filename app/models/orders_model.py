from typing import List
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, Enum, DateTime, func

from ..schemas import OrderStatus
from .base_model import Base
from .order_items_model import OrderItem


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))

    items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='order')
