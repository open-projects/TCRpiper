from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm


def sign_in(request):
    if request.method == "POST" and 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))
        else:
            ...  # TODO: add control for duplicate names and emails
    return HttpResponseRedirect(reverse('index:index'))


def sign_up(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('experiment:experiment_stock'))
    return HttpResponseRedirect(reverse('index:index'))


def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('index:index'))

