from django.db import models
from django.urls import reverse


class Post(models.Model):
    """
    this is class to create post
    """

    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250)
    content = models.TextField()
    status = models.BooleanField()
    catgory = models.ForeignKey(
        "Catgory", on_delete=models.SET_NULL, null=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_snippet(self):
        return self.content[0:5]

    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})


"""
this class for make a catgory
"""


class Catgory(models.Model):
    # this Class is for creating catgory
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name
