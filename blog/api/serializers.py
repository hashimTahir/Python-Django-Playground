from rest_framework import serializers

from blog.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image', 'date_updated']

    # https://www.django-rest-framework.org/
    # There are two type of serilizers. General and model.
    # general serilizers are much more customizable.
    # The ModelSerializer class provides a shortcut that lets you
    #  automatically create a Serializer class with fields that correspond to the Model fields.
