import os
from collections import deque
from typing import Collection

import requests
from requests.auth import HTTPBasicAuth


class IACController:

    def __init__(self, max_total_iacs: int, batch_size: int = 1000):
        self._iac_url = os.getenv('IAC_URL')
        self._iac_auth = HTTPBasicAuth(os.getenv('IAC_USERNAME'), os.getenv('IAC_PASSWORD'))
        self._iac_pool = deque()
        self._max_total_iacs = max_total_iacs
        self._batch_size = batch_size
        self._total_iacs_fetched = 0

    def get_iac(self) -> str:
        if not self._iac_pool:
            self._add_iac_batch_to_pool()
        return self._iac_pool.pop()

    def _add_iac_batch_to_pool(self):
        count = self._batch_size if self._batch_size < self._max_total_iacs - self._total_iacs_fetched else self._max_total_iacs - self._total_iacs_fetched
        iacs = self._generate_iacs(count)
        self._iac_pool.extend(iacs)
        self._total_iacs_fetched += len(iacs)

    def _generate_iacs(self, count: int) -> Collection[str]:
        response = requests.post(f'{self._iac_url}/iacs',
                                 json={'count': str(count), 'createdBy': 'SCRIPT'},
                                 auth=self._iac_auth)
        response.raise_for_status()
        return response.json()
