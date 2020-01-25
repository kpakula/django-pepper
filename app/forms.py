from django import forms
from app.models import CustomLogin
from django import forms
class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomLogin
        fields = ['username', 'password', ]
        widgets = {
            'password': forms.PasswordInput(),
        }