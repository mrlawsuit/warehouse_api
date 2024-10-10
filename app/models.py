from typing import List
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship
from sqlalchemy import String, Integer, FLOAT, Enum, DateTime, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs

from app.schemas import OrderStatus


class Base(AsyncAttrs, DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(FLOAT)
    quantity: Mapped[int] = mapped_column(Integer)
    
    order_items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='product')

class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))

    items: Mapped[List['OrderItem']] = relationship('OrderItem', back_populates='order')

class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id', ondelete='SET NULL'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete='SET NULL'))
    order_quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped['Order'] = relationship('Order', back_populates='items')
    product: Mapped['Product'] = relationship('Product', back_populates='order_items')
