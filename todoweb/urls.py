from django.urls import path
from todoweb import views
urlpatterns = [
    path('create/', views.TodoCreateView.as_view(), name='todo_create'),
    path('list/', views.TodoList.as_view(), name='todo_list'),
    path('list/completed/', views.TodoList.as_view(),{'filter':'completed'}, name='completed_todos'),
    path('list/incompleted/', views.TodoList.as_view(), {'filter':'incompleted'}, name='incompleted_todos'),
    path('detail/<int:pk>', views.TodoDetailView.as_view(), name='todo_detail'),
    path('edit/<int:pk>', views.TodoUpdateView.as_view(), name='todo_update'),
    path('delete/<int:pk>', views.delete_todo, name='todo_delete'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='custom_login')
]
