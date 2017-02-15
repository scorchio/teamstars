from django.shortcuts import render, redirect
from django.contrib.auth import logout

from .models import Vote


def index(request):
    context = {
        'leaderboard': Vote.objects.leaderboard(),
        'vote_stats': Vote.objects.vote_statistics(),
        'stars': 42,
    }
    return render(request, 'votes/index.html', context)


def add(request):
    context = {}
    return render(request, 'votes/add.html', context)


def logout_view(request):
    logout(request)
    return redirect('vote_index')
