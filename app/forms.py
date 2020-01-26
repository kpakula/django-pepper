from django import forms
from app.models import CustomLogin, Offer
from django import forms
from bootstrap_datepicker_plus import DatePickerInput
class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomLogin
        fields = ['username', 'password', ]
        widgets = {
            'password': forms.PasswordInput(),
        }

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ['user', 'date_published']
        widgets = {
            'date_start': DatePickerInput(format='%Y-%m-%d'),
            'date_end': DatePickerInput(format='%Y-%m-%d'), 
        }