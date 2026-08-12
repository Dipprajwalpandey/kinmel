from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    # Redirect base URL to the store
    path('', RedirectView.as_view(url='/store/', permanent=True)),

    # Django Admin
    path('admin/', admin.site.urls),

    # App Routers
    path('store/', include('store.urls')),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),

    # Dashboard Router
    path('useradmin/', include('useradmin.urls')),

    # Auth Views
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

from django.views.static import serve
from django.urls import re_path

# Serve media files even in production (for Render without S3)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]