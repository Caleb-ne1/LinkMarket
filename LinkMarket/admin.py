from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product, Category, Cart
from .forms import CustomUserCreationForm, CustomUserChangeForm, CategoryForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Cart)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'stock', 'price', 'image', 'view_link', 'edit_link', 'delete_link')

    def view_link(self, obj):
        return f'<a href="{obj.view()}">View</a>'
    view_link.allow_tags = True
    view_link.short_description = 'View'

    def edit_link(self, obj):
        return f'<a href="{obj.edit()}">Edit</a>'
    edit_link.allow_tags = True
    edit_link.short_description = 'Edit'

    def delete_link(self, obj):
        return f'<a href="{obj.delete()}">Delete</a>'
    delete_link.allow_tags = True
    delete_link.short_description = 'Delete'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image', 'name')

