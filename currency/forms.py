from django import forms

from .models import Calculator


class CalculatorForm(forms.ModelForm):
    class Meta:
        model = Calculator
        fields = ["currency_from", "currency_to", "amount"]
