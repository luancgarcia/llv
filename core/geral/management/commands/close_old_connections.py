# -*- encoding: utf-8 -*-
__author__ = 'jonatascd'

from django.db import close_old_connections
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = u'Fecha conexões com banco de dados que estejam sem uso'

    def handle(self, *args, **options):
        close_old_connections()