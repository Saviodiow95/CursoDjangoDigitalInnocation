from django.contrib import admin
from .models import  *


class EventoAdmin(admin.ModelAdmin):
    list_display = ('id','titulo','data_evento','created_at')
    list_filter = ('created_at',)

admin.site.register(Evento, EventoAdmin)
