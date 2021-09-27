import requests
from django.shortcuts import render
from .forms import PriceSearchForm
from .services import getDateService,getDefaultData,getUserInputDateRange,outOfRange #import business logic from services.py layer
from datetime import date, timedelta , datetime

# Create your views here.
def chart(request):
    bitcoin_price= None
    wrong_input = None
    range_error = None

    initiateDateGet = getDateService()
    initiateDefaultDataGet = getDefaultData()
    initiateUserDateGet = getUserInputDateRange()
    initiateRangeErrorGet = outOfRange()

    date_from, date_to = initiateDateGet.getCurrentDateView() #get the dates for present day and present day - 10 days 

    bitcoin_price,search_form= initiateDefaultDataGet.makeDefaultApiView(date_from, date_to) #use the 10days period obtained from the function above to get dafualt 10days data

    from_date, to_date = getUserDateView(request) #if request method is 'post', validate the form and get date range supplied by user and use it for the api call
    
    date_out_of_range = initiateRangeErrorGet.ooR(from_date, to_date, range_error)

    if date_out_of_range is not None:
        range_error = date_out_of_range
    else:
        if from_date is not None and to_date is not None:  #check if data was supplied by the user
            date_today=date_to
            bitcoin_price, date_from, date_to, wrong_input = getUserInputData(from_date, to_date, date_today, wrong_input) #if there is data supplied my the user via the form, proceed to make the api call and retrieve the required data
            search_form = initiateUserDateGet.userFormInputView(from_date, to_date, date_today ) #make the date range submitted in the form supplied by the user via the form the default input of the form
        

    context = {
        'search_form': search_form,
        'price': bitcoin_price,
        'wrong_input':wrong_input,
        'date_from':date_from,
        'date_to':date_to,
        'range_error': range_error
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


def getUserInputData(date_from, date_to, date_today, wrong_input):
    from_date= None
    to_date= None
    requested_btc_price_range= None
    
    if date_to > date_from:     #confirm that input2 is greater than input 1
        if date_to > date_today:    #if the date to from input is greater than today's date; there wont be data for the extra days, so we change the 'date_to' input back to todays's date
            date_to = date_today 
        api= 'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + date_from + '&end=' + date_to + '&index=[USD]' #use the 10days period obtained above to get dafualt 10days value
        try:
            response = requests.get(api, timeout=10) #get api response data from coindesk based on date range supplied by user with a timeout of 10seconds
            response.raise_for_status()        #raise error if HTTP request returned an unsuccessful status code.
            prices = response.json() #convert response to json format
            requested_btc_price_range=prices.get("bpi") #filter prices based on "bpi" values only
            from_date= date_from
            to_date= date_to
        except requests.exceptions.ConnectionError as errc:  #raise error if connection fails
            raise ConnectionError(errc)
        except requests.exceptions.Timeout as errt:     #raise error if the request gets timed out after 10 seconds without receiving a single byte
            raise TimeoutError(errt)
        except requests.exceptions.HTTPError as err:     #raise a general error if the above named errors are not triggered 
            raise SystemExit(err)
    else:
        wrong_input = 'Wrong date input selection: date from cant be greater than date to, please try again' #print out an error message if the user chooses a date that is greater than input1's date 

    return requested_btc_price_range, from_date, to_date , wrong_input,
