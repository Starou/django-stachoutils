import logging
from django.test import RequestFactory, TestCase
from django.contrib.messages.storage.base import BaseStorage


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


class MessageHandlerTestCase(TestCase):
    def test_message_handler(self):
        logger = logging.getLogger("stachoutils.logger1")
        rf = RequestFactory()
        request = rf.get('/')
        request._messages = MessageStorage(request)

        logger.error("This is a error message", extra={'request': request})
        logger.info("This is a info message", extra={'request': request})  # ignored
        self.assertEqual([str(m) for m in request._messages], ["This is a error message"])

