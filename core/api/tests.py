# -*- encoding: utf-8 -*-
from datetime import datetime

from django.test import TestCase

from models import ApiUser, ApiSession, ApiLog
from lojas.tests import ShoppingModelTest

class ApiUserModelTest(TestCase):
    @classmethod
    def _create_user(cls, shopping, token, name='Usuario teste', email='nada@void.com'):
        user = ApiUser()
        user.shopping = shopping
        user.nome = name
        user.email = email
        user.token = token
        user.save()
        return user

    def test_creating_a_new_apiuser_and_save_it_to_the_database(self):
        '''
        Start creating a new shopping
        '''
        shopping = ShoppingModelTest._create_shopping()
        token = ApiUser.create_token(shopping.slug)

        # Check if user can be created and saved on the database
        user = self._create_user(shopping, token)

        # Now check if it can be found in the database
        all_users_in_database = ApiUser.objects.all()
        self.assertEquals(len(all_users_in_database), 1)
        only_user_in_database = all_users_in_database[0]

        # Now check its attributes
        self.assertEquals(only_user_in_database, user)

        self.assertEquals(only_user_in_database.nome, 'Usuario teste')
        self.assertEquals(only_user_in_database.email, 'nada@void.com')
        self.assertEquals(only_user_in_database.token, token)
        self.assertEquals(only_user_in_database.shopping, shopping)


def create_new_user():
    shopping = ShoppingModelTest._create_shopping()
    token = ApiUser.create_token(shopping.slug)
    user = ApiUserModelTest._create_user(shopping, token)
    return user

class ApiSessionModelTest(TestCase):
    @classmethod
    def _create_session(cls, user, inicio, fim):
        sessao = ApiSession()
        sessao.user = user
        sessao.inicio = inicio
        sessao.fim = fim
        sessao.save()
        return sessao

    def test_create_new_session_and_save_it_in_the_database(self):
        user = create_new_user()
        inicio = datetime.strptime('Jul 18 2015  1:33PM', '%b %d %Y %I:%M%p')

        # Check if session can be created and saved on the database
        sessao = self._create_session(user, inicio, None)

        # Now check if it can be found on the database
        all_sessions_in_database = ApiSession.objects.all()
        self.assertEquals(len(all_sessions_in_database), 1)
        only_session_in_database = all_sessions_in_database[0]

        #Checking attributes
        self.assertEquals(only_session_in_database, sessao)

        self.assertEquals(only_session_in_database.user, user)
        # self.assertEquals(only_session_in_database.inicio, inicio)
        self.assertEquals(only_session_in_database.fim, None)


class ApiLogModelTest(TestCase):
    @classmethod
    def _create_log(cls, sessao):
        log = ApiLog()
        log.sessao = sessao
        log.save()
        return log

    def test_create_new_log_and_save_it_the_database(self):
        user = create_new_user()
        inicio = datetime.now()
        sessao = ApiSessionModelTest._create_session(user, inicio, None)

        # Check if session can be created and saved on the database
        log = self._create_log(sessao)

        # can it be found?
        all_logs_in_database = ApiLog.objects.all()
        self.assertEquals(len(all_logs_in_database), 1)
        only_log_in_database = all_logs_in_database[0]

        # attributes
        self.assertEquals(only_log_in_database, log)

        self.assertEquals(only_log_in_database.sessao, sessao)
