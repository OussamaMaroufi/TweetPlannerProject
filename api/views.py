from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django_filters import DateTimeFilter, FilterSet
from django_filters.filters import BooleanFilter, ChoiceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.fields import ChoiceField
from proj.pagination import CustomPagination
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import (api_view, parser_classes,
                                       permission_classes)
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Post

from .serializers import (PostSerializer, UserSerializer,
                          UserSerializerWithToken)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# create post
class createPost(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    # use formparser to support many html form data

    def post(self, request, format=None):
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostFilter(FilterSet):

    isPublished = BooleanFilter(method='filter_published')
    topic =ChoiceFilter(choices=Post.TOPICS_CHOICES)

    class Meta:
        model = Post
        fields = {
            'isPublished': ['exact'],
        }

    def filter_published(self, queryset, name, value):
        print(name, value)
        return queryset.filter(isPublished=value)


class GetPostsViewSet(ListAPIView):
    filterset_class = PostFilter
    serializer_class = PostSerializer
    model = Post
    queryset = Post.objects.all().order_by('-date_created')
    pagination_class = CustomPagination



# Delete post view
@api_view(['DELETE'])
@permission_classes([AllowAny])
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return Response('Producted Deleted')


# Update post view
@api_view(['PUT'])
@permission_classes([AllowAny])
def updatePost(request, pk):
    data = request.data
    post = Post.objects.get(id=pk)

    post.content = data['content']
    post.topic = data['topic']
    if 'postImage' in data:
        post.postImage = data['postImage']
    else:
        post.postImage = None
    post.postTime = data['postTime']

    post.save()
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)
