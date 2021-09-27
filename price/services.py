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
        PriceFormSearch = initialData(date_from, date_to) #call the initial data function and append the values to the search form
        search_form_default= PriceFormSearch

        return search_form_default

class getUserInputDateRange():
    def userFormInputView(self, date_from, date_to, date_today):
        if date_to > date_today:   #if the date to from input is greater than today's date; there wont be data for the extra days, so we change the 'date_to' input back to todays's date
            date_to = date_today
        PriceFormSearch = initialData(date_from, date_to)
        search_form_current= PriceFormSearch  #when the page reloads, set the default form date input values to the dates picked by the user

        return  search_form_current
class outOfRange():
    def ooR(self, date_from, date_to, range_error):
        from_date= datetime.strptime(date_from, '%Y-%m-%d').date()
        to_date= datetime.strptime(date_to, '%Y-%m-%d').date()

        if from_date < (to_date - timedelta(days=90)):   #check if the date range is not greater than 3 months
            range_error= 'No more than 3 months data can be displayed'

        PriceFormSearch = initialData(date_from, date_to)
        search_form_values= PriceFormSearch

        return date_from, date_to, range_error, search_form_values

def initialData(date_from, date_to):  #initial data function to render our date inputs out with chosen value
    initial_data={'date_from':date_from,   
                    'date_to':date_to,
                }
    PriceForm = PriceSearchForm(initial=initial_data) #append the date_from and date_to values to the search form

    return PriceForm
