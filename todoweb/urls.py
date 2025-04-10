from django.urls import path
from todoweb import views
urlpatterns = [
    path('signup',views.SignupView.as_view(),name='signup'),
    path('todos/create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('todos/list/', views.TodoList.as_view(), name='todo_list'),
    path('todos/list/completed/', views.TodoList.as_view(),{'filter':'completed'}, name='completed_todos'),
    path('todos/list/incompleted/', views.TodoList.as_view(), {'filter':'incompleted'}, name='incompleted_todos'),
    path('todos/detail/<int:pk>', views.TodoDetailView.as_view(), name='todo_detail'),
    path('todos/edit/<int:pk>', views.TodoUpdateView.as_view(), name='todo_update'),
    path('todos/delete/<int:pk>', views.delete_todo, name='todo_delete'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.CustomLoginView.as_view(), name='custom_login')
]
