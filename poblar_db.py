import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from blog.models import Author, Category, Tag, Post, Comment

def cargar_datos():
    print("Limpiando datos antiguos...")
    Author.objects.all().delete()
    Category.objects.all().delete()
    Tag.objects.all().delete()
    Post.objects.all().delete()

    print("Creando autores, categorías y etiquetas...")
    a1 = Author.objects.create(name="Alice Smith", email="alice@example.com", country="Peru")
    a2 = Author.objects.create(name="Bob Jones", email="bob@example.com", country="Chile")
    a3 = Author.objects.create(name="Charlie Brown", email="charlie@example.com", country="Peru")

    c1 = Category.objects.create(name="Tecnología")
    c2 = Category.objects.create(name="Ciencia")

    t1 = Tag.objects.create(name="Django")
    t2 = Tag.objects.create(name="Python")

    titulos_esp = [
        "Introducción a Django y desarrollo web",
        "Optimización de consultas ORM con select_related",
        "Creación de APIs REST con Python",
        "Buenas prácticas de arquitectura en Django",
        "Uso de bases de datos relacionales en la nube",
        "Seguridad y autenticación de usuarios en aplicaciones web",
        "Despliegue continuo de aplicaciones en la nube"
    ]

    print("Creando 15 publicaciones...")
    for i in range(1, 16):
        titulo = titulos_esp[(i - 1) % len(titulos_esp)] if i % 2 == 0 else f"Publicación borrador {i}"
        
        p = Post.objects.create(
            title=titulo,
            content=f"Este es el contenido explicativo para la publicación número {i}, donde se abordan conceptos clave de desarrollo web con Django y ORM.",
            is_published=(i % 2 == 0),
            author=a1 if i <= 5 else (a2 if i <= 10 else a3),
            category=c1 if i % 2 == 0 else c2
        )
        p.tags.add(t1, t2)

        if i % 2 == 0:
            Comment.objects.create(post=p, text=f"Excelente comentario en la publicación {i}")
            Comment.objects.create(post=p, text=f"Segundo comentario de prueba en {i}")

    print("--- ¡BASE DE DATOS POBLADA EXITOSAMENTE EN ESPAÑOL! ---")

if __name__ == "__main__":
    cargar_datos()