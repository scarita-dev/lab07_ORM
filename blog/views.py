from django.shortcuts import render
from .models import Post

def post_list(request):
    # Paso 8, 9 y 10: Usamos el manager personalizado y optimizamos con select_related y prefetch_related
    posts = Post.published.select_related('author').prefetch_related('tags').all()
    
    return render(request, 'blog/post_list.html', {'posts': posts})
