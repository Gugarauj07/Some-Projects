from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from .models import Post


class PostIndex(ListView):
    model = Post
    template_name = 'posts/index.html'
    paginate_by = 3
    context_object_name = 'posts'


class PostBusca(PostIndex):
    pass


class PostCategoria(PostIndex):
    pass


class PostDetalhes(UpdateView):
    pass
