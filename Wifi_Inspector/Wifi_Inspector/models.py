#This file contains the data structures (classes) that are saved in the database

from django.db import models as m

#Example:

"""
from django.contrib.auth.base_user import AbstractBaseUser

class judge(AbstractBaseUser):
    judge_name = m.CharField(max_length=128)
    judge_email = m.CharField(max_length=128, primary_key=True)
    session_id = m.IntegerField(default=0)
    is_admin = m.BooleanField(default=False)
    USERNAME_FIELD = 'judge_email'
    EMAIL_FIELD = 'judge_email'
    REQUIRED_FIELDS = ['judge_name']

"""
