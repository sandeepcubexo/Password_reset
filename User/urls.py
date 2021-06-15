from django.conf.urls import url
from .views import ChangePasswordView
from . import views
from django.urls import path, include
from User.views import Registerapi
urlpatterns = [
      path('Register/', Registerapi),
      path('Login/', views.Login.as_view(), name="api_auth"),
      path('change-password/', ChangePasswordView.as_view(), name='change-password'),
      path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),



]