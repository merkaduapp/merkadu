from allauth.account.views import LoginView
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
import requests
from utils import enviar_email_boas_vindas



class CustomLoginView(LoginView):
    template_name = 'client/multilogin.html'


class LoginRecovery(LoginView):
    template_name = 'client/password_recovery.html' 



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
        # Envie o e-mail de boas-vindas
        enviar_email_boas_vindas(nome, email)
        enviar_whatsapp(nome, email)

        return HttpResponseRedirect('/')
    else:
        pass