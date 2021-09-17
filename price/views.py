import requests
from django.shortcuts import render
from .forms import PriceSearchForm

# Create your views here.

def chart(request):
    # price= None
    filtered_price = {}

    response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2021-09-08&end=2021-09-17&index=[USD]')
    price = response.json()
    bitcoin_price=price.get("bpi")

    search_form= PriceSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
    
        for key, value in bitcoin_price.items():
            if key >= date_from and key <= date_to:
                filtered_price[key] = value
                # print(filtered_price)
        price= filtered_price

    context = {
        'search_form': search_form,
        'price': price,
        }

    return render(request, "btc/chart.html", context)
