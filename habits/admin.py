from django.contrib import admin
from .models import Habit


# Register your models here.
@admin.register(Habit)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('creator', 'time', 'frequency', 'duration',)
    list_filter = ('creator',)
    search_fields = ('creator',)
