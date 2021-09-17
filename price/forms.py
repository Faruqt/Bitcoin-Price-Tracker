from django import forms

class PriceSearchForm(forms.Form):
        date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': '2021-09-07', 'max': '2021-09-16'}))
        date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': '2021-09-07', 'max': '2021-09-16'}))
