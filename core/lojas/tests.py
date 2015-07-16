# -*- encoding: utf-8 -*-
from utils.functions import printa

from django.test import TestCase

from models import Shopping


class ShoppingModelTest(TestCase):
    @classmethod
    def _create_shopping(cls, name='Shopping teste', slug='shopping-teste'):
        mall = Shopping()
        mall.nome = name
        mall.slug = slug
        mall.save()
        return mall

    def test_creating_a_new_shoppig_and_save_it_to_the_database(self):
        '''
        Start creating a new shopping
        '''
        # shopping, nome, email, token
        # Check if mall can be created and saved on the database
        mall = self._create_shopping()

        # Now check if it can be found in the database
        all_malls_in_database = Shopping.objects.all()
        printa(all_malls_in_database)
        self.assertEquals(len(all_malls_in_database), 1)
        only_mall_in_database = all_malls_in_database[0]

        # Now check its attributes
        self.assertEquals(only_mall_in_database, mall)

        self.assertEquals(only_mall_in_database.nome, 'Shopping teste')
        self.assertEquals(only_mall_in_database.slug, 'shopping-teste')