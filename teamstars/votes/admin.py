from django.contrib import admin

from models import Vote, VoteType


class VoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'sender', 'recipient', 'created']
    list_filter = ['created']
    search_fields = ['title']


admin.site.register(Vote, VoteAdmin)
admin.site.register(VoteType)
