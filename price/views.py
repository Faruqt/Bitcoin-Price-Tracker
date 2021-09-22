import requests
from django.shortcuts import render
from datetime import date, timedelta
from .forms import PriceSearchForm

# Create your views here.

def chart(request):
    bitcoin_price= None
    wrong_input = None

    datetime_today = date.today() #get current date
    date_today = str(datetime_today) #convert datetime class to string
    date_10daysago = str(datetime_today - timedelta(days=10)) #get date of today -10 days

    #assign date from and date to for chart template heading 
    from_date = date_10daysago 
    to_date = date_today

    api= 'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + date_10daysago + '&end=' + date_today + '&index=[USD]' #use the 10days period obtained above to get dafualt 10days value
    try:
        response = requests.get(api, timeout=1) #get api response data from coindesk based on date range supplied by user
        response.raise_for_status()              #raise error if HTTP request returned an unsuccessful status code.
        prices = response.json() #convert response to json format
        bitcoin_price=prices.get("bpi") #filter prices based on "bpi" values only
    except requests.exceptions.ConnectionError as errc:  #raise error if connection fails
        raise ConnectionError(errc)
    except requests.exceptions.Timeout as errt:     #raise error if the request gets timed out without receiving a single byte
        raise TimeoutError(errt)
    except requests.exceptions.HTTPError as err:       #raise a general error if the above named errors are not triggered 
        raise SystemExit(err)

    search_form= PriceSearchForm(request.POST or None) #get post request from the front end
    if request.method == 'POST': 
            date_from = request.POST.get('date_from') #extract input 1 from submitted data
            date_to = request.POST.get('date_to') #extract input 1 from submitted data

            api= 'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + date_from + '&end=' + date_to + '&index=[USD]' #use the 10days period obtained above to get dafualt 10days value
            if date_to > date_from:     #confirm that input2 is greater than input 1
                try:
                    response = requests.get(api, timeout=1) #get api response data from coindesk based on date range supplied by user
                    response.raise_for_status()        #raise error if HTTP request returned an unsuccessful status code.
                    response = requests.get(api) #get api response data from coindesk based on date range supplied by user
                    prices = response.json() #convert response to json format
                    bitcoin_price=prices.get("bpi") #filter prices based on "bpi" values only
                except requests.exceptions.ConnectionError as errc:  #raise error if connection fails
                    raise ConnectionError(errc)
                except requests.exceptions.Timeout as errt:     #raise error if the request gets timed out without receiving a single byte
                    raise TimeoutError(errt)
                except requests.exceptions.HTTPError as err:       #raise a general error if the above named errors are not triggered 
                    raise SystemExit(err)

            else:
                wrong_input = 'Wrong date input selection: date from cant be greater than date to, please try again' #print out an error message if the user chooses a date that is greater than input1's date 

    search_form= PriceSearchForm() #reset form data before passing everytime the page loads
    context = {
        'search_form': search_form,
        'price': bitcoin_price,
        'wrong_input':wrong_input,
        'date_to':to_date,
        'date_from':from_date,
        }

    return render(request, "btc/chart.html", context)
