from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostListCreateView(generics.ListCreateAPIView):
    """List all posts with pagination and create new posts"""
    queryset = Post.objects.all()
    pagination_class = StandardResultsSetPagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostListSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create post with content
        post = serializer.save()
        
        # Generate rendered HTML from content
        post.rendered_html = self._render_content_to_html(post.content)
        post.save()
        
        # Return full post details
        detail_serializer = PostDetailSerializer(post)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
    
    def _render_content_to_html(self, content):
        """Convert structured content to HTML"""
        if not content:
            return ""
        
        html_parts = []
        for block in content:
            block_type = block.get('type', 'paragraph')
            content_text = block.get('content', '')
            
            if block_type == 'heading1':
                html_parts.append(f'<h1>{content_text}</h1>')
            elif block_type == 'heading2':
                html_parts.append(f'<h2>{content_text}</h2>')
            elif block_type == 'paragraph':
                # Handle inline formatting
                formatted_text = self._apply_inline_formatting(content_text)
                html_parts.append(f'<p>{formatted_text}</p>')
            elif block_type == 'bullet_list':
                items = block.get('items', [])
                list_html = '<ul>'
                for item in items:
                    formatted_item = self._apply_inline_formatting(item)
                    list_html += f'<li>{formatted_item}</li>'
                list_html += '</ul>'
                html_parts.append(list_html)
            elif block_type == 'numbered_list':
                items = block.get('items', [])
                list_html = '<ol>'
                for item in items:
                    formatted_item = self._apply_inline_formatting(item)
                    list_html += f'<li>{formatted_item}</li>'
                list_html += '</ol>'
                html_parts.append(list_html)
            elif block_type == 'code_block':
                code_content = block.get('content', '')
                language = block.get('language', '')
                html_parts.append(f'<pre><code class="language-{language}">{code_content}</code></pre>')
            elif block_type == 'blockquote':
                quote_text = self._apply_inline_formatting(content_text)
                html_parts.append(f'<blockquote>{quote_text}</blockquote>')
        
        return '\n'.join(html_parts)
    
    def _apply_inline_formatting(self, text):
        """Apply inline formatting (bold, italic, links) to text"""
        if not text:
            return ""
        
        # Simple inline formatting - in a real app you'd use a proper markdown parser
        # This is a basic implementation for demo purposes
        formatted_text = text
        
        # Handle bold (wrapped in **)
        import re
        formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_text)
        
        # Handle italic (wrapped in *)
        formatted_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_text)
        
        # Handle links [text](url)
        formatted_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', formatted_text)
        
        return formatted_text


class PostDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a post by slug"""
    queryset = Post.objects.all()
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Update post
        post = serializer.save()
        
        # Regenerate rendered HTML
        post.rendered_html = self._render_content_to_html(post.content)
        post.save()
        
        # Return updated post
        detail_serializer = PostDetailSerializer(post)
        return Response(detail_serializer.data)
    
    def _render_content_to_html(self, content):
        """Convert structured content to HTML (same as in PostListCreateView)"""
        if not content:
            return ""
        
        html_parts = []
        for block in content:
            block_type = block.get('type', 'paragraph')
            content_text = block.get('content', '')
            
            if block_type == 'heading1':
                html_parts.append(f'<h1>{content_text}</h1>')
            elif block_type == 'heading2':
                html_parts.append(f'<h2>{content_text}</h2>')
            elif block_type == 'paragraph':
                formatted_text = self._apply_inline_formatting(content_text)
                html_parts.append(f'<p>{formatted_text}</p>')
            elif block_type == 'bullet_list':
                items = block.get('items', [])
                list_html = '<ul>'
                for item in items:
                    formatted_item = self._apply_inline_formatting(item)
                    list_html += f'<li>{formatted_item}</li>'
                list_html += '</ul>'
                html_parts.append(list_html)
            elif block_type == 'numbered_list':
                items = block.get('items', [])
                list_html = '<ol>'
                for item in items:
                    formatted_item = self._apply_inline_formatting(item)
                    list_html += f'<li>{formatted_item}</li>'
                list_html += '</ol>'
                html_parts.append(list_html)
            elif block_type == 'code_block':
                code_content = block.get('content', '')
                language = block.get('language', '')
                html_parts.append(f'<pre><code class="language-{language}">{code_content}</code></pre>')
            elif block_type == 'blockquote':
                quote_text = self._apply_inline_formatting(content_text)
                html_parts.append(f'<blockquote>{quote_text}</blockquote>')
        
        return '\n'.join(html_parts)
    
    def _apply_inline_formatting(self, text):
        """Apply inline formatting (bold, italic, links) to text"""
        if not text:
            return ""
        
        formatted_text = text
        
        import re
        formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_text)
        formatted_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', formatted_text)
        formatted_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', formatted_text)
        
        return formatted_text
