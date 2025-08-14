from src.exceptions import ElementNotFound, InvalidOperation

class OrderProductNotFound(ElementNotFound):
    pass

class OrderNotFound(ElementNotFound):
    pass

class OrderInventoryError(InvalidOperation):
    pass

class OrderIdempotencyError(InvalidOperation):
    pass

class OrderPaymentFailedError(InvalidOperation):
    pass
