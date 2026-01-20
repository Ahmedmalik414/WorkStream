from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('toggle/<int:pk>/', views.toggle_task, name='toggle_task'),
    
    # Auth URLs
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('delete-selected/', views.delete_selected_tasks, name='delete_selected'),
]