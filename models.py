from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy import String, Integer, FLOAT, Enum, DateTime, ForeignKey
from schemas import OrderStatus


class Base(DeclarativeBase):
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

class Product(Base):
    __table_name__ = 'products'

    id: Mapped[int] = mapped_column(Integer primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(FLOAT)
    quantity: Mapped[int] = mapped_column(Integer)


class Order(Base):
    __table_name__ = 'orders'

    id: Mapped[]
    created_at: Mapped[datetime] = mapped_column()
    status: Mapped[] = mapped_column(Enum(OrderStatus))


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer ForeignKey('orders.id', ondelete='SET NULL'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete='SET NULL'))
    order_quantity: Mapped[int] = mapped_column(Integer)

