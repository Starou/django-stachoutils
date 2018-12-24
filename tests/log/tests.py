import logging

from django.contrib.messages.storage.base import BaseStorage
from django.core import mail
from django.test import RequestFactory, TestCase


class MessageStorage(BaseStorage):
    """This is a basic messages storage since RequestFactory does not provide
       a complete request object according to settings.MIDDLEWARE.
    """
    def __init__(self, request, *args, **kwargs):
        self.messages = None
        super(MessageStorage, self).__init__(request, *args, **kwargs)

    def _get(self, *args, **kwargs):
        return self.messages, True

    def _store(self, messages, response, *args, **kwargs):
        if messages:
            self.messages = messages
        else:
            self.messages = None
        return []


class MessageHandlerTest(TestCase):
    def test_message_handler(self):
        logger = logging.getLogger("stachoutils.logger1")
        rf = RequestFactory()
        request = rf.get('/')
        request._messages = MessageStorage(request)

        logger.error("This is a error message", extra={'request': request})
        logger.info("This is a info message", extra={'request': request})  # ignored
        self.assertEqual([str(m) for m in request._messages], ["This is a error message"])


# Can't use @override_settings here since BufferingSMTPHandler is initialized
# with settings values.
class AdminEmailHandlerTest(TestCase):
    def test_admin_email_handler(self):
        logger = logging.getLogger("stachoutils.logger2")
        logger.error("This is a error message")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[Project Lambda][ERROR] : [MY PROJECT]')
        self.assertEqual(mail.outbox[0].body, 'This is a error message')

    def test_buffered_admin_email_handler(self):
        logger = logging.getLogger("stachoutils.logger3")
        for i in range(3):
            logger.error("This is error message #%d" % i)
        self.assertEqual(len(mail.outbox), 0)

        logger.handlers[0].flush()
        self.assertEqual(len(mail.outbox), 1)


class NullHandlerTest(TestCase):
    def test_null_handler(self):
        logger = logging.getLogger("stachoutils.logger4")
        logger.error("This error is not handled")
