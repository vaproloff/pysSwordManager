from django.urls import path
from .views import password_list, password_detail, edit_password, delete_password, create_password

urlpatterns = [
    path('', password_list, name='password_list'),
    path('<int:entry_id>/', password_detail, name='password_detail'),
    path('<int:entry_id>/edit/', edit_password, name='edit_password'),
    path('<int:entry_id>/delete/', delete_password, name='delete_password'),
    path('new/', create_password, name='create_password'),
]