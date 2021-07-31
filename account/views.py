import json

from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import HttpResponse

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from account.permissions import IsOwnerOrReadOnly
from account.serializers import RegisterSerializer, UserSerializer, UpdateSerializer
from utils.decorators import validate_serializer_data


class RegisterAPI(APIView):
    @validate_serializer_data(RegisterSerializer)
    def post(self, request: Request):
        request.serializer.create(request.valid_data)
        return Response({
            "success": True
        })


class GetMeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request):
        serializer = UserSerializer(data=model_to_dict(request.user))
        serializer.is_valid()

        return Response(serializer.data)


class GetUserListAPI(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FetchUpdateUserAPI(RetrieveAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @validate_serializer_data(UpdateSerializer)
    def patch(self, request, *args, **kwargs):
        obj = self.get_object()
        print(request.valid_data)
        request.serializer.update(obj, request.valid_data)

        serializer = UserSerializer(data=model_to_dict(obj))
        serializer.is_valid()

        return Response(serializer.data)


