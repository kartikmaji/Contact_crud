# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

class Contact(models.Model):
    name = models.CharField(
        max_length=32,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=70,
        blank=False,
        null=False,
        unique=True
    )

    def save(self, *args, **kwargs):

        # Checks for valid email address before saving
        validator = EmailValidator()
        try:
            validator(self.email)
            super(Contact, self).save(*args, **kwargs)
        except ValidationError as e:
            raise e

    def __str__(self):
        return "{} - {}".format(self.name, self.email)

    @receiver(post_save, sender=User)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)