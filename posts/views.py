from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404, \
    RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from utils.decorators import method_permission_classes
from posts.permissions import IsOwnerOrAdmin


class ListCreateAPI(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def __init__(self):
        self.user = None
        super().__init__()

    @method_permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        self.user = request.user
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer: PostSerializer):
        serializer.save(writer=self.user)


class SinglePostAPI(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @method_permission_classes([IsAuthenticated, IsOwnerOrAdmin])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @method_permission_classes([IsAuthenticated, IsOwnerOrAdmin])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed('patch')


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        post.likes.get_or_create(
            user=request.user
        )

        return Response({"result": "success"})

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        try:
            post.likes.get(user=request.user).delete()
        except:
            pass
        return Response({"result": "success"})


class CommentAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def __init__(self):
        self.user = None
        super().__init__()

    def post(self, request, *args, **kwargs):
        self.user = request.user
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(writer=self.user)


class SingleCommentAPIView(RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault("replies", True)
        return super().get_serializer(*args, **kwargs)

    @method_permission_classes([IsAuthenticated, IsOwnerOrAdmin])
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)