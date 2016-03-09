from django.shortcuts import render, redirect


def card_number(request):
    if request.method == 'POST':
        return redirect('atm.views.pin_code')
    return render(request, 'atm/card_number.html')


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


def error(request):
    return render(request, 'atm/error.html', {'message': 'Something wrong'})


def logout(request):
    return redirect('atm.views.card_number')
