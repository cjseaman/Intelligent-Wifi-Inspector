# This is the file that does all the heavy lifting
# This file controls how the website looks and what code runs when things happen

from django.views.generic import TemplateView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from Wifi_Inspector import models as m
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user, login, logout

# This is the home view, it renders the index.html template from the templates folder when activated.
def home(request):
	return render(request, 'index.html')