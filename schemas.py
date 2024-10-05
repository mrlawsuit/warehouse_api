import enum
from pydantic import BaseModel


class OrderStatus(enum.Enum):
    in_process = 'в процессе'
    sent = 'отправлен'
    delivered = 'доставлен'
    
# для создания товара
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    quantity: int


# для создания заказа 
class OrderCreate(BaseModel):
    items: list
