from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
# 
from django.views.generic import (    
    View,
    ListView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Favorites

# app
from applications.entrada.models import Entry

# Create your views here.
class UserPageView(LoginRequiredMixin, ListView):   
    template_name = "favoritos/perfil.html"
    context_object_name = 'entradas_user'
    login_url = reverse_lazy('users_app:user-login')
    
    def get_queryset(self):
        return Favorites.objects.entradas_user(self.request.user)
    
    
class AddFavoritos(LoginRequiredMixin, View):
    login_url = reverse_lazy('users_app:user-login')
    
    def post(self, request, *args, **kwargs):
        # recuperar el usuario
        usuario = self.request.user
        # recuperar el id de la entrada
        entrada = Entry.objects.get(id=self.kwargs['pk'])
        # registrar la entrada a favoritos
        Favorites.objects.create(
            user=usuario,
            entry=entrada,
        )
        
        return HttpResponseRedirect(
            reverse(
                'favoritos_app:perfil'
            )
        )
        

class FavoritesDeleteView(DeleteView):
    model = Favorites
    success_url = reverse_lazy('favoritos_app:perfil')