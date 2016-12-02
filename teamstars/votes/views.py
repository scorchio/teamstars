from django.shortcuts import render

from .models import Vote


def index(request):
    context = {
        'leaderboard': Vote.objects.leaderboard(),
        'vote_stats': Vote.objects.vote_statistics(),
    }
    return render(request, 'votes/index.html', context)
