from django.contrib import admin
from .models import Biografia, Mostra, Opera, ImmagineOpera, VideoOpera


# Register your models here.


admin.site.register(Opera)
admin.site.register(ImmagineOpera)
admin.site.register(VideoOpera)
admin.site.register(Mostra)
admin.site.register(Biografia)
