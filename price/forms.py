from django import forms

class PriceSearchForm(forms.Form):
        date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
