from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView


app_name = "blog"
urlpatterns = [
    path("api/v1/", include("blog.api.v1.urls")),
    path("post/", views.PostlistView.as_view(), name="post-list"),
    path(
        "post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"
    ),
    path("post/create/", views.PostcreatView.as_view(), name="create-post"),
    path(
        "post/<int:pk>/edit", views.PostEditeView.as_view(), name="edit-post"
    ),
    path(
        "post/<int:pk>/delete",
        views.PostDeleteView.as_view(),
        name="edit-delete",
    ),
    path("Api-base-list/", TemplateView.as_view(template_name="api_base.html")),
    # path("about_fbv/", views.index_view, name="fbv-test"),
    # path('post/', views.api_post_view, name="post"),
    path("about_cbv/", views.IndexView.as_view(), name="index"),
    # path("go-to-index/<int:pk>/", views.RedirectToMaktabkoonehView.as_view(),
    #     name = "redirect_to_maktabkhooneh"),
    # path("about_cbv/", TemplateView.as_view(template_name="index.html",
    #                                          extra_context={"name": "reza"})),
    # # path("go-to-index/", RedirectView.as_view(
    #    pattern_name="cbv-test", name="redirect")),
]
