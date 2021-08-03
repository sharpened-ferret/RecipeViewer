from django.contrib import admin

from .models import Recipe, Keyword, NutritionalInfo

admin.site.register(Recipe)
admin.site.register(Keyword)
admin.site.register(NutritionalInfo)