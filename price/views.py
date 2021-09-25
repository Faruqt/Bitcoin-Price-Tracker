import requests
from django.shortcuts import render
from .forms import PriceSearchForm
from .services import getDateService,getDefaultData,getUserInputData #import business logic from services.py layer

# Create your views here.
def chart(request):
    bitcoin_price= None
    wrong_input = None

    initiateDateGet = getDateService()
    initiateDefaultDataGet = getDefaultData()
    initiateUserRequestGet = getUserInputData()

    date_from, date_to = initiateDateGet.getCurrentDateView() #get the dates for present day and present day - 10 days 

    bitcoin_price,search_form= initiateDefaultDataGet.makeDefaultApiView(date_from, date_to) #use the 10days period obtained from the function above to get dafualt 10days data

    from_date, to_date = getUserDateView(request) #if request method is 'post', validate the form and get date range supplied by user and use it for the api call
    
    if from_date is not None and to_date is not None:  #check if data was supplied by the user
        bitcoin_price, date_from, date_to, wrong_input, search_form = initiateUserRequestGet.userBtcDataView(from_date, to_date, wrong_input) #if there is data supplied my the user via the form, proceed to make the api call and retrieve the required data

    context = {
        'search_form': search_form,
        'price': bitcoin_price,
        'wrong_input':wrong_input,
        'date_from':date_from,
        'date_to':date_to
        }

    return render(request, "btc/chart.html", context)

#function to confirm if valid date ranges have been supplied by the user.
def getUserDateView(request):
    date_from = None
    date_to = None
    search_form= PriceSearchForm(request.POST or None) #get post request from the front end
    if request.method == 'POST': 
        if search_form.is_valid():  #Confirm if valid data was received from the form
            date_from = request.POST.get('date_from') #extract input 1 from submitted data
            date_to = request.POST.get('date_to') #extract input 2 from submitted data
        
        else:
            raise Http400("Sorry, this did not work. Invalid input")

    return date_from,date_to

