from django.urls import path
from blog.views import (
    create_blog_view,
    detail_blog_view,
)

# whenever an app is created which has its own urls, app_name
# parameter must be added. apps urls, required by django
app_name = 'blog'

urlpatterns = [
    path('create', create_blog_view, name="create"),
    path('<slug>/', detail_blog_view, name="detail"),
]
