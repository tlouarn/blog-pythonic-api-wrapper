from mapper import TradeMapper

TEST_DTO_DICT = {
    'id_': 'd76f36f0-cbdc-4481-9a46-36837d1847da',
    'way': 'BUY',
    'stock': 'AAPL US',
    'quantity': 54123,
    'price': '127.79',
    'currency': 'USD',
    'trade_date': '2021-03-01',
    'value_date': '2021-03-03'
}


def test_mapper_dto_to_api():
    api_dict = TradeMapper().to_api(TEST_DTO_DICT)

    assert api_dict['id'] == TEST_DTO_DICT['id_']
    assert api_dict['way'] == TEST_DTO_DICT['way']
    assert api_dict['stock'] == TEST_DTO_DICT['stock']
    assert api_dict['quantity'] == TEST_DTO_DICT['quantity']
    assert api_dict['price'] == TEST_DTO_DICT['price']
    assert api_dict['currency'] == TEST_DTO_DICT['currency']
    assert api_dict['tradeDate'] == TEST_DTO_DICT['trade_date']
    assert api_dict['valueDate'] == TEST_DTO_DICT['value_date']


def test_mapper_map_unmap():
    api_dict = TradeMapper().to_api(TEST_DTO_DICT)
    dto_dict = TradeMapper().to_dto(api_dict)

    assert api_dict == dto_dict


if __name__ == '__main__':
    test_mapper_dto_to_api()
