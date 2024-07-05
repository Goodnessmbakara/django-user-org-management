from django.urls import path
from .views import RegisterView, LoginView, UserView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('api/users/<uuid:id>', UserView.as_view(), name='user-detail'),
]
