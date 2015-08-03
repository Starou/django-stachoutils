# -*- coding: utf-8 -*-

import logging
import logging.handlers
import string
from django.core import mail
from django.conf import settings
from django.contrib import messages


levelname_to_int = {
    'DEBUG': messages.DEBUG,
    'INFO': messages.INFO,
    'WARNING': messages.WARNING,
    'ERROR': messages.ERROR,
}


# Python < 2.7.
class NullHandler(logging.Handler):
    def emit(self, record):
        pass


# http://www.red-dove.com/python_logging.html
class BufferingSMTPHandler(logging.handlers.BufferingHandler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, capacity):
        logging.handlers.BufferingHandler.__init__(self, capacity)
        self.mailhost = mailhost
        self.mailport = None
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.setFormatter(logging.Formatter("%(asctime)s %(levelname)-5s %(message)s"))

    def flush(self):
        if len(self.buffer) > 0:
            try:
                import smtplib
                port = self.mailport
                if not port:
                    port = smtplib.SMTP_PORT
                smtp = smtplib.SMTP(self.mailhost, port)
                msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (
                    self.fromaddr, string.join(self.toaddrs, ","), self.subject)
                for record in self.buffer:
                    s = self.format(record)
                    print s
                    msg = msg + s + "\r\n"
                smtp.sendmail(self.fromaddr, self.toaddrs, msg)
                smtp.quit()
            except:
                for record in self.buffer:
                    self.handleError(record)
            self.buffer = []


class BaseEmailHandler(logging.Handler):
    """Beneficie de la conf SMTP dans settings par rapport à logging.handlers.SMTPHandler. """
    def __init__(self, subject=""):
        """Allow one to set the subject in settings.LOGGING DictConfig. """
        logging.Handler.__init__(self)
        self.subject = subject

    def emit(self, record):
        subject = u'%s[%s] : %s' % (settings.EMAIL_SUBJECT_PREFIX, record.levelname, self.subject)
        message = record.msg
        mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, self.recipient_list,
                       fail_silently=True)


class AdminEmailHandler(BaseEmailHandler):
    def emit(self, record):
        self.recipient_list = [email for name, email in settings.ADMINS]
        BaseEmailHandler.emit(self, record)


class BufferingAdminEmailHandler(BufferingSMTPHandler):
    def __init__(self, subject="", capacity=1000):
        BufferingSMTPHandler.__init__(self, settings.EMAIL_HOST, settings.SERVER_EMAIL,
                                      [email for name, email in settings.ADMINS],
                                      subject, capacity)

    def flush(self):
        if len(self.buffer) > 0:
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (
                self.fromaddr,
                string.join(self.toaddrs, ","),
                self.subject)
            body = "\r\n".join([self.format(r) for r in self.buffer])
            email = mail.EmailMessage(self.subject, msg + body, self.fromaddr, self.toaddrs)
            email.send()
            self.buffer = []


class MessagelHandler(logging.Handler):
    """An handler proxiing to messages. """

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        messages.add_message(record.request, levelname_to_int[record.levelname], record.getMessage())
