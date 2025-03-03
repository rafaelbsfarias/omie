from typing import Callable, Union

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry


class Session:
    def __init__(self) -> None:
        self._session = requests.Session()
        self.retry = Retry(
            connect=1,
            total=5,
            # define tempo de espera entre as tentativas
            backoff_factor=1,
            status_forcelist=[
                429,
                500,
                502,
                503,
                504,
            ],  # 492 too many requests | Família do status 500 (erro servidor)
            allowed_methods=(["GET", "POST", "PUT", "DELETE"]),
        )
        self.adapter = HTTPAdapter(max_retries=self.retry)
        self._session.mount("https://", self.adapter)
        self._session.mount("http://", self.adapter)

    def get(self) -> Union[requests.Response, None]:
        return self._session


class Api:
    def __init__(
        self,
        url: str,
        headers: dict = None,
        params: dict = None,
        json: dict = None,
        proxies: dict = None,
    ) -> None:
        self.url = url
        self.headers = headers
        self.params = params
        self.json = json
        self.verify = True
        self.proxies = proxies
        self.session = Session().get()
        self.timeout = 30

    def get(self) -> Union[requests.Response, None]:
        response = self.session.get(
            url=self.url,
            headers=self.headers,
            params=self.params,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        return response

    def post(self) -> Union[requests.Response, None]:
        response = self.session.post(
            url=self.url,
            headers=self.headers,
            params=self.params,
            json=self.json,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        return response

    def put(self) -> Union[requests.Response, None]:
        response = self.session.put(
            url=self.url,
            headers=self.headers,
            params=self.params,
            json=self.json,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )
        return response

    def delete(self) -> Union[requests.Response, None]:
        response = self.session.delete(
            url=self.url,
            headers=self.headers,
            params=self.params,
            verify=self.verify,
            proxies=self.proxies,
            timeout=self.timeout,
        )

    def request(self, method: Callable) -> Union[dict, str, None]:
        try:
            response = method()
            if 200 <= response.status_code < 300:
                try:
                    return response.json()
                except ValueError:
                    logger.warning(
                        f"Status Code: {response.status_code}\n Success: Response content is not a JSON: {response.text}"
                    )
                    return response.text
            else:
                logger.error(
                    f"Status Code: {response.status_code}\n Error: {response.text}"
                )
                return response.text
        except RequestException as error:
            return logger.error(f"Request failed: {error}")
