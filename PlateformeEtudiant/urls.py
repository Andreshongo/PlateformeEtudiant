from django.contrib import admin
from magasin import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from magasin.views import tableau_de_bord
from django.contrib.auth.views import LogoutView
urlpatterns = [
    # tes autres URL ici
    path('admin/', admin.site.urls),
    path('', include('magasin.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', tableau_de_bord, name='tableau_de_bord'),
    path('commander/', views.commander_view, name='commander'),

    path('compte/', include('compte.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

