from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, ForeignKey

from .base_model import Base
from .orders_model import Order
from .products_model import Product


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id', ondelete='SET NULL'))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey('products.id', ondelete='SET NULL'))
    order_quantity: Mapped[int] = mapped_column(Integer)

    order: Mapped['Order'] = relationship('Order', back_populates='items')
    product: Mapped['Product'] = relationship('Product', back_populates='order_items')
