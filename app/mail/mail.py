from flask_mail import Mail, Message

from app import app

mail = Mail(app)


def send_mail_without_template(receiver, subject, content):
    print('1111111111')

    msg = Message(
        subject,
        recipients=[receiver],
        # html=template,
        sender=app.config['MAIL_USERNAME']
    )
    print(receiver)

    msg.body = content

    mail.send(msg)



def send_mail_with_template(receiver, subject, template):
    msg = Message(
        subject,
        recipients=[receiver],
        html=template,
        sender=app.config['MAIL_USERNAME']
    )

    mail.send(msg)
