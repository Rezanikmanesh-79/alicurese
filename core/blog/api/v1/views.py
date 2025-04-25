from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer, CatgorySerializer
from blog.models import Post, Catgory
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import CustomPagination

data = {
    "id": 1,
    "title": "hello",
}

# v0
# @api_view(['GET', "POST"])
# @permission_classes([IsAuthenticated])
# def api_post_list_view(request):
#     if request.method == "GET":
#         posts=Post.objects.all()
#         # posts=Post.objects.filter(status=True)
#         srializer=PostSerializer(posts,many=True)
#         return Response(srializer.data)
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
# -----------------------------------------------------------
# @api_view(['GET', "PUT","DELETE"])
# def api_post_detail_view(request,id):
#     post=get_object_or_404(Post,pk=id,status=True)
#     if request.method == "GET":
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     elif request.method =="PUT":
#         serializer = PostSerializer(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response (serializer.data)
#     elif request.method == "DELETE":
#         post.delete()
#         return Response({"detail": "item removed susses"})

# v1
# class PostListView(APIView):

#     permission_classes =[IsAuthenticated]
#     serializer_class=PostSerializer

#     def get(self, request):
#         posts = Post.objects.all()
#         # posts=Post.objects.filter(status=True)
#         srializer = PostSerializer(posts, many=True)
#         return Response(srializer.data)
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
# ------------------------------------------------------------------
# class PostDetailView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

#     def get_object(self, id):
#         return get_object_or_404(Post, pk=id, status=True)

#     def get(self, request, id):
#         post = self.get_object(id)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)

#     def put(self, request, id):
#         post = self.get_object(id)
#         serializer = self.serializer_class(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, id):
#         post = self.get_object(id)
#         post.delete()
#         return Response({"detail": "Item removed successfully"})


# v2
# class PostListView (GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset=Post.objects.all()
#     serializer_class=PostSerializer
#     permission_classes=[IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post (self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# ------------------------------------------------------------------------------
# class PostDetailView(GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=True)

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

# v3 View set
# _________________________________________________
# class PostListView (ListCreateAPIView):
#     permission_classes=[IsAuthenticated]
#     serializer_class=PostSerializer
#     queryset=Post.objects.all()

# class PostDetailView(RetrieveUpdateDestroyAPIView):
#     permission_classes=[IsAuthenticated]
#     serializer_class=PostSerializer
#     queryset=Post.objects.filter(status=True)

# # view set example
# class PostViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#     queryset =Post.objects.filter(status=True)

#     def list(self, request):
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#             post_object = get_object_or_404(self.queryset, pk=pk)
#             serializer=self.serializer_class(post_object)
#             return Response(serializer.data)


#     def create(self, request):
#         pass


#     def update(self, request, pk=None):
#         pass

#     def partial_update(self, request, pk=None):
#         pass

#     def destroy(self, request, pk=None):
#         pass


class PostModelViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    @action(methods=["get"], detail=False)
    def get_ok(self, request):
        return Response({"detail": "ok"})

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = {
        "catgory": ["exact", "in"],
        "author": ["exact"],
        "status": ["exact"],
    }
    search_fields = ["title", "content"]
    ordering_fields = ["created_date"]
    pagination_class = CustomPagination


class CatgoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CatgorySerializer
    queryset = Catgory.objects.all()
