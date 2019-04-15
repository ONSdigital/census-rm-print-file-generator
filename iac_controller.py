import os
from multiprocessing.pool import ThreadPool
from queue import Queue
from typing import Collection, List, Optional

import requests
from requests.auth import HTTPBasicAuth


class IACController:

    def __init__(self, max_total_iacs: int, batch_size: int = 1000):
        self._iac_url = os.getenv('IAC_URL')
        self._iac_auth = HTTPBasicAuth(os.getenv('IAC_USERNAME'), os.getenv('IAC_PASSWORD'))
        self._iac_pool = Queue()
        self._max_total_iacs = max_total_iacs
        self._batch_size = batch_size

    def get_iac(self) -> str:
        return self._iac_pool.get(timeout=30)

    def _add_iac_batch_to_pool(self, batch_size: int):
        iacs = self._generate_iacs(batch_size)
        for iac in iacs:
            self._iac_pool.put(iac)

    def _generate_iacs(self, count: int) -> Collection[str]:
        response = requests.post(f'{self._iac_url}/iacs',
                                 json={'count': str(count), 'createdBy': 'SCRIPT'},
                                 auth=self._iac_auth)
        response.raise_for_status()
        return response.json()

    def start_fetching_iacs(self):
        batch_sizes = self._get_batch_sizes()
        ThreadPool(4).map_async(self._add_iac_batch_to_pool, batch_sizes,
                                error_callback=__class__._raise_exception)

    def _get_batch_sizes(self) -> List[int]:
        batches_sizes = [self._batch_size] * (self._max_total_iacs // self._batch_size)
        remainder_batch_size = self._max_total_iacs % self._batch_size
        if remainder_batch_size:
            batches_sizes += [remainder_batch_size]
        return batches_sizes

    @staticmethod
    def _raise_exception(e: Optional[BaseException]):
        if e is not None:
            raise e
