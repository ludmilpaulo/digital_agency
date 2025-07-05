import json
import os
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from posts.models import Author, Category, Tag, Post

User = get_user_model()

def get_image_from_url(url):
    # You can install requests: pip install requests
    import requests
    from django.core.files.temp import NamedTemporaryFile

    if not url:
        return None

    img_temp = NamedTemporaryFile(delete=True)
    r = requests.get(url)
    if r.status_code == 200:
        img_temp.write(r.content)
        img_temp.flush()
        return img_temp
    return None

class Command(BaseCommand):
    help = 'Load demo blogs from a JSON file'

    def handle(self, *args, **options):
        file_path = os.path.join(os.getcwd(), "maindo_blogs.json")
        with open(file_path, "r", encoding="utf-8") as f:
            blogs = json.load(f)

        for blog in blogs:
            # Create/get category
            cat_names = [c.strip() for c in blog.get("categories", "").split(",") if c.strip()]
            if cat_names:
                cat_name = cat_names[0]
                category, _ = Category.objects.get_or_create(
                    slug=slugify(cat_name),
                    defaults={"name": cat_name, "description": cat_name}
                )
            else:
                category = None

            # Create/get tags
            tag_objs = []
            tag_names = [t.strip() for t in blog.get("tags", "").split(",") if t.strip()]
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tag_objs.append(tag)

            # Create/get author
            author_data = blog.get("author")
            if author_data:
                user, _ = User.objects.get_or_create(
                    username=slugify(author_data["name"]).replace("-", ""),
                    defaults={"first_name": author_data["name"].split(" ")[0], "last_name": " ".join(author_data["name"].split(" ")[1:])}
                )
                author, _ = Author.objects.get_or_create(
                    user=user,
                    defaults={
                        "bio": author_data.get("bio", ""),
                        # Optionally download avatar if you want
                    }
                )
            else:
                author = None

            # Download the post image if you want, else set blank
            image_field = None
            if blog.get("image"):
                try:
                    img_temp = get_image_from_url(blog["image"])
                    if img_temp:
                        image_field = ContentFile(img_temp.read(), name=f'post_{blog["id"]}.jpg')
                except Exception as e:
                    print(f"Image download failed: {e}")

            # Create post
            post, created = Post.objects.get_or_create(
                title=blog["title"],
                defaults={
                    "author": author,
                    "content": blog["content"],
                    "image": image_field,
                    "published_date": blog["published_date"],
                    "status": "published",
                    "category": category,
                    "featured": False,
                }
            )
            if created:
                post.tags.set(tag_objs)
                post.save()
                self.stdout.write(self.style.SUCCESS(f"Loaded blog: {blog['title']}"))
            else:
                self.stdout.write(f"Skipped (exists): {blog['title']}")

        self.stdout.write(self.style.SUCCESS("All demo blogs loaded!"))
