import decimal

from django.http import HttpResponse
from rest_framework.decorators import api_view

from convert.models import CurrencyConverter


# Create your views here.

@api_view(['GET'])
def convert(request, currency_1, currency_2, amount_of_currency_1):
    if request.method == 'GET':
        converter = CurrencyConverter.objects.filter(original_currency=currency_1).filter(target_currency=currency_2)
        convert_rate = converter.values('convert_rate')[0]['convert_rate']
        result = decimal.Decimal(amount_of_currency_1) * convert_rate
        return HttpResponse(result)
