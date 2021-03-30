import datetime as dt
import pytest
import requests

from decimal import Decimal
from unittest import mock

from model import Way
from model import TradeDTO
from wrapper import ETPSWrapper


@mock.patch('requests.get')
def test_get_trade(mock_response):
    mock_response.return_value.request.method = 'GET'
    mock_response.return_value.url = 'https://api.etps.world/trades/d76f36f0-cbdc-4481-9a46-36837d1847da'
    mock_response.return_value.status_code = 200
    mock_response.return_value.text = '{ \
        "id": "d76f36f0-cbdc-4481-9a46-36837d1847da", \
        "way": "BUY", \
        "stock": "AAPL US", \
        "quantity": 54123, \
        "price": "127.79", \
        "currency": "USD", \
        "tradeDate": "2021-03-01", \
        "valueDate": "2021-03-03" \
        }'
    mock_response.return_value.content = bytes(mock_response.return_value.text, 'UTF-8')
    mock_response.return_value.elapsed = dt.timedelta(microseconds=2100000)
    trade_dto = ETPSWrapper().get_trade('d76f36f0-cbdc-4481-9a46-36837d1847da')

    assert trade_dto.id_ == 'd76f36f0-cbdc-4481-9a46-36837d1847da'
    assert trade_dto.way == 'BUY'
    assert trade_dto.stock == 'AAPL US'
    assert trade_dto.quantity == 54123
    assert trade_dto.price == '127.79'
    assert trade_dto.currency == 'USD'
    assert trade_dto.trade_date == '2021-03-01'
    assert trade_dto.value_date == '2021-03-03'


@mock.patch('requests.get')
def test_get_trade_not_found(mock_response):
    mock_response.return_value.request.method = 'GET'
    mock_response.return_value.url = 'https://api.etps.world/trades/xxxxxxxxxx'
    mock_response.return_value.status_code = 404
    mock_response.return_value.text = ''
    mock_response.return_value.content = bytes(mock_response.return_value.text, 'UTF-8')
    mock_response.return_value.elapsed = dt.timedelta(microseconds=2100000)

    with pytest.raises(requests.exceptions.HTTPError):
        trade = ETPSWrapper().get_trade('xxxxxxxxxx')


@mock.patch('requests.post')
def test_post_trade(mock_response):
    trade = TradeDTO('', Way.BUY, 'AAPL US', 54123, Decimal('127.79'), 'USD', dt.date(2021, 3, 1),
                  dt.date(2021, 3, 3))
    mock_response.return_value.request.method = 'POST'
    mock_response.return_value.url = 'https://api.etps.world/trades/d76f36f0-cbdc-4481-9a46-36837d1847da'
    mock_response.return_value.status_code = 201
    mock_response.return_value.text = '{ \
        "id": "d76f36f0-cbdc-4481-9a46-36837d1847da" \
        }'
    mock_response.return_value.content = bytes(mock_response.return_value.text, 'UTF-8')
    mock_response.return_value.elapsed = dt.timedelta(microseconds=2100000)

    trade_id = ETPSWrapper().post_trade(trade)

    assert trade_id == 'd76f36f0-cbdc-4481-9a46-36837d1847da'


@mock.patch('requests.delete')
def test_delete_trade(mock_response):
    mock_response.return_value.request.method = 'DELETE'
    mock_response.return_value.url = 'https://api.etps.world/trades/d76f36f0-cbdc-4481-9a46-36837d1847da'
    mock_response.return_value.status_code = 204
    mock_response.return_value.text = ''
    mock_response.return_value.content = bytes(mock_response.return_value.text, 'UTF-8')
    mock_response.return_value.elapsed = dt.timedelta(microseconds=2100000)

    ETPSWrapper().delete_trade('d76f36f0-cbdc-4481-9a46-36837d1847da')


@mock.patch('requests.get')
def test_search_trades(mock_response):
    mock_response.return_value.request.method = 'GET'
    mock_response.return_value.url = 'https://api.etps.world/trades?trade-date=2021-03-01&stock=AAPL%20US'
    mock_response.return_value.status_code = 200
    mock_response.return_value.text = '{ \
      "limit" : 20, \
      "offset" : 0, \
      "total" : 2, \
      "results" :  \
        [{ \
            "id": "d76f36f0-cbdc-4481-9a46-36837d1847da", \
            "way": "BUY", \
            "stock": "AAPL US", \
            "quantity": 54123, \
            "price": "127.79", \
            "currency": "USD", \
            "tradeDate": "2021-03-01", \
            "valueDate": "2021-03-03" \
        },  \
        { \
            "id": "0f0a9b7d-38f8-42f0-87ee-3b7833285218", \
            "way": "BUY", \
            "stock": "AAPL US", \
            "quantity": 8458, \
            "price": "127.79", \
            "currency": "USD", \
            "tradeDate": "2021-03-01", \
            "valueDate": "2021-03-03" \
        }] \
    }'
    mock_response.return_value.content = bytes(mock_response.return_value.text, 'UTF-8')
    mock_response.return_value.elapsed = dt.timedelta(microseconds=2100000)

    trade_list = ETPSWrapper().search_trades(dt.date(2021, 3, 1), stock='AAPL US')

    assert len(trade_list) == 2


if __name__ == '__main__':
    test_get_trade()
    test_get_trade_not_found()
    test_post_trade()
    test_delete_trade()
    test_search_trades()
