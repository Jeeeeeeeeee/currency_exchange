"""
doc string goes here
"""

__all__ = ['Provider', 'Currency', 'CurrencyExchangeRate']

# Standard library imports.

# Related third party imports.
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local application/library specific imports.


class Provider(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = 'provider'
        app_label = 'currency_exchange'
        verbose_name = _('Provider')
        verbose_name_plural = _('Providers')

    def __str__(self):
        return self.name or self.code


class Currency(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200, blank=False)

    class Meta:
        db_table = 'currency'
        app_label = 'currency_exchange'
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')

    def __str__(self):
        return self.name or self.code


class CurrencyExchangeRate(models.Model):
    from_currency = models.ForeignKey(
        Currency,
        related_name='from_currency',
        on_delete=models.CASCADE
    )
    to_currency = models.ForeignKey(
        Currency,
        related_name='to_currency',
        on_delete=models.CASCADE
    )
    on_date = models.DateTimeField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=24, decimal_places=12)

    class Meta:
        db_table = 'currency_exchange_rate'
        app_label = 'currency_exchange'
        verbose_name = _('Currency Exchange Rate')
        verbose_name_plural = _('Currency Exchange Rates')
