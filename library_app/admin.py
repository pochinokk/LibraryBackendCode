from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book

class BookInline(admin.StackedInline):
    model = Book
    extra = 0

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'phone', 'address', 'role')}),
    )
    # # Полностью переопределяем fieldsets
    # fieldsets = (
    #     (None, {'fields': ('username', 'password')}),
    #     ('Персональная информация', {'fields': ('full_name', 'phone', 'address', 'role')}),
    #     ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    #     ('Даты', {'fields': ('last_login', 'date_joined')}),
    # )

    # # Переопределяем add_fieldsets для формы добавления
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('username', 'password1', 'password2', 'full_name', 'phone', 'address', 'role'),
    #     }),
    # )
    def save_model(self, request, obj, form, change):
        if obj.role in ('LIBRARIAN', 'ADMIN'):
            obj.is_staff = True
        else:
            obj.is_staff = False
        super().save_model(request, obj, form, change)
    inlines = (
        BookInline,
    )
    list_display = ('username', 'full_name', 'role', 'is_staff')
    search_fields = ('username', 'full_name', 'role')
    # list_display = (
    #     'username',        
    # )

class BookAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'printing_year',
        'language',
        'end_date',
        'is_taken',
        'reader',
    )
    list_editable = (
        'reader',
        'author',
        'printing_year',
        'language'
    )    
    search_fields = ('name',)
    list_filter = ('reader',)
    list_display_links = ('name',)




admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.empty_value_display = 'Не задано'
