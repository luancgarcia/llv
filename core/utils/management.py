# -*- encoding: utf-8 -*-
from datetime import datetime

from django.core.management import BaseCommand

class BaseCommand(BaseCommand):

    def log(self, str=None, header=False, linha=False, faixa=False):
        data_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _linha = "-----------------------------------------------------------"
        _faixa = "==========================================================="

        if linha:
            msg = _linha
        elif faixa:
            msg = _faixa
        elif header:
            self.log(faixa=True)
            self.log(str)
            self.log(faixa=True)
            return
        else:
            msg = str

        self.stdout.write("[%s] %s" % (data_str, msg))