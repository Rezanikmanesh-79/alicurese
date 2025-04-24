from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    RedirectView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import get_object_or_404
from .models import Post
from .forms import ContactForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.http import HttpResponse


"""
def index_view(request):
    function base view to show index
    name = "reza"
    return render(request, "index.html", {
        "name": name})
"""


class IndexView(TemplateView):
    """class base view to show index"""

    permission_required = "blog.view_post"
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "ali"
        context["posts"] = Post.objects.all()
        return context


"""
FBV for redirect

from django.shortcuts import redirect
def redirect_to_maktab(request):
    return redirect("https://maktabkhooneh.org/")

"""


class RedirectToMaktabkoonehView(
    LoginRequiredMixin, PermissionRequiredMixin, RedirectView
):
    permission_required = "blog.view_post"
    url = "https://maktabkhooneh.org/"

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["pk"])
        print(post)
        return super().get_redirect_url(*args, **kwargs)


class PostlistView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "blog.view_post"
    model = Post
    # queryset = Post.objects.all()
    paginate_by = 2
    ordering = "-id"
    # def get_queryset(self):
    #     posts = Post.objects.filter(status=True)
    #     return posts
    context_object_name = "Posts"


class PostDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    permission_required = "blog.view_post"
    # adding post detail
    model = Post


"""
class PostcreatView(FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = '/bloge/post/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
"""


class PostcreatView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "blog.view_post"
    # model = Post
    # fields = ['author', 'title', 'content', 'status', 'catgory', 'published_date']
    form_class = ContactForm
    template_name = "blog/post_form.html"
    success_url = "/bloge/post/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostEditeView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "blog.view_post"
    model = Post
    form_class = ContactForm
    success_url = "/bloge/post/"


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "blog.view_post"
    model = Post
    success_url = "/bloge/post/"
