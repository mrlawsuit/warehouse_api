import enum

class OrderStatus(enum.Enum):
    in_process = 'в процессе'
    sent = 'отправлен'
    delivered = 'доставлен'
    