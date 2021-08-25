from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.registration_view, name='signup'),
    path('signin/', views.login_view, name='signin'),
    path('signout/', views.logout_request, name='signout'),
    path('authenticate/', views.must_authenticate_view, name='authenticate'),
    path('profile/', views.account_view, name='profile'),
    path('verify/', views.verification_view, name='verify')
]