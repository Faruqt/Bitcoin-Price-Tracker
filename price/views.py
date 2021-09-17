import requests
from django.shortcuts import render
from .forms import PriceSearchForm

# Create your views here.

def chart(request):
    price= None
    wrong_input = None
    length= None
    filtered_price = {} #declare empty dict to hold filtered price
    
    response = requests.get('https://api.coindesk.com/v1/bpi/historical/close.json?start=2021-09-08&end=2021-09-17&index=[USD]') #get api respnse data from coindesk
    prices = response.json() #convert response to json format
    bitcoin_price=prices.get("bpi") #filter prices based on "bpi" values only

    search_form= PriceSearchForm(request.POST or None) #get post request from the front end
    if request.method == 'POST': 
        date_from = request.POST.get('date_from') #extract input 1 from submitted data
        date_to = request.POST.get('date_to') #extract input 1 from submitted data

        if date_to > date_from:     #confirm that input2 is greater than input 1
            for key, value in bitcoin_price.items(): #filter bitcoin prices and date with the key and value
                if key >= date_from and key <= date_to:
                    filtered_price[key] = value #populate the filtered_price 'dict' with the filtered data
            price= filtered_price    #append the 'dict' to the price which will be used as context when the page is being rendered
            length = len(price)
        else:
            wrong_input = 'Wrong date input selection, please try again' #print out an error message if the user chooses a date that is greater than input1's date 

    search_form= PriceSearchForm() #reset form data before passing everytime the page loads
    context = {
        'search_form': search_form,
        'price': price,
        'prices': prices,
        'wrong_input':wrong_input,
        'length': length
        }

    return render(request, "btc/chart.html", context)
