import requests
from datetime import date, timedelta , datetime
from .forms import PriceSearchForm

#function to get the current and today-10days dates respectively
class getDateService():
    def getCurrentDateView(self):
        datetime_today = date.today() #get current date
        date_today = str(datetime_today) #convert datetime class to string
        date_10daysago = str(datetime_today - timedelta(days=10)) #get date of today -10 days

        #assign 'date from' and 'date to' for chart template heading 
        date_from = date_10daysago 
        date_to = date_today

        return date_from,date_to

    #function to make the api get call and retrieve the default 10days api data.
class getDefaultData():
    def makeDefaultApiView(self, date_from, date_to):
        initial_data={'date_from':date_from,  #set initial 10 days date range as default input
                    'date_to':date_to,
        }
        search_form_default= PriceSearchForm(initial=initial_data)
        api= 'https://api.coindesk.com/v1/bpi/historical/close.json?start=' + date_from + '&end=' + date_to + '&index=[USD]' 
        try:
            response = requests.get(api, timeout=5) #get api response data from coindesk based on date range supplied by user
            response.raise_for_status()              #raise error if HTTP request returned an unsuccessful status code.
            prices = response.json() #convert response to json format
            default_btc_price_range=prices.get("bpi") #filter prices based on "bpi" values only
        except requests.exceptions.ConnectionError as errc:  #raise error if connection fails
            raise ConnectionError(errc)
        except requests.exceptions.Timeout as errt:     #raise error if the request gets timed out after 10 seconds without receiving a single byte
            raise TimeoutError(errt)
        except requests.exceptions.HTTPError as err:    #raise a general error if the above named errors are not triggered 
            raise SystemExit(err)

        return default_btc_price_range,search_form_default

class getUserInputDateRange():
    def userFormInputView(self, date_from, date_to, date_today):
        if date_to > date_today:   #if the date to from input is greater than today's date; there wont be data for the extra days, so we change the 'date_to' input back to todays's date
            date_to = date_today
        initial_data={'date_from':date_from,   
                    'date_to':date_to,
                }
        search_form_current= PriceSearchForm(initial=initial_data)  #when the page reloads, set the default form date input values to the dates picked by the user

        return  search_form_current
class outOfRange():
    def ooR(self, date_from, date_to, range_error):
        from_date= datetime.strptime(date_from, '%Y-%m-%d').date()
        to_date= datetime.strptime(date_to, '%Y-%m-%d').date()

        if from_date < (to_date - timedelta(days=90)):   #check if the date range is not greater than 3 months
            range_error= 'No more than 3 months data can be displayed'

        return range_error
