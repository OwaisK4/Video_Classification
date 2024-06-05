from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from vertical.views import index, blog, blog_details

urlpatterns = [
    path('index/', index, name="index"),
    path('blog/', blog, name="blog"),
    path('blog-details/<slug:filename>/', blog_details, name="blog-details"),
    path('', blog),
] + static(settings.MEDIA_URL)