from flask import Flask, request, jsonify, make_response
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


@app.route("/<json>/")
def index(json):
    response = make_response("test")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale'
    response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, OPTIONS, DELETE, GET'
    return response


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

    response = make_response(jsonify(data))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Headers'] = 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale'
    response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, OPTIONS, DELETE, GET'
    return response


@app.route("/matching/<input_data>/")
def matching_algo(input_data):
    for key, value in test_data.items():
        items = FormItem.query.filter((FormItem.name == key) & (FormItem.count <= value)).all()
        for item in items:
            print(item.name)

    response = make_response("done")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale'
    response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, OPTIONS, DELETE, GET'
    return response


@app.route("/login_check", methods=["POST"])
def login_check():
    email =  request.form["email"]
    password = request.form["password"]

    user = User.query.filter(User.email == email).first()
    if user:
        if user.check_password(password):
            response = make_response("yes")
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers[
                'Access-Control-Allow-Headers'] = 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale'
            response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, OPTIONS, DELETE, GET'
            return response

    response = make_response("no")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale'
    response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, OPTIONS, DELETE, GET'
    return response



@app.route("/registration_form", methods=["POST"])
def registration_form():
    data = {
      "name": request.form["name"],
      "email": request.form["email"],
      "ico": request.form["ico"],
      "contact_name": "Dominik Vagala",
    }

    user = User(data["name"], " ", " ")
    user.email = data["email"]
    user.ico = int(data["ico"])

    response = make_response("success")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale'
    response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, OPTIONS, DELETE, GET'
    return response




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
    body = "Organisation wants to have these items: " + list_of_items + "\n Order Id: " + str(order.id)
    recipient = u.email

    email_send(subject, body, recipient)

    response = make_response("success")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale'
    response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, OPTIONS, DELETE, GET'
    return response


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
        response = make_response("Order was not found")
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin,Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,locale'
        response.headers['Access-Control-Allow-Methods'] = 'POST, PUT, OPTIONS, DELETE, GET'
        return response


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