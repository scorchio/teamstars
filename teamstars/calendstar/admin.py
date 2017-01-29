from django.contrib import admin

from models import CalendarEvent


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'starts', 'ends', 'is_private', 'submitted_by']
    list_filter = ['starts', 'is_private']
    search_fields = ['title']


admin.site.register(CalendarEvent, CalendarAdmin)
