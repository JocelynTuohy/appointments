# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from ..login.models import User
from .models import Task
# Create your views here.
def index(request):
    print '!'*100
    context = {
        'user': User.objects.get(id=request.session['id']),
        'todaytasks': Task.objects.todayTasks(request.session['id']),
        'futuretasks': Task.objects.futureTasks(request.session['id'])
    }
    return render(request, 'schedule/index.html', context)

def edit(request, appt):
    try:
        thisappt = Task.objects.get(id=appt)
        context = {
            'task': thisappt,
        }
        return render(request, 'schedule/edit.html', context)
    except ObjectDoesNotExist:
        messages.error(request, 'That task does not appear to exist!')
        return redirect('schedule/index.html')

def add(request):
    if request.method == 'POST':
        errors = Task.objects.validate(request.POST, request.session['id'])
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('schedule:index'))
        else:
            Task.objects.addTask(request.POST, request.session['id'])
    return redirect(reverse('schedule:index'))

def delete(request, appt):
    try:
        Task.objects.get(id=appt).delete()
    except ObjectDoesNotExist:
        messages.error(request, 'You just tried to delete an appointment ' +
                       'that does not exist.')
    return redirect(reverse('schedule:index'))

def update(request, appt):
    if request.method == 'POST':
        errors = Task.objects.validate(request.POST, request.session['id'], appt)
        statuserror = Task.objects.validateStatus(request.POST)
        if statuserror:
            errors.append(statuserror)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(reverse('schedule:edit', kwargs={'appt': appt}))
        else:
            Task.objects.update(request.POST, appt)
            return redirect(reverse('schedule:index'))
    else:
        messages.error(request, 'Whatever you just tried did not work.')
        return redirect(reverse('schedule:edit', kwargs={'appt': appt}))
