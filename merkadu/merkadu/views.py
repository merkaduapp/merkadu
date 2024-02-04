from django.shortcuts import render, redirect
from allauth.account.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from flask import Flask, render_template
from flask_mail import Mail, Message
from django.views.decorators.csrf import csrf_protect
import requests
from urllib.parse import quote




app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='merkaduapp@gmail.com',  # Substitua pelo seu endereço de e-mail
    MAIL_PASSWORD='ryhr bflx mxzc bvri'  # Substitua pela sua senha
)
mail = Mail(app)



class CustomLoginView(LoginView):
    template_name = 'client/multilogin.html'  # Defina o seu template personalizado


class LoginRecovery(LoginView):
    template_name = 'client/password_recovery.html'  # Defina o seu template personalizado



def enviar_email_boas_vindas(nome, email):
    with app.app_context():
        msg = Message('Bem-vindo ao Nosso Serviço',
                    sender='merkaduapp@gmail.com',  # Substitua pelo seu endereço de e-mail
                    recipients=[email])
        msg.html = f'''
            <html>
            <head></head>
            <body>
                <p>Olá {nome},</p>
                 <p>Bem-vindo ao nosso serviço! Modernize o seu negócio!</p>
                <p>Para criar a sua conta, clique <a href="http://127.0.0.1:8000/register/">aqui</a>.</p>
                <p>Obrigado!</p>
            </body>
            </html>
        '''
        mail.send(msg)

def enviar_whatsapp(nome, email):
    message = f'Olá {nome}, tudo bem ?, Eu sou o Kadu! enviamos no seu e-mail {email} o link para criar a sua conta no merkadu app, caso tenha alguma dúvida, estou aqui!'
    api_key = "rAW5cr2wdxKc"
    phone = "+5547999911656"
    try:
        requests.get(
            url=f"https://api.textmebot.com/send.php?recipient={phone}&apikey={api_key}&text={message}"
        )
    except Exception as e:
        print("Erro no envio do WhatsApp")
    



@csrf_protect
def processar_formulario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        phone = f"+55{request.POST.get('telefone')}"


        # Aqui você pode validar os dados do formulário conforme necessário

        # Envie o e-mail de boas-vindas
        enviar_email_boas_vindas(nome, email)
        enviar_whatsapp(nome, email)

        # Redirecione ou faça o que for necessário após o envio do e-mail
        return HttpResponseRedirect('/')
    else:
        # Lógica para tratamento de método GET, se necessário
        pass