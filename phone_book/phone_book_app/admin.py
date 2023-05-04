from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

# Register your models here.

class PhoneCardAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone_number',
        'name',
        'company_division_name',
        'address',
        'slug',
        'create_date',
        'update_date',
        'cat',
        'is_published',)
    list_display_links = ('id', 'phone_number')
    search_fields = (
        'phone_number',
        'name',
        'company_division_name',
        'address', )
    prepopulated_fields = {'slug': ('id',)}
    list_editable = ('is_published',)
    list_filter = ('is_published', 'create_date')
    fields = ('phone_number', 'slug', 'cat', 'name', 'create_date', 'update_date', )
    readonly_fields = ('create_date', 'update_date', )
    save_on_top = True


# class CompanyAdmin(admin.ModelAdmin):
#     list_display = ('id', 'phone_number', 'company_name', 'slug', 'create_date', 'cat', 'is_published')
#     list_display_links = ('id', 'phone_number')
#     search_fields = ('phone_number', 'company_name')
#     prepopulated_fields = {'slug': ('company_name',)}
#     list_editable = ('is_published',)
#     list_filter = ('is_published', 'create_date')
#     fields = ('phone_number', 'slug', 'cat', 'company_name', 'create_date', 'update_date',)
#     readonly_fields = ('create_date', 'update_date',)
#     save_on_top = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('id', )
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(PhoneCard, PhoneCardAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_header = 'Администраторская панель'
admin.site.site_title = 'Телефонный справочник'

