import responses

from iac_controller import IACController
from tests import IACConfigTestCase


class TestIACController(IACConfigTestCase):

    def test_get_iac(self):

        # Given
        iac_batch = ['testiaccode1']
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(responses.POST, f'{self.test_iac_url}/iacs', json=iac_batch)
            iac_controller = IACController(max_total_iacs=1, batch_size=1)
            iac_controller.start_fetching_iacs()

            # When
            iac = iac_controller.get_iac()

        # Then
        assert iac == iac_batch[0]

    def test_get_iac_multiple_batches(self):

        # Given
        iac_batch_1 = ['testiaccode1', 'testiaccode2']
        iac_batch_2 = ['testiaccode3']
        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(responses.POST, f'{self.test_iac_url}/iacs', json=iac_batch_1)
            iac_controller = IACController(max_total_iacs=3, batch_size=2)
            iac_controller.start_fetching_iacs()

            # When
            first_iac = iac_controller.get_iac()

        second_iac = iac_controller.get_iac()

        with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
            rsps.add(responses.POST, f'{self.test_iac_url}/iacs', json=iac_batch_2)
            third_iac = iac_controller.get_iac()

        # Then
        assert second_iac in iac_batch_1
        assert first_iac in iac_batch_1
        assert third_iac == iac_batch_2[0]
