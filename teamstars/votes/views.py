from django.shortcuts import render, redirect
from django.contrib.auth import logout

from .models import Vote


def index(request):
    context = {
        'leaderboard': Vote.objects.leaderboard(),
        'vote_stats': Vote.objects.vote_statistics(),
    }
    return render(request, 'votes/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('vote_index')
