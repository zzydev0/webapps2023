from django.db import models


# Create your models here.

class CurrencyConverter(models.Model):
    original_currency = models.CharField(max_length=8)
    target_currency = models.CharField(max_length=8)
    convert_rate = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.original_currency + '->' + self.target_currency

    class Meta:
        verbose_name = 'converter'
        verbose_name_plural = verbose_name
