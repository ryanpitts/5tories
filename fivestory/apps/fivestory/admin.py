from django.contrib import admin

from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    save_on_top=True
    exclude=('description',)
    readonly_fields=('created','updated',)
    list_display=('name','description','created',)
    