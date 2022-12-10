from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from plant_shop.accounts.models import UserProfile

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ('email', 'is_staff', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': (
            'email',
            'password',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active',
            'date_joined',
        )}),

        ('Permissions', {
            'fields': ('groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')


@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ('user', 'city', 'address_line_1', 'address_line_2')
