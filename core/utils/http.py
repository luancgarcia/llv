# -*- encoding: utf-8 -*-
try:
    import json
except:
    import simplejson as json
from django.http import HttpResponse, Http404

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group



def JSonResponse(response):
    return HttpResponse(json.dumps(response),
                        mimetype='application/javascript')

def APIAuth(request):
    '''Faz autenticação da API'''
    post = request.POST.get
    username = post('login')
    senha = post('senha')
    token = post('token')
    if not any([username, senha, token]):
        raise Http404

    user = None
    # Checa se existe uma sessao para aquele token
    if token:
        response = {'success': 0, 'Error_Message': u'Token de sessão inválido ou expirado'}
        try:
            sessao = Session.objects.get(pk=token)
        except Session.DoesNotExist:
            sessao = None

        # Se existir essa sessao tenta retornar o usuario, ou None
        if sessao:
            user_id = sessao.get_decoded().get('_auth_user_id')
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    pass

    # Se não encontrou usuario com os dados do token vamos procurar por usuario e senha
    if not user:
        if username or senha:
            response = {'success': 0, 'Error_Message': u'Usuário ou senha inválidos'}
            if username and senha:
                user = authenticate(username=username, password=senha)
                if user:
                    login(request, user)

    # Se ao fim de todas as tentativas conseguiu encontrar um usuário gera a resposta de success
    if user:
        response = {'success': 1,
                    'token': request.session.session_key,
                    'name': user.first_name,
                    'userID': user.id}

    return user, response