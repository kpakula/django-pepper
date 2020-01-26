from django import forms
from app.models import CustomLogin, Offer
from django import forms
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
        fields = '__all__'