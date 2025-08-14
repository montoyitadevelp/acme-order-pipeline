import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_CREATED: _ClassVar[EventType]
    PAYMENT_PROCESSED: _ClassVar[EventType]
    ORDER_CONFIRMED: _ClassVar[EventType]
    ORDER_FAILED: _ClassVar[EventType]

class PaymentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_PENDING: _ClassVar[PaymentStatus]
    PAYMENT_COMPLETED: _ClassVar[PaymentStatus]
    PAYMENT_FAILED: _ClassVar[PaymentStatus]

class FailureReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    INSUFFICIENT_INVENTORY: _ClassVar[FailureReason]
    PAYMENT_DECLINED: _ClassVar[FailureReason]
    INVALID_PRODUCT: _ClassVar[FailureReason]
    SYSTEM_ERROR: _ClassVar[FailureReason]
ORDER_CREATED: EventType
PAYMENT_PROCESSED: EventType
ORDER_CONFIRMED: EventType
ORDER_FAILED: EventType
PAYMENT_PENDING: PaymentStatus
PAYMENT_COMPLETED: PaymentStatus
PAYMENT_FAILED: PaymentStatus
INSUFFICIENT_INVENTORY: FailureReason
PAYMENT_DECLINED: FailureReason
INVALID_PRODUCT: FailureReason
SYSTEM_ERROR: FailureReason

class OrderEvent(_message.Message):
    __slots__ = ("event_id", "order_id", "event_type", "timestamp", "order_created", "payment_processed", "order_confirmed", "order_failed")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ORDER_CREATED_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_PROCESSED_FIELD_NUMBER: _ClassVar[int]
    ORDER_CONFIRMED_FIELD_NUMBER: _ClassVar[int]
    ORDER_FAILED_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    order_id: str
    event_type: EventType
    timestamp: _timestamp_pb2.Timestamp
    order_created: OrderCreated
    payment_processed: PaymentProcessed
    order_confirmed: OrderConfirmed
    order_failed: OrderFailed
    def __init__(self, event_id: _Optional[str] = ..., order_id: _Optional[str] = ..., event_type: _Optional[_Union[EventType, str]] = ..., timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., order_created: _Optional[_Union[OrderCreated, _Mapping]] = ..., payment_processed: _Optional[_Union[PaymentProcessed, _Mapping]] = ..., order_confirmed: _Optional[_Union[OrderConfirmed, _Mapping]] = ..., order_failed: _Optional[_Union[OrderFailed, _Mapping]] = ...) -> None: ...

class OrderCreated(_message.Message):
    __slots__ = ("order_id", "customer", "items")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    CUSTOMER_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    customer: Customer
    items: _containers.RepeatedCompositeFieldContainer[OrderItem]
    def __init__(self, order_id: _Optional[str] = ..., customer: _Optional[_Union[Customer, _Mapping]] = ..., items: _Optional[_Iterable[_Union[OrderItem, _Mapping]]] = ...) -> None: ...

class PaymentProcessed(_message.Message):
    __slots__ = ("order_id", "payment_result")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    PAYMENT_RESULT_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    payment_result: PaymentResult
    def __init__(self, order_id: _Optional[str] = ..., payment_result: _Optional[_Union[PaymentResult, _Mapping]] = ...) -> None: ...

class OrderConfirmed(_message.Message):
    __slots__ = ("order_id", "summary")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    summary: OrderSummary
    def __init__(self, order_id: _Optional[str] = ..., summary: _Optional[_Union[OrderSummary, _Mapping]] = ...) -> None: ...

class OrderFailed(_message.Message):
    __slots__ = ("order_id", "reason", "error_message")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    reason: FailureReason
    error_message: str
    def __init__(self, order_id: _Optional[str] = ..., reason: _Optional[_Union[FailureReason, str]] = ..., error_message: _Optional[str] = ...) -> None: ...

class Customer(_message.Message):
    __slots__ = ("user_id", "email")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    email: str
    def __init__(self, user_id: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class OrderItem(_message.Message):
    __slots__ = ("product_id", "sku", "name", "price", "quantity")
    PRODUCT_ID_FIELD_NUMBER: _ClassVar[int]
    SKU_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    product_id: str
    sku: str
    name: str
    price: float
    quantity: int
    def __init__(self, product_id: _Optional[str] = ..., sku: _Optional[str] = ..., name: _Optional[str] = ..., price: _Optional[float] = ..., quantity: _Optional[int] = ...) -> None: ...

class PaymentResult(_message.Message):
    __slots__ = ("status", "transaction_id", "amount", "failure_reason")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    FAILURE_REASON_FIELD_NUMBER: _ClassVar[int]
    status: PaymentStatus
    transaction_id: str
    amount: float
    failure_reason: str
    def __init__(self, status: _Optional[_Union[PaymentStatus, str]] = ..., transaction_id: _Optional[str] = ..., amount: _Optional[float] = ..., failure_reason: _Optional[str] = ...) -> None: ...

class OrderSummary(_message.Message):
    __slots__ = ("subtotal", "tax_amount", "total_amount")
    SUBTOTAL_FIELD_NUMBER: _ClassVar[int]
    TAX_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    subtotal: float
    tax_amount: float
    total_amount: float
    def __init__(self, subtotal: _Optional[float] = ..., tax_amount: _Optional[float] = ..., total_amount: _Optional[float] = ...) -> None: ...
