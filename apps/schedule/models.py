# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date, time
from django.db import models
from ..login.models import User
# Create your models here.
class TaskManager(models.Manager):
    def todayTasks(self, user):
        todaytasks = (
            Task.objects.filter(date=date.today())
            .filter(user=User.objects.get(id=user))
            .order_by('time')
        )
        return todaytasks
    def futureTasks(self, user):
        futuretasks = (
            Task.objects.filter(date__gt=date.today())
            .filter(user=User.objects.get(id=user))
            .order_by('date')
        )
        return futuretasks
    def addTask(self, form_data, user_id):
        newtask = Task(
            user=User.objects.get(id=user_id),
            task=form_data['task'],
            status='Pending',
            date=datetime.strptime(form_data['date'], "%Y-%m-%d").date(),
            time=datetime.strptime(form_data['time'], "%H:%M").time()
        )
        newtask.save()
        return newtask
    def validate(self, form_data, user_id, appt_id=None):
        errors = []
        if len(form_data['task']) < 1:
            errors.append('Please provide a task/appointment description.')
        try:
            thisdate = datetime.strptime(form_data['date'], "%Y-%m-%d").date()
            thistime = datetime.strptime(form_data['time'], "%H:%M").time()
            thistasktime = datetime.combine(thisdate, thistime)
        except ValueError:
            errors.append('Invalid date or time.')
            return errors
        # date and time must be unique for this user
        thisuser = User.objects.get(id=user_id)
        usertasks = Task.objects.filter(user=thisuser)
        for each in usertasks:
            thattasktime = datetime.combine(each.date, each.time)
            if not appt_id:
                if thistasktime == thattasktime:
                    errors.append('You already have an appointment at that date ' +
                                  'and time.')
        # date and time must be in the future
        if datetime.now() > thistasktime:
            errors.append('You may only add appointments that are in the ' +
                          'future.')
        return errors
    def update(self, form_data, appt_id):
        update_task = Task.objects.get(id=appt_id)
        update_task.task = form_data['task']
        update_task.date = datetime.strptime(form_data['date'],
                                             "%Y-%m-%d").date()
        update_task.time = datetime.strptime(form_data['time'], "%H:%M").time()
        update_task.status = form_data['status']
        print update_task.date
        update_task.save()
        return update_task
    def validateStatus(self, form_data):
        error = None
        if form_data['status'] not in ['Done', 'Pending', 'Missed']:
            error = 'Invalid task status.'
        return error

class Task(models.Model):
    user = models.ForeignKey(User)
    task = models.CharField(max_length=255)
    status = models.CharField(max_length=7)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskManager()
