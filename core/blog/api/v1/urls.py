from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter, DefaultRouter

app_name = "api-v1"
router = DefaultRouter()
# normal view set
# router.register(r'post', views.PostViewSet, basename='post')
# model view set

router.register(r"post", views.PostModelViewSet, basename="post")
router.register(r"catgory", views.CatgoryModelViewSet, basename="catgory")
urlpatterns = router.urls

# urlpatterns = [
#     # path('post/', views.api_post_list_view, name="post"),
#     # path('post/<int:id>/', views.api_post_detail_view, name="post"),
#     #path('post/<int:id>/', views.api_post_detail_view, name="post"),
#     # path('post/', views.PostListView.as_view(), name="post"),
#     # path('post/<int:pk>/', views.PostDetailView.as_view(), name="post_detail"),
#     # path('post/', views.PostViewSet.as_view({'get': 'list','post':'create'}), name="post"),
#     # path('post/<int:pk>/', views.PostViewSet.as_view({
#     # 'get': 'retrieve',
#     # 'put': 'update',
#     # 'patch': 'partial_update',
#     # 'delete': 'destroy'
#     # }), name="post_detail"),
#     # using router in url
#     path('', include(router.urls)),
# ]
