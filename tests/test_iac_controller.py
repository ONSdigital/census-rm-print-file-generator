import responses

from iac_controller import IACController
from tests import IACConfigTestCase


class TestIACController(IACConfigTestCase):

    def test_get_iac(self):
        iac_batch = ['testiaccode1']
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(responses.POST, f'{self.test_iac_url}/iacs', json=iac_batch)
            iac_controller = IACController(max_total_iacs=1, batch_size=1)
            iac = iac_controller.get_iac()
        assert iac == iac_batch[0]

    def test_get_iac_multiple_batches(self):
        iac_batch_1 = ['testiaccode1', 'testiaccode2']
        iac_batch_2 = ['testiaccode3']
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(responses.POST, f'{self.test_iac_url}/iacs', json=iac_batch_1)
            iac_controller = IACController(max_total_iacs=3, batch_size=2)
            first_iac = iac_controller.get_iac()

        second_iac = iac_controller.get_iac()

        assert first_iac in iac_batch_1
        assert second_iac in iac_batch_1

        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(responses.POST, f'{self.test_iac_url}/iacs', json=iac_batch_2)
            third_iac = iac_controller.get_iac()

        assert third_iac == iac_batch_2[0]
