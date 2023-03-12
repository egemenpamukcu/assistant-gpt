from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from social_django import urls as social_auth_urls
from .views import home
from django.contrib.auth.views import LogoutView
admin.autodiscover()

urlpatterns = [
    path('', home, name='home'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('chat/', include('apps.chatbot.urls')),
    path('admin/', admin.site.urls),
# #    path('login-redirect/', login_redirect, name='login_redirect'),
#     path('auth/', include('social_django.urls', namespace='social')),
#     path('login/', auth_views.LoginView.as_view(template_name='login.html', extra_context={'google_auth': True}), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]