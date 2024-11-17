from django.contrib import admin
from .models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'progress', 'raised_amount', 'goal_amount', 'progress_percentage')
    search_fields = ('title', 'category', 'location')
    list_filter = ('category', 'location')


# Register your models here.
