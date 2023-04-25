from django.contrib import admin

from . import models


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'currency',
        'balance',
    )


admin.site.register(models.User, UserAdmin)
