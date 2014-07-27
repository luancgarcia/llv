# -*- encoding: utf-8 -*-
import thread
from StringIO import StringIO
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse as url_reverse
from django.core.management import call_command
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from django.conf import settings
from utils.models import OrderedModel

@staff_member_required
def ajax_command(request, command):
    '''Executa os commands do django via ajax assincrono'''
    url = url_reverse('command', kwargs={'comando': command})
    context = {'comando': command,
               'url': url,
               'STATIC_URL': settings.STATIC_URL}
    return render_to_response("admin/ajax.html", context)

@staff_member_required
def command(request, comando):
    '''Executa o comando via manager'''
    comandos_disponiveis = ['submit_playlist', 'submit_radioschedule']

    def thread_handler(command):
        inicio = datetime.now().strftime('%H:%M:%S %d/%m')
        saida = StringIO()
        e = False
        try:
            call_command(command, stdout=saida)
        except Exception, e:
            pass
        saida.seek(0)
        print saida.read()
        # s = saida.read()
        # fim = datetime.now().strftime('%H:%M:%S %d/%m')
        # n = Notificacao()
        # n.tipo = 101
        # n.titulo = u'Executado comando %s' % command
        # n.detalhes = "%s Iniciado:<br/>%s" % (inicio, s.replace('\n', '<br/>'))
        # if e:
        #     n.detalhes += "<br/>ERRO:<br/>%s<br>" % str(e).replace('\n', '<br/>')
        #     n.tipo = 401
        # n.detalhes += "<br/>%s Finalizado." % fim
        # n.save()

    if comando in comandos_disponiveis:
        # p = Process(target=call_command, args=(comando, stdout=saida))
        thread.start_new_thread(thread_handler, (comando, ))
        # p.start()
        # p.map(call_command, [comando])
        context = {'resultado': 'Processo disparado e pode levar alguns minutos para ser concluído'}
    else:
        context = {'resultado': 'Comando indisponível'}

    return render_to_response("admin/commands/resultado.html", context)

@staff_member_required
@transaction.commit_on_success
def admin_move_ordered_model(request, direction, model_type_id, model_id):
    if direction == "up":
        OrderedModel.move_up(model_type_id, model_id)
    else:
        OrderedModel.move_down(model_type_id, model_id)

    ModelClass = ContentType.objects.get(id=model_type_id).model_class()

    app_label = ModelClass._meta.app_label
    model_name = ModelClass.__name__.lower()

    url = "/admin/%s/%s/" % (app_label, model_name)

    return HttpResponseRedirect(url)


def unescape(s):
    unicode_string = u"%s" % s
    return unicode_string.encode('ascii', 'xmlcharrefreplace')