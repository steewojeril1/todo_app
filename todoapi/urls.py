from django.urls import path
from todoapi import views
urlpatterns=[
    path('todos/', views.TodoListCreate.as_view(), name='api-todo-list-create'),
    path('signup/', views.SignupView.as_view(), name='api-signup')

]