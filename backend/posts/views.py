from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

class HomeView(ListView):
    """Home page view with navigation options"""
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        # Get the latest 3 posts for preview
        return Post.objects.all().order_by('-created_at')[:3]

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('posts:post-list')

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('posts:post-list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:post-list')