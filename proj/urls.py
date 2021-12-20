
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from api.views import GetPostsViewSet, MyTokenObtainPairView, createPost, deletePost, updatePost
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions, views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', MyTokenObtainPairView.as_view(), name="login"),
    path('posts/', GetPostsViewSet.as_view(), name="get_posts"),
    path('post/create/', createPost.as_view(), name="create_post"),
    path('post/delete/<str:pk>/', deletePost, name='delete_post'),
    path('post/update/<str:pk>/', updatePost, name='update_post'),
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger',
        cache_timeout=0), name='schema-swagger-ui'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
