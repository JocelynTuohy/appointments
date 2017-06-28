# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import User

# Create your views here.
def index(request):
    print 'in the login index route'
    return redirect(reverse('login:main'))

def main(request):
    print 'in the login main route'
    return render(request, 'login/index.html')

def login(request):
    print 'in the login login route'
    if request.method == 'POST':
        try:
            login_user = User.objects.log_validate(request.POST)
        except ObjectDoesNotExist:
            messages.error(request, 'Login failed; try again.')
            return redirect(reverse('login:main'))
        if User.objects.check_password(login_user, request.POST):
            request.session['id'] = login_user.id
            return redirect(reverse('schedule:index'))
        else:
            messages.error(request, 'Login failed; try again.')
    return redirect(reverse('login:main'))

def register(request):
    print 'in the login register route'
    if request.method == 'POST':
        errors = User.objects.reg_validate(request.POST)
        if not errors:
            new_user = User.objects.register(request.POST)
            request.session['id'] = new_user.id
            return redirect(reverse('schedule:index'))
        else:
            for error in errors:
                messages.error(request, error)
    return redirect(reverse('login:main'))

def logout(request):
    request.session.flush()
    messages.success(request, 'You have been logged out. Come again!')
    return redirect(reverse('login:main'))
