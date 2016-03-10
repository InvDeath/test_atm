from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from .models import Card

class CardNumberTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_user_can_input_number(self):
        response = self.client.get(reverse('card_number'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/card_number.html')

    def test_wrong_number(self):
        response = self.client.post(
            reverse('card_number'),
            {'number': 'sdsadasd-4234-234-24erdfd'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, '16 digits')

    def test_card_absent(self):
        response = self.client.post(
            reverse('card_number'),
            {'number': '2222-2222-2222-2222'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'not found')

    def test_blocked_card_message(self):
        response = self.client.post(
            reverse('card_number'),
            {'number': '1234-1234-1234-1234'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'blocked')

    def test_valid_card_and_number(self):
        response = self.client.post(
            reverse('card_number'),
            {'number': '1111-1111-1111-1111'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/pin_code.html')
        self.assertEqual(
            self.client.session['card_number'], '1111-1111-1111-1111')
        self.assertFalse(self.client.session['card_holder'])


class PinTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def input_correct_card_number(self):
        self.client.post(
            reverse('card_number'),
            {'number': '1111-1111-1111-1111'}
        )

    def test_witout_card_number(self):
        response = self.client.get(reverse('pin_code'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'access')



    def test_wrong_pin_message(self):
        self.input_correct_card_number()
        response = self.client.post(reverse('pin_code'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'wrong pin')


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
