import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import Card, Operation


def error_message(request, message):
    messages.error(request, message)
    return redirect('atm.views.error')


def card_number(request):
    if request.method != 'POST':
        return render(request, 'atm/card_number.html')

    raw_number = request.POST.get('number', '')
    pattern = re.compile('^(\d{4}-\d{4}-\d{4}-\d{4})$')

    if not pattern.match(raw_number):
        return error_message(request, 'The card number must consist of 16 digits')

    card = (Card.objects.filter(number=raw_number) or [None])[0]

    if not card:
        return error_message(request, 'Card with this number not found')

    if not card.active:
        return error_message(request, 'This card is blocked')

    request.session['card_number'] = raw_number
    request.session['card_holder'] = False
    return redirect('atm.views.pin_code')


def pin_code(request):
    card_number = request.session.get('card_number')

    if not card_number:
        return error_message(request, 'You don’t have access to this page')

    if request.method != 'POST':
        return render(request, 'atm/pin_code.html')

    card = Card.objects.get(number=card_number)
    raw_pin = request.POST.get('pin_code', '')
    pattern = re.compile('^(\d{4})$')

    if not card.active or not pattern.match(raw_pin) or not card.pin == raw_pin:
        Operation.objects.create(operation_type=Operation.WRONG_PIN, card=card)
        attempts = Operation.objects.filter(
            operation_type=Operation.WRONG_PIN, card=card).count()
        if attempts >= settings.ATM_PIN_ATTEMPTS:
            card.active = False
            card.save()
            return error_message(request, 'Your card has been blocked')
        return error_message(request, 'Wrong pin code')

    request.session['card_holder'] = True
    return redirect('atm.views.operations')


def operations(request):
    if not request.session.get('card_holder'):
        return error_message(request, 'You don’t have access to this page')

    return render(request, 'atm/operations.html')


def balance(request):
    card_number = request.session.get('card_number')
    if not request.session.get('card_holder') or not card_number:
        return error_message(request, 'You don’t have access to this page')

    card = Card.objects.get(number=card_number)
    context = {
        'card_number': card_number,
        'balance': card.balance,
    }

    Operation.objects.create(operation_type=Operation.CHECK_BALANCE, card=card)

    return render(request, 'atm/balance.html', context)


def withdrawal(request):
    card_number = request.session.get('card_number')
    if not request.session.get('card_holder') or not card_number:
        return error_message(request, 'You don’t have access to this page')

    if request.method != 'POST':
        return render(request, 'atm/withdrawal.html')

    amount = int(request.POST.get('amount', 0))

    if amount <= 0:
        return error_message(request, 'Please input correct amount')

    card = Card.objects.get(number=card_number)

    if card.balance < amount:
        return error_message(request, 'Amount exceeds balance')

    card.balance -= amount
    card.save()

    Operation.objects.create(
        card=card,
        operation_type=Operation.WITHDRAWAL,
        withdrawal_amount=amount,
    )

    return redirect('atm.views.report')


def report(request):
    card_number = request.session.get('card_number')
    if not request.session.get('card_holder') or not card_number:
        return error_message(request, 'You don’t have access to this page')

    operation = Operation.objects.filter(
        card__number=card_number,
        operation_type=Operation.WITHDRAWAL
    ).select_related('card').latest('time')

    card = operation.card

    context = {
        'card_number': card.number,
        'operation_date': operation.time,
        'withdrawal': operation.withdrawal_amount,
        'balance': card.balance,
    }

    return render(request, 'atm/report.html', context)


def error(request):
    return render(request, 'atm/error.html')


def logout(request):
    del request.session['card_holder']
    del request.session['card_number']
    return redirect('atm.views.card_number')
