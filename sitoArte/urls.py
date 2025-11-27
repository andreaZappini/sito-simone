from django.urls import path
from . import views

urlpatterns = [
    path('', views.opere, name="opere"),
    path('<int:pk>/', views.dettaglio_opera, name="dettaglio_opera"),
]