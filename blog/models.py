from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete,pre_save
from django.dispatch import receiver


def upload_location(instance, filename):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author_id), title=str(instance.title), filename=filename
    )
    return file_path


class BlogPost(models.Model):
    title = models.CharField(max_length=50, null=False, blank=True)
    body = models.TextField(max_length=6000, null=False, blank=True)
    image = models.ImageField(
        upload_to=upload_location, null=False, blank=True)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="Date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="Date updated")

    # Link it to the User model table
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title


# If a blog post is deleted also delete the image associated with it.
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)



def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(
            instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)
