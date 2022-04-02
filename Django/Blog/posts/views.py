from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView


class PostIndex(ListView):
    pass


class PostBusca(PostIndex):
    pass


class PostCategoria(PostIndex):
    pass


class PostDetalhes(UpdateView):
    pass
