from django import forms
from app.models import CustomLogin

class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomLogin
        fields = ['post', 'post2', ]