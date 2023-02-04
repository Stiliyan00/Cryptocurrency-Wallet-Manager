from datetime import datetime

import requests
from requests import Response


class CryptocurrencyCoinsAPIClient:
    @staticmethod
    def get_specific_rate_of_currency(asset_id_base: str, asset_id_quote: str) -> Response:
        url = 'https://rest.coinapi.io/v1/exchangerate/' + asset_id_base + '/' + asset_id_quote
        headers = {'X-CoinAPI-Key': 'F5DFB3A6-F7DA-4645-8DDA-A8D713C18129'}
        return requests.get(url, headers=headers)

    @staticmethod
    def get_all_current_rates_of_currency(asset_id_base: str) -> Response:
        url = 'https://rest.coinapi.io/v1/exchangerate/' + asset_id_base + '?invert=false'
        headers = {'X-CoinAPI-Key': 'F5DFB3A6-F7DA-4645-8DDA-A8D713C18129'}
        return requests.get(url, headers=headers)

    @staticmethod
    def get_currency_historical_exchange_rates(asset_id_base: str, asset_id_quote: str, period_id: str,
                                               time_start: datetime, time_end: datetime) -> Response:
        url = 'https://rest.coinapi.io/v1/exchangerate/' + asset_id_base + '/' + asset_id_quote + '/' + \
              'history?period_id=' + period_id + '&ime_start=' + time_start.strftime('%Y-%m-%dT%H:%M:%S') + \
              '&time_end=' + time_end.strftime('%Y-%m-%dT%H:%M:%S')
        # 'BTC/USD/history?period_id=1MIN&time_start=2016-01-01T00:00:00&time_end=2016-02-01T00:00:00'
        headers = {'X-CoinAPI-Key': 'F5DFB3A6-F7DA-4645-8DDA-A8D713C18129'}
        return requests.get(url, headers=headers)

    @staticmethod
    def get_list_of_all_assets() -> Response:
        url = 'https://rest.coinapi.io/v1/assets'
        headers = {'X-CoinAPI-Key': 'F5DFB3A6-F7DA-4645-8DDA-A8D713C18129'}
        return requests.get(url, headers=headers)
