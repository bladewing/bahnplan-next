from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from accounts.models import Player


class PlayerInline(admin.StackedInline):
    model = Player


class UserAdmin(BaseUserAdmin):
    inlines = (PlayerInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Player)
