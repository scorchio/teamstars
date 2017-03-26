from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from common.forms import UserSettingsForm

@login_required
def settings(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            request.user.username = form.cleaned_data['username']
            request.user.save()
            return HttpResponseRedirect('/user/')

    else:
        form = UserSettingsForm(initial={'username': request.user.username})

    return render(request, 'common/settings.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('vote_index')
