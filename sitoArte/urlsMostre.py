from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostre, name="mostre"),
    path('<int:pk>/', views.dettaglio_mostra, name="dettaglio_mostra")
    # path('contatti/', views.contatti, name="contatti"),
    # path('mostre/', views.mostre, name="mostre")
]