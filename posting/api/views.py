from rest-framework import generics
from posting.models import BlogPost

class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = pk
    query_set = BlogPost.objects.all()