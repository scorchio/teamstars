from django.contrib.auth.models import User
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
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'votes/add.html', context)
