
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap





from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap


urlpatterns = [
    path('admin/', admin.site.urls),
    path('info/', include('information.urls')),
    path('services/', include('services.urls')),
    path('careers/', include('careers.urls')),
    path('blog/', include('posts.urls')),
    path('project/', include('projects.urls')),
    path('appointment/', include('appointments.urls')),
    path('task/', include('tasks.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    
    path('account/', include('accounts.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('social/', include('allauth.urls')),
    

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
