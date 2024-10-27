from flask import Flask, request, jsonify
from threading import Thread
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

from database import db_session
from models import *



app = Flask(__name__)



app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = '465'
app.config["MAIL_USERNAME"] = 'ekolo.bratislava@gmail.com'
app.config["MAIL_PASSWORD"] = 'yqnp fitd demx ymzx '
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)

test_data = {"Knihy": 50,
             "Dekorácie":60,
             "Platne": 50}


@app.route("/")
def index():
    email_sending()
    return "sd"


@app.route("/load-data")
def load_data():
    data = [
  {
    "parent_category": "furniture",
    "products": [
      {
        "name": "lamp",
        "available_amount": 50
      },
      {
        "name": "beds",
        "available_amount": 50
      }
    ]
  },
  {
    "parent_category": "elektro",
    "products": [
      {
        "name": "pc",
        "available_amount": 50
      },
      {
        "name": "flashlight",
        "available_amount": 50
      }
    ]
  }
]

    return jsonify(data)


@app.route("/matching/<input_data>/")
def matching_algo(input_data):
    for key, value in test_data.items():
        items = FormItem.query.filter((FormItem.name == key) & (FormItem.count <= value)).all()
        for item in items:
            print(item.name)

    return 0


@app.route("/login_check")
def login_check():
    data = { "email": "d.vagala@gmail.com",
            "password": "asdfasdfa"}

    user = User.query.filter(User.email == data["email"]).first()
    if user:
        if user.check_password(data["password"]):
            return "yes"


    return "no"


@app.route("/registration_form")
def registration_form():
    data = {
      "name": "Katolicka charita",
      "email": "d.vagala@gmail.com",
      "ico": "23432",
      "contact_name": "Dominik Vagala",
    }

    user = User(data["name"], " ", " ")
    user.email = data["contact_name"]
    user.ico = int(data["ico"])

    return "success"




@app.route("/receive")
def receive_order():
    data = {
      "organization_email": "pravoslav.zilka@gmail.com",
      "products": [
        {
          "name": "lamp",
          "reserved_amount": 50
        },
        {
          "name": "beds",
          "reserved_amount": 50
        }
      ]
    }

    email = data["organization_email"]
    products_dict = {product["name"]: product["reserved_amount"] for product in data["products"]}

    list_of_items = ""

    u = User.query.filter(User.email == email).first()
    order = Order()
    order.user = u
    for product, value in products_dict.items():
        order_item = OrderItem(product, value)
        order_item.order = order
        db_session.add(order_item)
        list_of_items += f"\n{product} of value {value} "

    db_session.add(order)
    db_session.commit()

    #send email

    subject = f"The {u.name} organization have sent material request"
    body = "Organisation wants to have these items: " + list_of_items + "\n Order Id: " + order.id
    recipient = u.email

    email_send(subject, body, recipient)


    return "success"


@app.route("/confirm-order")
def confirm_order():
    data = {
        "order_id": "1",
        "organization_email": "pravoslav.zilka@gmail.com",
        "products": [
            {
                "name": "lamp",
                "reserved_amount": 50
            },
            {
                "name": "beds",
                "reserved_amount": 50
            }
        ]
    }

    order_id = data["order_id"]
    products_dict = {product["name"]: product["reserved_amount"] for product in data["products"]}

    order = Order.query.filter(Order.id == order_id).first()

    if not order:
        return "failed, order wasn't found"


    for item in order.order_items:
        for product, value in products_dict.items():
            if product == item.name:
                item.count = value

    db_session.commit()

    subject = "Your material request have been confirmed"
    body = "Please pick it up on 11 of November 2024 "
    recipient = order.user.email

    email_send(subject, body, recipient)


    return "success"



def send_email(app, msg):
    with app.app_context():
        mail.send(msg)



def email_send(subject, body, recipient):

    msg = Message(subject=subject, sender="ekolo.bratislava@gmail.com", recipients=[recipient])
    msg.body = body
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