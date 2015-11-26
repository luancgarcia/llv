# -*- encoding: utf-8 -*-
import thread
from StringIO import StringIO
from datetime import datetime
import traceback

from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse as url_reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.management import call_command
from django.conf import settings

from geral.models import Log
from utils.functions import jsonResponse


@staff_member_required
def ajax_command(request, command):
    '''Executa os commands do django via ajax assincrono'''
    url = url_reverse('command', kwargs={'comando': command})
    context = {'comando': command,
               'url': url,
               'STATIC_URL': settings.STATIC_URL}
    return render_to_response("admin/commands/ajax.html", context)


@staff_member_required
def command(request, comando):
    '''Executa o comando via manager'''
    comandos_disponiveis = ['atualiza_lojas', 'atualiza_ranking', 'expira_itens_vencidos']

    def thread_handler(command):
        # inicio = datetime.now().strftime('%H:%M:%S %d/%m')
        saida = StringIO()
        e = False
        try:
            call_command(command, stdout=saida)
        except Exception, e:
            # trace = traceback.format_exc()
            print e
        # saida.seek(0)
        # s = saida.read()

    if comando in comandos_disponiveis:
        # p = Process(target=call_command, args=(comando, stdout=saida))
        thread.start_new_thread(thread_handler, (comando, ))
        # p.start()
        # p.map(call_command, [comando])
        context = {'resultado': 'Processo disparado e pode levar alguns minutos para ser concluído'}

    else:
        context = {'resultado': 'Comando indisponível'}

    return jsonResponse(context)

# def recuperar_login(request):
#     return