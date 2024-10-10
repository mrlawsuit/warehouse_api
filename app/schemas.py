import enum
from pydantic import BaseModel
from typing import Union


class OrderStatus(enum.Enum):
    in_process = 'в процессе'
    sent = 'отправлен'
    delivered = 'доставлен'
    
# для создания товара
class ProductCreate(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    quantity: int


# для создания заказа 
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: list

