import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Card


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
    if not request.session.get('card_number'):
        return error_message(request, 'You don’t have access to this page')

    if request.method != 'POST':
        return render(request, 'atm/pin_code.html')

    return redirect('atm.views.operations')


def operations(request):
    return render(request, 'atm/operations.html')


def balance(request):
    return render(request, 'atm/balance.html')


def withdrawal(request):
    if request.method == 'POST':
        if request.POST.get('amount'):
            return redirect('atm.views.report')
        return redirect('atm.views.error')
    return render(request, 'atm/withdrawal.html')


def report(request):
    return render(request, 'atm/report.html')


def error(request):
    return render(request, 'atm/error.html')


def logout(request):
    return redirect('atm.views.card_number')
