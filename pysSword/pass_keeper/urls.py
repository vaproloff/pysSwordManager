from django.urls import path
from .views import password_list, password_detail, create_password

urlpatterns = [
    path('', password_list, name='password_list'),
    path('<int:entry_id>/', password_detail, name='password_detail'),
    path('new/', create_password, name='create_password'),
]