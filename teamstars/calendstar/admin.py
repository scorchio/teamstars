from django.contrib import admin

from models import CalendarEvent, CalendarEventResponse


class CalendarAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'starts', 'ends', 'is_private', 'submitted_by']
    list_filter = ['starts', 'is_private']
    search_fields = ['title']


class CalendarEventResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'calendar_event', 'status', 'comment']


admin.site.register(CalendarEvent, CalendarAdmin)
admin.site.register(CalendarEventResponse, CalendarEventResponseAdmin)
