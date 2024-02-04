import os
from flask import Flask, render_template
from flask_mail import Mail, Message



# Instanciando objeto app
app = Flask(__name__)

# Configuração dos dados do e-mail
app.config.update(
    DEBUG=os.getenv('DEBUG', default=True),
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=os.getenv('MAIL_PORT'),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS'),
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL'),
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'), 
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD_APP'),
)
mail = Mail(app)



def enviar_email_boas_vindas(nome, email):
    with app.app_context():
        msg = Message('Bem-vindo ao Nosso Serviço',
                    sender='merkaduapp@gmail.com',
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

