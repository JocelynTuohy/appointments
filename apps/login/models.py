# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from datetime import datetime, date
import bcrypt
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
ALPHASPACE_REGEX = re.compile(r'^[a-zA-Z]+[a-zA-Z ]+[a-zA-Z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validate(self, form_data):
        errors = []
        if (len(form_data['name']) < 3 or
                not ALPHASPACE_REGEX.match(form_data['name'])):
            errors.append(
                'Name must include at least three characters ' +
                '(only letters and spaces allowed--must begin and end with a ' +
                'letter).')
        if not EMAIL_REGEX.match(form_data['reg_email']):
            errors.append('Please enter a valid email.')
        try:
            User.objects.get(email=form_data['reg_email'])
            errors.append('Account has already been created for this email.')
        except ObjectDoesNotExist:
            print 'good, they do not already have an account'
        if len(form_data['reg_password']) < 8:
            errors.append('Password must include at least eight characters.')
        if form_data['reg_password'] != form_data['confirm']:
            errors.append('Passwords do not match.')
        # DOB validation
        try:
            birthdate = datetime.strptime(
                form_data['birthdate'], '%Y-%m-%d'
            ).date()
            today = date.today()
            print birthdate
            age = (
                today.year - birthdate.year - ((today.month, today.day) <
                                               (birthdate.month, birthdate.day))
            )
            print age
            if age < 10:
                errors.append(
                    'You must be at least 10 years old to use this ' +
                    'application. We have standards.'
                )
        except ValueError:
            errors.append('Invalid birth date.')
        return errors
    def register(self, user_data):
        new_user = User(
            name=user_data['name'],
            email=user_data['reg_email'],
            password=bcrypt.hashpw(
                user_data['reg_password'].encode(), bcrypt.gensalt()
            ),
            birthdate=datetime.strptime(user_data['birthdate'],
                                        "%Y-%m-%d").date()
        )
        new_user.save()
        return new_user
    def log_validate(self, form_data):
        found_user = User.objects.get(email__iexact=form_data['log_email'])
        return found_user
    def check_password(self, user_data, form_data):
        if user_data.password == bcrypt.hashpw(
                form_data['log_password'].encode(),
                user_data.password.encode()):
            return True
        else:
            return False
    def login(self, user_data):
        logged_user = User.objects.get(email__iexact=user_data['log_email'])
        return logged_user.id

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
