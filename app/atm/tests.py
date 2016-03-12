import datetime
from django.test import TestCase, Client
from django.conf import settings
from django.core.urlresolvers import reverse
from .models import Card, Operation


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
        response = self.client.post(
            reverse('pin_code'), {'pin_code': '1234'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'Wrong pin code')

    def test_block_card(self):
        self.input_correct_card_number()
        for i in range(1, settings.ATM_PIN_ATTEMPTS):
            response = self.client.post(
                reverse('pin_code'), {'pin_code': '1234'}, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'atm/error.html')
            self.assertContains(response, 'Wrong pin code')
            attempts = Operation.objects.filter(
                card__number=self.client.session.get('card_number'),
                operation_type=Operation.WRONG_PIN,
            ).count()
            self.assertEqual(attempts, i)
        response = self.client.post(
            reverse('pin_code'), {'pin_code': '1234'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'been blocked')

        card = Card.objects.get(number=self.client.session.get('card_number'))

        self.assertFalse(card.active)

    def test_valid_pin(self):
        self.input_correct_card_number()
        response = self.client.post(
            reverse('pin_code'), {'pin_code': '0000'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/operations.html')
        self.assertTrue(self.client.session.get('card_holder'))


class OperationsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_access(self):
        response = self.client.get(reverse('operations'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'access')

    def test_render(self):
        session = self.client.session
        session['card_holder'] = True
        session.save()
        response = self.client.get(reverse('operations'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/operations.html')


class BalanceTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_access(self):
        response = self.client.get(reverse('balance'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'access')

    def test_balance_appears(self):
        session = self.client.session
        session['card_number'] = '1111-1111-1111-1111'
        session['card_holder'] = True
        session.save()

        response = self.client.get(reverse('balance'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/balance.html')
        self.assertContains(response, '300.00')
        self.assertContains(response, '1111-1111-1111-1111')
        self.assertContains(response,
                            datetime.datetime.now().strftime('%dth %B %Y'))

    def test_balance_operation(self):
        session = self.client.session
        session['card_number'] = '1111-1111-1111-1111'
        session['card_holder'] = True
        session.save()

        self.client.get(reverse('balance'))
        operation = Operation.objects.get(card__number='1111-1111-1111-1111')
        self.assertEqual(operation.operation_type, Operation.CHECK_BALANCE)


class WithdrawalTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_access(self):
        response = self.client.get(reverse('withdrawal'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'access')

    def test_wrong_amount(self):
        session = self.client.session
        session['card_number'] = '1111-1111-1111-1111'
        session['card_holder'] = True
        session.save()

        response = self.client.post(
            reverse('withdrawal'), {'amount': '0'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'correct amount')

        response = self.client.post(
            reverse('withdrawal'), {'amount': '400'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'balance')

    def test_success_report(self):
        session = self.client.session
        session['card_number'] = '1111-1111-1111-1111'
        session['card_holder'] = True
        session.save()

        response = self.client.post(
            reverse('withdrawal'), {'amount': '100'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/report.html')
        card = Card.objects.get(number='1111-1111-1111-1111')
        self.assertEqual(card.balance, 200)
        operation = Operation.objects.get(card=card)
        self.assertEqual(operation.operation_type, Operation.WITHDRAWAL)
        self.assertEqual(operation.withdrawal_amount, 100)


class ReportTestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.client = Client()

    def test_access(self):
        response = self.client.get(reverse('report'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/error.html')
        self.assertContains(response, 'access')

    def test_report(self):
        session = self.client.session
        session['card_number'] = '1111-1111-1111-1111'
        session['card_holder'] = True
        session.save()

        response = self.client.post(
            reverse('withdrawal'), {'amount': '100'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'atm/report.html')
        self.assertContains(response, '1111-1111-1111-1111')


class ExitTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_exit_view(self):
        session = self.client.session
        session['card_number'] = '1111-1111-1111-1111'
        session['card_holder'] = True
        session.save()

        response = self.client.get(reverse('logout'), follow=True)

        session = self.client.session

        self.assertFalse(session.get('card_holder', False))
        self.assertFalse(session.get('card_number', False))
