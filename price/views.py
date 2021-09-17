import requests
from django.shortcuts import render

# Create your views here.

def chart(request):
    # price= None
    filtered_price = {}
    response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2021-09-08&end=2021-09-17&index=[USD]')
    price = response.json()
    bitcoin_price=price.get("bpi")

    for key, value in bitcoin_price.items():
        if key >= '2021-09-08' and key <= '2021-09-14':
            filtered_price[key] = value
            # print(filtered_price)
    price= filtered_price

    context = {
        "price": price
        }

    return render(request, "btc/chart.html", context)
