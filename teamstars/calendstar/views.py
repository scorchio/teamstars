from django.shortcuts import render

from calendstar.models import CalendarEvent


def index(request):
    context = {
        "events": CalendarEvent.objects.all()
    }
    return render(request, 'calendstar/index.html', context)


def single(request, event_id):
    context = {
        "event": CalendarEvent.objects.get(pk=event_id)
    }
    return render(request, 'calendstar/single.html', context)
