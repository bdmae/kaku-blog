from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import json


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.JSONField(default=list)  # Store structured content
    rendered_html = models.TextField(blank=True)  # Store rendered HTML
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Ensure slug uniqueness
        if Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
            counter = 1
            while Post.objects.filter(slug=f"{self.slug}-{counter}").exclude(pk=self.pk).exists():
                counter += 1
            self.slug = f"{self.slug}-{counter}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def snippet(self):
        """Generate a snippet from the content for list views"""
        if not self.content:
            return ""

        # Extract text from first few content blocks
        text_parts = []
        for block in self.content[:3]:  # First 3 blocks
            if block.get('type') == 'paragraph':
                text = block.get('content', '')
                if text:
                    text_parts.append(text)
        
        snippet = ' '.join(text_parts)
        return snippet[:150] + '...' if len(snippet) > 150 else snippet
