import requests
from datetime import date, timedelta
from .forms import PriceSearchForm

#function to get the current and today-10days dates respectively
class getApiService():
    def getCurrentDateView(self):
        datetime_today = date.today() #get current date
        date_today = str(datetime_today) #convert datetime class to string
        date_10daysago = str(datetime_today - timedelta(days=10)) #get date of today -10 days

        #assign 'date from' and 'date to' for chart template heading 
        date_from = date_10daysago 
        date_to = date_today

        return date_from,date_to

    #function to make the api get call and retrieve the default 10days api data.
    def makeDefaultApiCall(self, date_from, date_to):
        initial_data={'date_from':date_from,  #set initial 10 days date range as default input
                    'date_to':date_to,
        }
        search_form_default= PriceSearchForm(initial=initial_data)
        api= 'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + date_from + '&end=' + date_to + '&index=[USD]' 
        try:
            response = requests.get(api, timeout=2) #get api response data from coindesk based on date range supplied by user
            response.raise_for_status()              #raise error if HTTP request returned an unsuccessful status code.
            prices = response.json() #convert response to json format
            default_btc_price_range=prices.get("bpi") #filter prices based on "bpi" values only
        except requests.exceptions.ConnectionError as errc:  #raise error if connection fails
            raise ConnectionError(errc)
        except requests.exceptions.Timeout as errt:     #raise error if the request gets timed out without receiving a single byte
            raise TimeoutError(errt)
        except requests.exceptions.HTTPError as err:    #raise a general error if the above named errors are not triggered 
            raise SystemExit(err)

        return default_btc_price_range,search_form_default

    #function to confirm if valid date ranges have been supplied by the user.
    def getUserDateView(self, request):
        date_from = None
        date_to = None
        search_form= PriceSearchForm(request.POST or None) #get post request from the front end
        if request.method == 'POST': 
            if search_form.is_valid():  #Confirm if valid data was received from the form
                date_from = request.POST.get('date_from') #extract input 1 from submitted data
                date_to = request.POST.get('date_to') #extract input 2 from submitted data
            
            else:
                raise Http404("Invalid input")

        return date_from,date_to

    def userBtcDataChart(self, date_from, date_to, wrong_input):
        from_date= None
        to_date= None
        requested_btc_price_range= None

        initial_data={'date_from':date_from, 
                    'date_to':date_to,
                }
        search_form_current= PriceSearchForm(initial=initial_data) 

        api= 'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + date_from + '&end=' + date_to + '&index=[USD]' #use the 10days period obtained above to get dafualt 10days value
        if date_to > date_from:     #confirm that input2 is greater than input 1
            try:
                    response = requests.get(api, timeout=2) #get api response data from coindesk based on date range supplied by user
                    response.raise_for_status()        #raise error if HTTP request returned an unsuccessful status code.
                    response = requests.get(api) #get api response data from coindesk based on date range supplied by user
                    prices = response.json() #convert response to json format
                    requested_btc_price_range=prices.get("bpi") #filter prices based on "bpi" values only
                    from_date= date_from
                    to_date= date_to
            except requests.exceptions.ConnectionError as errc:  #raise error if connection fails
                raise ConnectionError(errc)
            except requests.exceptions.Timeout as errt:     #raise error if the request gets timed out without receiving a single byte
                raise TimeoutError(errt)
            except requests.exceptions.HTTPError as err:       #raise a general error if the above named errors are not triggered 
                raise SystemExit(err)

        else:
            wrong_input = 'Wrong date input selection: date from cant be greater than date to, please try again' #print out an error message if the user chooses a date that is greater than input1's date 

        return requested_btc_price_range, from_date, to_date , wrong_input, search_form_current
