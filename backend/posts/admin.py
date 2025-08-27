from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'rendered_html']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug')
        }),
        ('Content', {
            'fields': ('content',),
            'description': 'Content should be a JSON array of content blocks'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Rendered Output', {
            'fields': ('rendered_html',),
            'classes': ('collapse',),
            'description': 'Auto-generated HTML from content'
        }),
    )
