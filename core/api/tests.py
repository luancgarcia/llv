# -*- encoding: utf-8 -*-
from django.test import TestCase

from models import ApiUser

class ApiUserModelTest(TestCase):
    @classmethod
    def _create_user(cls):
        user = ApiUser()
        #todo: implementar demais campos
        return user
