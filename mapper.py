from bidict import bidict
from typing import Dict


class Mapper:
    MAPPING_DICT = bidict()

    def __init__(self):
        pass

    def to_api(self, input_dict: Dict) -> Dict:
        return {self.MAPPING_DICT[k]: v for k, v in input_dict.items()}

    def to_dto(self, input_dict: Dict) -> Dict:
        return {self.MAPPING_DICT.inverse[k]: v for k, v in input_dict.items()}


class TradeMapper(Mapper):
    MAPPING_DICT = bidict({
        'id_': 'id',
        'way': 'way',
        'stock': 'stock',
        'quantity': 'quantity',
        'price': 'price',
        'currency': 'currency',
        'trade_date': 'tradeDate',
        'value_date': 'valueDate'
    })


class TradeToBookMapper(Mapper):
    MAPPING_DICT = bidict({
        'way': 'way',
        'stock': 'stock',
        'quantity': 'quantity',
        'price': 'price',
        'currency': 'currency',
        'trade_date': 'tradeDate',
        'value_date': 'valueDate'
    })
