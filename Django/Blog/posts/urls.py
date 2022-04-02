from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostIndex, name='index'),
    path('categoria/<str:categoria>', views.PostCategoria, name='post_categoria'),
    path('busca/', views.PostBusca, name='post_busca'),
    path('post/<int:pk>', views.PostDetalhes, name='post_detalhes'),
]