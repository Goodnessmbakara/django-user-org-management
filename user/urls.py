from django.urls import path
from .views import RegisterView, LoginView, UserView

urlpatterns = [
    path('api/auth/register', RegisterView.as_view(), name='register'),
    path('api/auth/login', LoginView.as_view(), name='login'),
    path('api/users/<int:userId>', UserView.as_view(), name='user-detail'),
]
