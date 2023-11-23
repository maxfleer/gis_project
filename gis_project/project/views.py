from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from .forms import RegisterForm
# Create your views here.


def homepage (request):
    return render(request, 'homepage.html')

@login_required
def gamepage (request):
    return render(request, "gamepage.html")

@login_required
def leaderboard (request):
    return render(request, "leaderboard.html")

@login_required
def logout (request):
    return render(request, "logged_out.html")

@login_required
def profile (request):
    return render(request, "profile.html")


class RegisterView (generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'