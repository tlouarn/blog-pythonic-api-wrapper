from dataclasses import dataclass


@dataclass
class TradeDTO:
    id_: str
    way: str
    stock: str
    quantity: int
    price: str
    currency: str
    trade_date: str
    value_date: str


@dataclass
class TradeToBookDTO:
    way: str
    stock: str
    quantity: int
    price: str
    currency: str
    trade_date: str
    value_date: str
