from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Language)
admin.site.register(models.Phrase)
admin.site.register(models.Comment)
