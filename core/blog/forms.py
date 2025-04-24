from django import forms
from .models import Post


class ContactForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "status", "catgory", "published_date"]
