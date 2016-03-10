from django.db import models
from decimal import Decimal


class Card(models.Model):
    number = models.CharField(max_length=19)
    pin = models.IntegerField()
    active = models.BooleanField()
    balance = models.DecimalField(
        max_digits=6, decimal_places=2, default=Decimal('0.00'))


class Operation(models.Model):
    CHECK_BALANCE = 0
    WITHDRAWAL = 1
    WRONG_PIN = 2
    BLOCKING = 3

    TYPE_CHOICES = (
        (CHECK_BALANCE, 'Check Balance'),
        (WITHDRAWAL, 'Withdrawal'),
        (WRONG_PIN, 'Wrong PIN'),
        (BLOCKING, 'Blocking card')
    )

    operation_type = models.SmallIntegerField(choices=TYPE_CHOICES)
    time = models.DateTimeField(auto_now_add=True)
    card = models.ForeignKey(Card)
    withdrawal_amount = models.IntegerField(default=0)
