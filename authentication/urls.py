from django.urls import path
from .views import RegisterView, LoginAPIView, LogoutAPIView, SetNewPasswordAPIView, AccountSearchAPI, AccountView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('password/', SetNewPasswordAPIView.as_view(), name='password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/search/', AccountSearchAPI, name='search'),
    path('api/<username1>-<username2>/', AccountView, name="view"),
	#path('api/<username>/edit/', EditAccountView.as_view(), name="edit"),
]
