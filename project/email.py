from flask import abort
from flask_mail import Message
from project import mail
from project import app


def send_email(email, subject, html):
    msg = Message()
    msg.sender = app.config['MAIL_USERNAME']
    msg.recipients = [email]
    msg.subject = subject
    msg.html = html
    with app.app_context():
        try:
            mail.send(msg)
        except:
            abort(500)
