from flask import Flask, request
from openai import OpenAI
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from models import *



app = Flask(__name__)



app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = '465'
app.config["MAIL_USERNAME"] = 'ekolo.bratislava@gmail.com'
app.config["MAIL_PASSWORD"] = 'yqnp fitd demx ymzx '
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_DEFAULT_SENDER '] = "no-reply@gma.sk"


mail = Mail(app)

test_data = {"Knihy": 50,
             "Dekorácie":60,
             "Platne": 50}


@app.route("/")
def index():
    email_sending()
    return "sd"


@app.route("/matching/<input_data>/")
def matching_algo(input_data):
    for key, value in test_data.items():
        items = FormItem.query.filter((FormItem.name == key) & (FormItem.count <= value)).all()
        for item in items:
            print(item.name)

    return "0"





def send_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route("/email/")
def email_sending():
    subject = "Test mail"
    recipient = "pravoslav.zilka@gmail.com"
    body = "Hello"


    msg = Message(subject=subject, sender="ekolo.bratislava@gmail.com", recipients=[recipient])
    msg.body = body
    mail.send(msg)

    return 'Email sent successfully!'



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)