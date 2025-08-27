from rest_framework import serializers
from .models import Post


class PostListSerializer(serializers.ModelSerializer):
    """Serializer for list view - includes snippet"""
    snippet = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'snippet', 'created_at', 'updated_at']


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer for detail view - includes full content"""
    snippet = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'content', 'rendered_html', 'created_at', 'updated_at']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for create/update operations"""
    
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def validate_content(self, value):
        """Validate that content is a list of content blocks"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Content must be a list of content blocks")
        
        # Basic validation of content structure
        for block in value:
            if not isinstance(block, dict):
                raise serializers.ValidationError("Each content block must be a dictionary")
            if 'type' not in block:
                raise serializers.ValidationError("Each content block must have a 'type' field")
        
        return value 