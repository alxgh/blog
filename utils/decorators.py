import functools
from typing import Type

from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer


def validate_serializer_data(serializer_class: Type[Serializer]):
    """
    Pass body to a serializer and validate the data. if data is invalid return a 422 response.
    """
    def validate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = args[1]
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                request.valid_data = serializer.data
                request.serializer = serializer
                return func(*args, **kwargs)
            else:
                return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return wrapper
    return validate
