from django.db.models import Q
from rest_framework import generics, mixins

from posting.models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

class BlogPostView(mixins.CreateModelMixin, generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        qs = BlogPost.objects.all()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
                ).distinct()
        return qs

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)


