import json
import requests

from lib.utils import func_args_preprocessing
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



class CoinGeckoAPI:
    __API_URL_BASE = 'https://api.coingecko.com/api/v3/'

    def __init__(self, api_base_url=__API_URL_BASE):
        self.api_base_url = api_base_url
        self.request_timeout = 10

        self.session = requests.Session()
        retry_strategy = Retry(
            total=10,
            status_forcelist=[429, 502, 503, 504],
            method_whitelist=['GET'],
            backoff_factor=1
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retry_strategy))

    def __request(self, url, include_response_header=False):
        try:
            response = self.session.get(url, timeout=self.request_timeout)
        except requests.exceptions.RequestException:
            raise
        try:
            if response.status_code == 404:
                print(f'Invalid coin id in url {url}; skipping request', flush=True)
                content = {}
            else:
                response.raise_for_status()
                content = json.loads(response.content.decode('utf-8'))
            if include_response_header:
                return content, response.headers
            else:
                return content
        except Exception as e:
            try:
                content = json.loads(response.content.decode('utf-8'))
                raise ValueError(content)
            except json.decoder.JSONDecodeError:
                pass
            raise

    def __api_url_params(self, api_url, params, api_url_has_params=False):
        if params:
            api_url += '&' if api_url_has_params else '?'
            for key, value in params.items():
                if type(value) == bool:
                    value = str(value).lower()
                api_url += "{0}={1}&".format(key, value)
            api_url = api_url[:-1]
        return api_url

    @func_args_preprocessing
    def __get_coin_ticker_by_id(self, id, include_response_header=False, **kwargs):
        """Get coin tickers (paginated to 100 items)"""
        api_url = '{0}coins/{1}/tickers'.format(self.api_base_url, id)
        api_url = self.__api_url_params(api_url, kwargs)
        return self.__request(api_url, include_response_header)

    def __extract_tickers(self, response: dict):
        return [ticker['market']['identifier'] for ticker in response['tickers']]

    def get_exchanges(self, id):
        """Get all ticker identifiers for a given id"""
        first_batch, response_header = self.__get_coin_ticker_by_id(id, include_response_header=True)
        if first_batch:
            tickers = self.__extract_tickers(first_batch)
            total_tickers = int(response_header['total'])
            page = 0
            while total_tickers > len(tickers):
                page += 1
                batch = self.__get_coin_ticker_by_id(id, page=page)
                tickers.extend(self.__extract_tickers(batch))
            return {
                'id': id,
                'exchanges': tickers
            }
