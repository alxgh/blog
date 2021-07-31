from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path

from account.views import *

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', GetMeAPI.as_view(), name='get_me'),
    path('<int:pk>/', FetchUpdateUserAPI.as_view(), name='get_me'),
    path('', GetUserListAPI.as_view(), name='get_me')
]