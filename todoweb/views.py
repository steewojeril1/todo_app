from django.shortcuts import render, redirect

from todoweb.models import Todo
from django.views.generic import View
from todoweb.forms import TodoForm, LoginForm, CustomSignupForm
from todoweb.decorators import sign_in_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model # this will return value in AUTH_USER_MODEL in settings

class SignupView(View):
    def get(self, request, *args, **kwargs):
        form = CustomSignupForm()  # custom form, or use UserCreationForm
        '''
        The default UserCreationForm only includes:
        username
        password1
        password2
        to include first_name,last_name,email we need to create a form -that is CustomSignupForm  
        '''
        return render(request, "todo/signup.html", {'form': form})
        
    def post(self, request, *args, **kwargs):
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Secure: Hashes the password automatically # written inside UserCreationForm
            login(request, user)  # automatically logs in the new user
            messages.success(request, 'Your profile has been created and you are now logged in!')
            return redirect('todo_list') 
        else:
            messages.error(request, 'Something went wrong. Please check the form.')
            return render(request, 'todo/signup.html', {'form': form})


class CustomLoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'todo/custom_login.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid(): #It checks if all required fields are filled out correctly based on your model's rules.
            username=form.cleaned_data.get('username')  #cleaned_data is the validated data
            password=form.cleaned_data.get('password')# use cleaned_data if we are using regular forms (not model forms)(if we want to access individual form field values without necessarily saving the model.)
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                print('user:::',request.user)
                messages.success(request,'You have been successfully Logged in. Welcome %s' %request.user)
                return redirect('todo_list')
            else:
                messages.error(request,'Incorrect username/password')
                return render(request,'todo/custom_login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('custom_login')


@method_decorator(sign_in_required, name='dispatch')
class TodoCreateView(View):
    def get(self, request, *args, **kwargs):  # when the user opens the form page
        form = TodoForm()
        return render(request, 'todo/todo_form.html',{'form':form})
    def post(self, request, *args, **kwargs): # when the user submits the form 
        form = TodoForm(request.POST)
        if form.is_valid(): #It checks if all required fields are filled out correctly based on your model's rules.
            todo = form.save(commit=False) #used when modelform is used.(If normal form, we need to take each data from cleaned_Data and explicitly create object with that)
            '''
             # You manually create the model instance
                todo = Todo.objects.create(
                title=title,
                description=description,
                user=request.user  # add extra fields manually
            )
            '''
            todo.user = request.user
            todo.save()
            messages.success(self.request,'Your todo has been added!!!')
            return redirect('todo_list')

@method_decorator(sign_in_required, name='dispatch')
class TodoList(View):
    def get(self, request, *args, **kwargs): 
        filter_type = self.request.GET.get('filter', 'all')
        if filter_type == 'completed':
            todos =  Todo.objects.filter(user=self.request.user, completed=True).order_by('-created_at')
        elif filter_type == 'incompleted':
            todos =   Todo.objects.filter(user=self.request.user, completed=False).order_by('-created_at')
        else:
            todos = Todo.objects.filter(user=request.user).order_by('completed', '-created_at')
        return render(request, 'todo/todo_list.html',{'todos':todos, 'count':todos.count(), 'filter':filter_type})
@method_decorator(sign_in_required, name='dispatch')
class TodoUpdateView(View):
    def get(self, request, *args, **kwargs): 
        pk=kwargs.get('pk') 
        todo = Todo.objects.get(pk=pk, user=request.user) #can also use id=pk
        form = TodoForm(instance=todo)
        return render(request, 'todo/todo_form.html',{'form':form})
    def post(self, request, *args, **kwargs): 
        pk=kwargs.get('pk') 
        todo = Todo.objects.get(pk=pk, user=request.user)
        form = TodoForm(request.POST, instance=todo) # instance = todo is given because to edit in that particular todo. else it will create new todo when calling form.save()
        if form.is_valid(): 
            form.save()
            print("entered",request.user)
            return redirect('todo_list')
            
@method_decorator(sign_in_required, name='dispatch')
class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        todo=Todo.objects.get(pk=pk)
        return render(request,'todo/todo_detail.html',{'todo':todo})
        
@sign_in_required
def delete_todo(request, *args, **kwargs):
    pk =kwargs.get('pk')
    todo=Todo.objects.get(id=pk)
    if request.method == 'POST':
        todo.delete()
        messages.success(request,'Your todo has been deleted')
        return redirect('todo_list')
    return render(request, 'todo/todo_delete.html', {'todo':todo})
