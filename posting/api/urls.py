
from django.conf.urls import url
# from django.urls import path
from .views import BlogPostRudView, BlogPostView

app_name = 'api-posting'

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(), name='post-rud'),
    url(r'^$', BlogPostView.as_view(), name='postings'),
]
