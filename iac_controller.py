import os
from collections import deque

import requests
from requests.auth import HTTPBasicAuth


class IACController:
    def __init__(self, max_total_iacs, batch_size=1000):
        self._iac_cache = deque()
        self._max_total_iacs = max_total_iacs
        self._total_iacs_fetched = 0
        self._iac_url = f'{os.getenv("IAC_PROTOCOL")}://{os.getenv("IAC_HOST")}:{os.getenv("IAC_PORT")}'
        self._iac_auth = HTTPBasicAuth(os.getenv('IAC_USERNAME'), os.getenv('IAC_PASSWORD'))
        self._batch_size = batch_size

    def get_iac(self):
        try:
            return self._iac_cache.pop()
        except IndexError:
            self._generate_iac_batch()
        return self._iac_cache.pop()

    def _generate_iac_batch(self):
        count = self._batch_size if self._batch_size < self._max_total_iacs - self._total_iacs_fetched else self._max_total_iacs - self._total_iacs_fetched
        response = requests.post(f'{self._iac_url}/iacs',
                                 json={'count': str(count), 'createdBy': 'SCRIPT'},
                                 auth=self._iac_auth)
        response.raise_for_status()
        iacs = response.json()
        self._iac_cache.extend(iacs)
        self._total_iacs_fetched += len(iacs)
