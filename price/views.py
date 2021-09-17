import requests
from django.shortcuts import render

# Create your views here.

def chart(request):
    response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2021-08-01&end=2021-08-10&index=[USD]')
    price = response.json()
    return render(request, "btc/chart.html", {"price": price})
