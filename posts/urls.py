from django.urls import path

from posts.views import *

urlpatterns = [
    path('', ListCreateAPI.as_view(), name='posts'),
    path('<int:pk>/', SinglePostAPI.as_view(), name='post'),
    path('<int:pk>/like/', LikeAPIView.as_view(), name='post_like'),
]