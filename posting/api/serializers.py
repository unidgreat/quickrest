from rest_framework import serializers

from posting.models import BlogPost



class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['pk', 'title', 'content', 'timestamp']

    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(f"The title '{value}' already exist")
        return value
