from django import forms


CHOICES = [("EUR", "EUR"), ("USD", "USD")]
UAH = [("UAH", "UAH"),]


class CalculatorForm(forms.Form):
    currency_from = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    currency_to = forms.ChoiceField(widget=forms.Select, choices=UAH)
    amount = forms.IntegerField()
