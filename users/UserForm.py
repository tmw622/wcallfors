from django import forms
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username=forms.CharField(label='username',max_length=100,required=True)
    userpwd=forms.CharField(label='password',max_length=100,required=True, widget=forms.PasswordInput)
    captcha=CaptchaField()
