# -*- encoding: utf-8 -*-
from django.test import TestCase

from models import ApiUser
from lojas.tests import ShoppingModelTest

class ApiUserModelTest(TestCase):
    @classmethod
    def _create_user(cls, shopping, name='Usuario teste', email='nada@void.com'):
        user = ApiUser()
        user.shopping = shopping
        user.nome = name
        user.email = email
        user.save()
        return user

    def test_creating_a_new_apiuser_and_save_it_to_the_database(self):
        '''
        Start creating a new shopping
        '''
        shopping = ShoppingModelTest._create_shopping()

        # Check if user can be created and saved on the database
        user = self._create_user(shopping)

        # Now check if it can be found in the database
        all_users_in_database = ApiUser.objects.all()
        self.assertEquals(len(all_users_in_database), 1)
        only_user_in_database = all_users_in_database[0]

        # Now check its attributes
        self.assertEquals(only_user_in_database, user)

        self.assertEquals(only_user_in_database.nome, 'Usuario teste')
        self.assertEquals(only_user_in_database.email, 'nada@void.com')
        self.assertEquals(only_user_in_database.shopping, shopping)
