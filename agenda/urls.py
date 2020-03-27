from django.urls import path
from .views import *

urlpatterns = [
    path('', lista_eventos),
    path('evento/', evento),
    path('evento/submit', submit_evento),
    path('evento/delete/<int:id>', delete_evento),
    path('lista/', json_lista)
]