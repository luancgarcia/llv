# -*- encoding: utf-8 -*-
import re
import simplejson as json

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.http import HttpResponse
from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import date as _date
from django.template.defaultfilters import slugify
from django.core.validators import validate_email
from django.conf import settings


def dictfetchall(cursor):
    ''' Returns all rows from a cursor as a dict '''
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def jsonResponse(obj):
    return HttpResponse(json.dumps(obj), content_type="application/json")

def trataString(string):
    re_pattern = re.compile(u'[^\u0000-\uD7FF\uE000-\uFFFF]', re.UNICODE)
    filtered_string = re_pattern.sub(u'\uFFFD', string)
    return filtered_string

def validate_only_one_instance(obj):
    model = obj.__class__
    if (model.objects.count() > 0 and obj.id != model.objects.get().id):
        raise ValidationError(u"Limitado a apenas 1 instância de %s" % model.__name__)

def ajusta_data(data):
    dias = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
    data_longa = _date(data, 'w d/m/Y - H:i')
    dia = data_longa.split(' ')[0][:3]
    restante = data_longa.split(' ')[1:]
    return dias[int(dia)] + ' ' + ' '.join(restante)

def valida_email(email, verbose=True):
    try:
        validate_email(email)
        return True
    except ValidationError, e:
        if verbose:
            print '%s -- %s' % (e, email)
        return False

def smtp_on(fecha=False, conexao=None):
    s = conexao
    if fecha and s:
        s.close()
        s = None
    else:
        s = SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        try:
            s.ehlo()
            # s.starttls()
            # s.ehlo
            # s.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        except Exception, e:
            print 'ERRO ao conectar via SMTP: %s' % e
            s.close()
            s = None
    return s

def envia_email_smtp(contexto, s):
    from_email = settings.EMAIL_FROM
    email = contexto['email']

    corpo = MIMEMultipart('alternative')
    corpo['Subject'] = "Convite Bolão Campeão SporTV"
    corpo['From'] = from_email
    corpo['To'] = email

    # monta mensagem em plain e html
    texto = """\
        SporTV - Bolão SporTV\n
        -----------\n
        %(nome)s convidou você para participar do Bolão Campeão SporTV - 2014 e de seu Bolão pessoal:\n
        %(bolao_nome)s\n
        '%(mensagem)s'\n
        PARTICIPE AGORA - http://bolaosportv.globo.com/bolao/%(bolao_slug)s/?convite_hash=%(hash)s\n
        \n\n
        Atenciosamente, Equipe Bolão Campeão SporTV - 2014\n\n
    """ % contexto

    html = """\
    <html><head>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    <title>SporTV - Bol&atilde;o SporTV</title>
    </head>
    <body bgcolor="#efefef" leftmargin="0" topmargin="0" rightmargin="0" bottommargin="0" marginwidth="0" marginheight="0">
    <br>
        <table width="550" border="0" cellspacing="0" cellpadding="0" align="center" style="word-break:break-all;">
        <tr>
            <td bgcolor="#ffffff" width="20">&nbsp;</td>
            <td bgcolor="#ffffff" width="510">
                <font face="Arial" size="4" color="#005711">
                    <strong>Bol&atilde;o Campe&atilde;o SporTV - 2014</strong>
                </font><br><br>
                <font face="Arial" size="2" color="#666666">
                    %(nome)s convidou voc&ecirc; para participar do
                    <font face="Arial" size="2" color="#005711">
                        <strong>Bol&atilde;o Campe&atilde;o SporTV - 2014</strong>
                    </font>e de seu Bol&atilde;o pessoal
                    <font face="Arial" size="2" color="#005711">
                        <strong>%(bolao_nome)s</strong>.
                    </font>
                </font><br><br>
                <font face="georgia" size="2" color="#666666">
                    <i>&quot;%(mensagem)s&quot;</i><br><br>
                </font>
                    <a href="http://bolaosportv.globo.com/bolao/%(bolao_slug)s/?convite_hash=%(hash)s" title="Participe Agora!" style="text-decoration:none;" target="_blank">
                        <font face="Arial" size="5" color="#005711">
                            <strong>PARTICIPE AGORA</strong>
                        </font>
                    </a>
                <br><br>
                <font face="Arial" size="2" color="#666666">
                    Atenciosamente,<br>
                    <strong>Equipe Bol&atilde;o Campe&atilde;o SporTV - 2014</strong>
                </font>
                <br><br>
            </td>
            <td bgcolor="#ffffff" width="20">&nbsp;</td>
        </tr>
    </table></body></html>
    """ % contexto

    parte_plain = MIMEText(texto.encode('utf-8'), 'plain')
    parte_html = MIMEText(html.encode('utf-8'), 'html')

    corpo.attach(parte_plain)
    corpo.attach(parte_html)

    # dispara o email
    try:
        s.sendmail(from_email, email, corpo.as_string())
        enviado = True
    except Exception, e:
        print 'ERRO ao enviar email: %s' % e
        enviado = False

    return enviado

def slug_upload(value):
   value.name = '/'.join(['.'.join([slugify(j) for j in i.split('.')]) for i in value.name.split('/')])

def separa_tres_colunas(lista):
    tamanho = len(lista)
    retorno = lista
    if tamanho > 3:
        num = tamanho / 3
        um = lista[:num]
        dois = lista[num:num * 2]
        tres = lista[num * 2:]
        colunas = zip(um, dois, tres)
        retorno = []
        for coluna in colunas:
            for c in coluna:
                retorno.append(c)
    return retorno

def dict_mais_vistas(item):
    return {'id': str(int(item.id)),
            'nome': item.nome,
            'numero': item.vistas}
