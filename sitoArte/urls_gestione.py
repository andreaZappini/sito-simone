from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    
    path('nuova_opera/', views.nuova_opera, name="nuova_opera"),
    path('modifica_opera/<int:pk>/', views.modifica_opera, name='modifica_opera'),
]