import requests
from django.shortcuts import render
from datetime import date, timedelta
from .forms import PriceSearchForm

# Create your views here.
def chart(request):
    bitcoin_price= None
    wrong_input = None

    date_from, date_to = getCurrentDateView() #get the dates for present day and present day - 10 days 

    bitcoin_price= makeDefaultApiCall(date_from, date_to) #use the 10days period obtained from the function above to get dafualt 10days data

    from_date, to_date = getUserDateView(request) #if request method is 'post', get date range supplied by user and use it for the api call
    
    print(from_date)
    print(to_date)
    if from_date is not None and to_date is not None:
        bitcoin_price, date_from, date_to, wrong_input= userBtcDataChart(from_date, to_date, wrong_input) 

    search_form= PriceSearchForm() #reset form data before passing everytime the page loads
    context = {
        'search_form': search_form,
        'price': bitcoin_price,
        'wrong_input':wrong_input,
        'date_from':date_from,
        'date_to':date_to
        }

    return render(request, "btc/chart.html", context)

def getCurrentDateView():
    datetime_today = date.today() #get current date
    date_today = str(datetime_today) #convert datetime class to string
    date_10daysago = str(datetime_today - timedelta(days=10)) #get date of today -10 days

    #assign date from and date to for chart template heading 
    date_from = date_10daysago 
    date_to = date_today

    return date_from,date_to

