import requests
import json
import os
import sendgrid
from flask import escape
from flask_cors import CORS, cross_origin
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@cross_origin()
def recebe_requisicao(request):
    request_form = request.form

    if request_form and 'inputNome' and 'inputSobrenome' and 'inputEmail' in request_form:
        nome = request_form['inputNome']
        sobrenome = request_form['inputSobrenome']
        email = request_form['inputEmail']

        resultado = cria_usuario_moodle(email,nome,sobrenome)

        if resultado == 'sucesso':
            return 'Solicitação recebida com sucesso.'
        else:
            print('RR:ERRO:CRIACAO_DE_USUARIO_FALHOU')
            return 'Erro, entre em contato com o administrador do sistema'
    else:
        print('RR:ERRO:PARAMETRO_NAO_ENCONTRADO')
        return 'Erro, Erro, ente em contato com o administrador do sistema'

def send_email(email, username, nome):
    sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

    message = Mail(
        from_email='aramos197442@gmail.com',
        to_emails=email,
        subject=nome+' sua conta no Moodle foi criada!',
        html_content="<strong>"+nome+"</strong> sua conta foi criada.<br>Segue:<br>Conta: "+username+"<br>Senha: "+os.environ.get('TEMP_PASS'))
    sg.send(message)

def cria_usuario_moodle(email,nome,sobrenome):
    token = os.environ.get('MOODLE_TOKEN')
    servidor = os.environ.get('MOODLE_SERVER')

    function = 'core_user_create_users'
    url = 'http://{0}/webservice/rest/server.php?wstoken={1}&wsfunction={2}&moodlewsrestformat=json'.format(servidor,token,function)

    email = email
    username = email.split("@")[0]
    
    users = {'users[0][username]': username,
            'users[0][email]': email,
            'users[0][lastname]': sobrenome,
            'users[0][firstname]': nome,
            'users[0][password]': os.environ.get('TEMP_PASS')}

    try:
        response= requests.post(url,data=users)
        if 'exception' in json.loads(response.text):
            print('Result: '+response.text)
            return 'Erro'
        else:
            print('Result: '+response.text)
            send_email(email,username,nome)
            return 'sucesso'
    except Exception as e:
        print(e)
        return 'Erro'