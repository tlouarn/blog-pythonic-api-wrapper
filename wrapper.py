import dataclasses
import datetime as dt
import json
import logging
import requests

from requests.exceptions import HTTPError
from typing import List

from model import TradeDTO, TradeToBookDTO
from mapper import TradeMapper, TradeToBookMapper
from utils import response_formatter


class ETPSWrapper:
    ROOT = 'https://api.etps.world/'
    TRADES_PATH = 'trades'

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_trade(self, trade_id: str) -> TradeDTO:
        url = '/'.join([self.ROOT, self.TRADES_PATH, trade_id])
        res = requests.get(url)
        self.logger.debug(response_formatter(res))

        if res.status_code == 200:
            api_dict = json.loads(res.text)
            dto_dict = TradeMapper().to_dto(api_dict)
            return TradeDTO(**dto_dict)

        else:
            raise HTTPError(f'HTTP Error {res.status_code}: {res.reason}')

    def post_trade(self, trade: TradeToBookDTO) -> str:
        url = '/'.join([self.ROOT, self.TRADES_PATH])

        dto_dict = dataclasses.asdict(trade)
        api_dict = TradeToBookMapper().to_api(dto_dict)
        payload = json.dumps(api_dict)
        res = requests.post(url, data=payload)
        self.logger.debug(response_formatter(res))

        if res.status_code == 201:
            api_dict = json.loads(res.text)
            return api_dict['id']

        else:
            raise HTTPError(f'HTTP Error {res.status_code}: {res.reason}')

    def delete_trade(self, trade_id: str) -> None:
        url = '/'.join([self.ROOT, self.TRADES_PATH, trade_id])
        res = requests.delete(url)
        self.logger.debug(response_formatter(res))

        if res.status_code != 204:
            raise HTTPError(f'HTTP Error {res.status_code}: {res.reason}')

    def search_trades(self, trade_date: dt.date, stock: str = None) -> List[TradeDTO]:
        url = '/'.join([self.ROOT, self.TRADES_PATH])
        params = {'trade-date': trade_date.strftime('%Y-%m-%d')}

        if stock:
            params['stock'] = stock

        res = requests.get(url, params=params)
        self.logger.debug(response_formatter(res))

        if res.status_code == 200:
            trades_list = []
            res_dict = json.loads(res.text)
            for api_dict in res_dict['results']:
                dto_dict = TradeMapper().to_dto(api_dict)
                trades_list.append(TradeDTO(**dto_dict))

            # If more results, loop through the results
            while res_dict['total'] > res_dict['offset'] + res_dict['limit']:
                params['offset'] = res_dict['offset'] + res_dict['limit']
                params['limit'] = res_dict['limit']
                res = requests.get(url, params=params)
                self.logger.debug(response_formatter(res))

                res_dict = json.loads(res.text)
                for api_dict in res_dict['results']:
                    dto_dict = TradeMapper().to_dto(api_dict)
                    trades_list.append(TradeDTO(**dto_dict))

            return trades_list

        elif res.status_code == 404:
            return []

        else:
            raise HTTPError(f'HTTP Error {res.status_code}: {res.reason}')
