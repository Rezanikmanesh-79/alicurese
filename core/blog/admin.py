from django.contrib import admin
from .models import Post, Catgory


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "image",
        "title",
        "content",
        "status",
        "catgory",
        "created_date",
        "updated_date",
        "published_date",
    ]


admin.site.register(Post, PostAdmin)
admin.site.register(Catgory)
