import re
from django.shortcuts import render, redirect
from .models import Card


def error(request, message):
    return render(request, 'atm/error.html', {'message': message})


def card_number(request):
    if request.method != 'POST':
        return render(request, 'atm/card_number.html')

    raw_number = request.POST.get('number', '')
    pattern = re.compile('^(\d{4}-\d{4}-\d{4}-\d{4})$')

    if not pattern.match(raw_number):
        return error(request,
                     message='The card number must consist of 16 digits')

    card = (Card.objects.filter(number=raw_number) or [None])[0]

    if not card:
        return error(request, message='Card with this number not found')

    return redirect('atm.views.pin_code', card_number=raw_number)


def pin_code(request):
    if request.method == 'POST':
        return redirect('atm.views.operations')
    return render(request, 'atm/pin_code.html')


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


def logout(request):
    return redirect('atm.views.card_number')
