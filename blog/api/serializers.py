from blog.models import BlogPost
from rest_framework import serializers
import cv2
import sys
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2  # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50


class BlogPostSerializer(serializers.ModelSerializer):

    # as mentioned in docs. get_username_from_author is the method name
    username = serializers.SerializerMethodField('get_username_from_author')
    image = serializers.SerializerMethodField('validate_image_url')

    class Meta:
        model = BlogPost
        fields = ['pk', 'title', 'slug', 'body',
                  'image', 'date_updated', 'username']

    def get_username_from_author(self, blog_post):
        username = blog_post.author.username
        return username

        # Validate the image url incase of production. E.g. aws attaches
        # some signature after the image url. making it inaccessable in mob
        # app. Remove anything after the ?

    def validate_image_url(self, blog_post):
        image = blog_post.image
        new_url = image.url
        if "?" in new_url:
            new_url = image.url[:image.url.rfind("?")]
        return new_url


class BlogPostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'image']

    def validate(self, blog_post):
        try:
            title = blog_post['title']
            if len(title) < MIN_TITLE_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a title longer than " + str(MIN_TITLE_LENGTH) + " characters."})

            body = blog_post['body']
            if len(body) < MIN_BODY_LENGTH:
                raise serializers.ValidationError(
                    {"response": "Enter a body longer than " + str(MIN_BODY_LENGTH) + " characters."})

            image = blog_post['image']
            url = os.path.join(settings.TEMP, str(image))
            storage = FileSystemStorage(location=url)

            with storage.open('', 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
                destination.close()

            if sys.getsizeof(image.file) > IMAGE_SIZE_MAX_BYTES:
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "That image is too large. Images must be less than 2 MB. Try a different image."})

            img = cv2.imread(url)
            dimensions = img.shape  # gives: (height, width, ?)

            aspect_ratio = dimensions[1] / dimensions[0]  # divide w / h
            if aspect_ratio < 1:
                os.remove(url)
                raise serializers.ValidationError(
                    {"response": "Image height must not exceed image width. Try a different image."})

            os.remove(url)
        except KeyError:
            pass
        return blog_post

    # https://www.django-rest-framework.org/
    # There are two type of serilizers. General and model.
    # general serilizers are much more customizable.
    # The ModelSerializer class provides a shortcut that lets you
    #  automatically create a Serializer class with fields that correspond to the Model fields.
