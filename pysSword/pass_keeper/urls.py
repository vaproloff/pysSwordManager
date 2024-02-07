from django.urls import path
from .views import (
    password_list,
    edit_password,
    delete_password,
    create_password,
    get_password,
)

urlpatterns = [
    path('', password_list, name='password_list'),
    path('<int:entry_id>/edit/', edit_password, name='edit_password'),
    path('<int:entry_id>/delete/', delete_password, name='delete_password'),
    path('new/', create_password, name='create_password'),
    path('get/<int:entry_id>/', get_password, name='get_pass_api'),
]
