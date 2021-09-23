import requests
from django.shortcuts import render
from .services import getApiService

# Create your views here.
def chart(request):
    bitcoin_price= None
    wrong_input = None

    initiateApiGet=getApiService()

    date_from, date_to = initiateApiGet.getCurrentDateView() #get the dates for present day and present day - 10 days 

    bitcoin_price,search_form= initiateApiGet.makeDefaultApiCall(date_from, date_to) #use the 10days period obtained from the function above to get dafualt 10days data

    from_date, to_date = initiateApiGet.getUserDateView(request) #if request method is 'post', validate the form and get date range supplied by user and use it for the api call
    
    if from_date is not None and to_date is not None:  #check if data was supplied by the user
        bitcoin_price, date_from, date_to, wrong_input, search_form = initiateApiGet.userBtcDataChart(from_date, to_date, wrong_input) #if there is data supplied my the user via the form, proceed to make the api call and retrieve the required data

    context = {
        'search_form': search_form,
        'price': bitcoin_price,
        'wrong_input':wrong_input,
        'date_from':date_from,
        'date_to':date_to
        }

    return render(request, "btc/chart.html", context)

