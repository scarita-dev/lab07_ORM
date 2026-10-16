import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Author, Category, Tag, Post, Comment
from django.db.models import Count
from django.db import connection, reset_queries

print("="*60)
print(" EVIDENCIA DE CONSULTAS ORM - LABORATORIO 07 ")
print("="*60)

# 1. Consultas Básicas
print("\n--- 1. CONSULTAS BÁSICAS ---")
print("Todos los posts:", Post.objects.all())
print("Post con ID 1:", Post.objects.get(id=1))
print("Posts publicados:", Post.objects.filter(is_published=True))
print("Posts no publicados:", Post.objects.filter(is_published=False))

# 2. Field Lookups
print("\n--- 2. BÚSQUEDAS POR CAMPO (FIELD LOOKUPS) ---")
print("Título contiene '1':", Post.objects.filter(title__icontains="1"))
print("Rango de fechas 2026:", Post.objects.filter(created_at__range=["2026-01-01", "2026-12-31"]).count(), "posts encontrados")
print("Sin categoría:", Post.objects.filter(category__isnull=True))
print("Más de 1 comentario:", Post.objects.annotate(num_comments=Count('comments')).filter(num_comments__gt=1))

# 3. Relaciones (Doble Guion Bajo)
print("\n--- 3. NAVEGACIÓN DE RELACIONES (__) ---")
print("Posts de autores de Perú:", Post.objects.filter(author__country="Peru"))
print("Comentarios en categoría Tecnología/Tech:", Comment.objects.filter(post__category__name__in=["Tech", "Tecnología"]))

# 4. Ordenar y Limitar
print("\n--- 4. ORDENAR Y LIMITAR ---")
print("10 más recientes:", Post.objects.order_by('-created_at')[:10])
print("5 más comentados:", Post.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:5])

# 5. Manager propio
print("\n--- 5. USO DE PUBLISHED MANAGER ---")
print("Posts desde Post.published:", Post.published.all())

# 6. Comparativa N+1
print("\n--- 6. MEDICIÓN DEL PROBLEMA N+1 ---")

reset_queries()
posts = list(Post.objects.all())
for p in posts:
    _ = p.author.name
print("Consultas SIN OPTIMIZAR:", len(connection.queries))

reset_queries()
posts_opt = list(Post.objects.select_related('author').prefetch_related('tags').all())
for p in posts_opt:
    _ = p.author.name
    _ = [t.name for t in p.tags.all()]
print("Consultas CON OPTIMIZACIÓN (select_related + prefetch_related):", len(connection.queries))

print("\n" + "="*60)
print(" FIN DE LA EJECUCIÓN ")
print("="*60)