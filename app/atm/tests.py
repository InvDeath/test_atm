from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class CardNumberTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_user_can_input_number(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/card_number.html')

    def test_process_valid_data(self):
        assert False

    def test_blocked_card_message(self):
        assert False

    def test_valid_card_and_number(self):
        assert False


class PinTestCase(TestCase):

    def test_only_after_card_number(self):
        assert False

    def test_wrong_pin_message(self):
        assert False

    def test_block_card(self):
        assert False

    def test_valid_pin(self):
        assert False


class OperationsTestCase(TestCase):

    def test_access(self):
        assert False

    def test_render(self):
        assert False


class BalanceTestCase(TestCase):

    def test_access(self):
        assert False

    def test_balance_appears(self):
        assert False


class WithdrawalTestCase(TestCase):

    def test_access(self):
        assert False

    def test_wrong_amount(self):
        assert False

    def test_success_report(self):
        assert False


class ReportTestCase(TestCase):

    def test_access(self):
        assert False

    def test_report_by_id(self):
        assert False


class ExitTestCase(TestCase):

    def test_exit_view(self):
        assert False

    def test_session_expire(self):
        assert False
