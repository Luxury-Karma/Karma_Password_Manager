from django.urls import path
from . import views

urlpatterns = [
    path('password_manager/', views.members, name='karma_little_password_manager'),
]
