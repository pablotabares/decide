from django.contrib import admin

from .models import Mixnet, ConnectionStatus


admin.site.register(Mixnet)
admin.site.register(ConnectionStatus)