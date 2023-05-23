from django.contrib import admin

from .models import Game, User

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "stage_number", "end_date")
    list_display_links = ("id", "name")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "stage1", "stage2", "game")
    list_display_links = ("id", "name")
