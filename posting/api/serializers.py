from rest_framework import serializers

from posting.models import BlogPost



class BlogPostSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['pk', 'title', 'content', 'timestamp', 'uri']

    def get_uri(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(f"The title '{value}' already exist")
        return value
