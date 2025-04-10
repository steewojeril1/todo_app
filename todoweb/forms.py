from django import forms
from todoweb.models import Todo 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model # this will return value in AUTH_USER_MODEL in settings

class RegistrationForm(UserCreationForm ):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'})) # password1 and password2 are just form fields, not model fields
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'})) # So we must style them separately outside the Meta class
    class Meta:
        model=get_user_model()
        fields=['first_name','last_name','email','username','password1','password2'] # this form is created here to add this. else we can directly use UserCreationForm
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),               # Only model fields
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
        '''
        The default UserCreationForm only includes:
        username
        password1
        password2
        '''


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
