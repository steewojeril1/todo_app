from django import forms
from todoweb.models import Todo 

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
