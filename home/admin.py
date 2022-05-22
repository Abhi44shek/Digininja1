from django.contrib import admin
from .models import Search,Contact

# Register your models here.
@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display = ('query','user',)
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','phone',)