import json

import responses

from iac_controller import IACController
from tests import IACConfigTestCase


class TestIACController(IACConfigTestCase):
    iac_batches = {'0': [], '1': ['testiaccode1'], '2': ['testiaccode2', 'testiaccode3']}

    def setUp(self) -> None:
        super().setUp()
        self.mock_call_iac_counts = []

    def tearDown(self) -> None:
        super().tearDown()
        self.mock_call_iac_counts = []

    def iac_request_callback(self, request):
        payload = json.loads(request.body)
        resp_body = TestIACController.iac_batches[payload['count']]
        self.mock_call_iac_counts.append(payload['count'])
        return 200, {}, json.dumps(resp_body)

    def test_get_iac(self):
        # Given
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add_callback(
                responses.POST, f'{self.test_iac_url}/iacs',
                callback=self.iac_request_callback,
                content_type='application/json'
            )
            iac_controller = IACController(max_total_iacs=1, batch_size=1)

            # When
            iac = iac_controller.get_iac()

        # Then
        assert self.mock_call_iac_counts == ['1']
        assert iac == self.iac_batches['1'][0]

    def test_get_iac_multiple_batches(self):
        # Given
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add_callback(
                responses.POST, f'{self.test_iac_url}/iacs',
                callback=self.iac_request_callback,
                content_type='application/json'
            )
            iac_controller = IACController(max_total_iacs=3, batch_size=2)

            # When
            # Should request 2 IACs
            first_iac = iac_controller.get_iac()
            assert self.mock_call_iac_counts == ['2']

            # Should not make another request to IAC service since there were 2 in the pool
            second_iac = iac_controller.get_iac()
            assert self.mock_call_iac_counts == ['2']

            # Should request 1 more IAC
            third_iac = iac_controller.get_iac()
            assert self.mock_call_iac_counts == ['2', '1']

        # Then
        assert second_iac in self.iac_batches['2']
        assert first_iac in self.iac_batches['2']
        assert third_iac == self.iac_batches['1'][0]
