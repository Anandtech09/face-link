from django.contrib import admin

# Register your models here.
from .models import Scholarship

class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'deadline')
    search_fields = ('name', 'description','s_caste')
    list_filter = ('deadline',)

admin.site.register(Scholarship, ScholarshipAdmin)
