from django.urls import path
from todoapi import views
urlpatterns=[
    path('todos/', views.TodoListCreate.as_view(), name='api_todo_list_create'),
    path('signup/', views.SignupView.as_view(), name='api_signup'),
    path('todos/<int:pk>/', views.TodoDetail.as_view(), name='api_todo_detail'),

]