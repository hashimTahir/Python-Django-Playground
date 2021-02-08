from django import forms
from django.db.models import fields
from blog.models import BlogPost


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model=BlogPost
        fields= ['title','body','image']