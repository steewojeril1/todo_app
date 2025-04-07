from django import forms
from todoweb.models import Todo 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model # this will return value in AUTH_USER_MODEL in settings

class RegistrationForm(UserCreationForm ):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=get_user_model()
        fields=['first_name','last_name','email','username','password1','password2']


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'completed'] # exclude=('user','created_by)
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'})
        }
