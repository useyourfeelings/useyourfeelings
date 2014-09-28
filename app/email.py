from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['UYF_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['UYF_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    print('xcc send_email')
    print('%r %r' %(app.config['UYF_MAIL_SENDER'], to))
    
    msg.charset = 'utf8' #xiongchen20140811
    
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
