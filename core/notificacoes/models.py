# -*- encoding: utf-8 -*-

from django.db import models
from django.conf import settings

from utils.models import BaseModel, EditorialModel
from utils.custom_email import TemplatedEmail
from lojas.models import Loja


class BaseNotificacao(EditorialModel):
    mensagem = models.CharField(u'Mensagem', null=True, blank=True,
                                max_length=255)
    lida = models.BooleanField(u'Lida?', default=False)

    class Meta:
        abstract = True
        verbose_name = u'Base da Notificação'
        verbose_name_plural = u'Base das Notificações'
        ordering = ('-data_criacao',)


class Notificacao(BaseNotificacao):
    resolvida = models.BooleanField(u'Resolvida?', default=False)
    oferta = models.ForeignKey('geral.Oferta', verbose_name=u'Oferta',
                               null=True,
                               related_name='notificacoes', blank=True)
    solicitante = models.ForeignKey('geral.Perfil', verbose_name=u'Autor',
                                    blank=True, null=True,
                                    related_name='solicitante')
    responsavel = models.ForeignKey('geral.Perfil', null=True, blank=False,
                                    verbose_name=u'Marketing responsável',
                                    related_name='responsavel')
    enviada_mkt = models.BooleanField(u'Enviada para o marketing?',
                                      default=False)
    enviada_lojista = models.BooleanField(u'Enviada para o lojista?',
                                          default=False)

    class Meta:
        verbose_name = u'Notificação'
        verbose_name_plural = u'Notificações'

    def __unicode__(self):
        return u'%s' % self.oferta

    def save(self, *args, **kwargs):
        if not self.mensagem:
            self.mensagem = u'Nova oferta para aprovacao - %s' % self.oferta
        super(Notificacao, self).save(*args, **kwargs)

    def notifica_criacao(self):
        if self.responsavel and self.responsavel.user.email:
            try:
                para = settings.NOTIFICACAO + [self.responsavel.user.email]
                TemplatedEmail(para, self.mensagem, 'email/notificacao.html',
                               self.to_dict(), send_now=True)
                self.enviada_mkt = True
                self.save()
            except:
                raise

    def notifica_aprovacao(self):
        autor = self.solicitante
        if autor and autor.user.email:
            assunto = u'Sua oferta foi aprovada e publicada'
            try:
                para = settings.NOTIFICACAO + [autor.user.email]
                TemplatedEmail(para, assunto, 'email/aprovacao.html',
                               self.to_dict(), send_now=True)
                self.enviada_lojista = True
                self.resolvida = True
                self.lida = True
                self.save()
            except:
                raise

    def to_dict(self):
        return {'id': self.id,
                'mensagem': self.mensagem,
                'oferta': self.oferta.to_dict(),
                'lojista': self.solicitante}



class Solicitacao(BaseNotificacao):
    MENSAGEM_DEFAULT = u'As pessoas estão buscando ofertas da sua loja.'

    nome = models.CharField(u'Nome', null=True, blank=False, max_length=250)
    email = models.CharField(u'E-mail', null=True, blank=False, max_length=250)
    loja = models.ForeignKey(Loja, verbose_name=u'Loja', null=True,
                             blank=True, related_name='solicitacoes')
    enviada = models.BooleanField(u'Enviada?', default=True)
    respondida = models.BooleanField(u'Respondida?', default=False)

    class Meta:
        verbose_name = u'Solicitação de Loja'
        verbose_name_plural = u'Solicitações de Lojas'

    def __unicode__(self):
        return u'%s (%s) - %s' % (self.nome, self.email, self.loja)

    def save(self, *args, **kwargs):
        if not self.mensagem:
            self.mensagem = self.MENSAGEM_DEFAULT
        super(Solicitacao, self).save(*args, **kwargs)

    def responde_solicitacao(self):
        loja = self.loja
        assunto = u'Novidades da %s' % loja.nome
        contexto = {'nome': self.nome,
                    'loja': loja.nome,
                    'shopping_slug': loja.shopping.slug}
        try:
            para = self.email
            TemplatedEmail(para, assunto, 'email/resposta_solicitacao.html',
                           contexto, send_now=True)
            self.lida = True
            self.respondida = True
            self.save()
        except:
            raise

    def dispara_solicitacao(self, contexto, mkt_mails, lojistas_mails):
        try:
            para = settings.NOTIFICACAO + mkt_mails + lojistas_mails
            TemplatedEmail(para, contexto['assunto'],
                           'email/solicitacao.html', contexto, send_now=True)
            return True
        except:
            self.enviada = False
            return False

    def processa_nao_enviados(self):
        from geral.models import Perfil
        loja = self.loja
        loja_dict = loja.to_dict()
        mkt_lojistas = Perfil.objects.filter(shopping=loja.shopping)
        mkts = mkt_lojistas.filter(tipo=Perfil.MARKETING)
        mkt_mails = [m.user.email for m in mkts]
        lojistas = mkt_lojistas.filter(tipo=Perfil.LOJISTA)
        lojistas_mails = [l.user.email for l in lojistas]

        contexto = {'nome': self.nome,
                    'email': self.email,
                    'loja': loja_dict,
                    'assunto': u'LLV - Solicitação de loja %s' % loja_dict['nome'],
                    'sucesso': False}

        self.dispara_solicitacao(contexto, mkt_mails, lojistas_mails)
