from django.shortcuts import render


def card_number(request):
    return render(request, 'atm/card_number.html')
