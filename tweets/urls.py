from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import home

app_name='tweets'


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('auth/', views.oauth, name='auth'),
    path('callback/', views.callback, name='callback'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    # path('oauth/', include('social_django.urls', namespace='social')),
]
