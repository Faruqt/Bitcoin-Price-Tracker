from django import forms

class PriceSearchForm(forms.Form):
        date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': '2021-09-08', 'max': '2021-09-17'}))
        date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': '2021-09-08', 'max': '2021-09-17'}))
