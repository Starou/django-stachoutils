import logging
from django.test import TestCase
from django_stachoutils.log import BufferingSMTPHandler
try:
    from unittest import mock
except:
    import mock


class BufferingSMTPHandlerTest(TestCase):
    mailhost = "my_smtp"
    fromaddr = "me@my_compagny.com"
    toaddrs = ["chris.mannix@redrock.org", "bob.ruth@bassocied-bhunters.com"]
    subject = "Concerning Daisy D."
    capacity = 10

    @mock.patch('smtplib.SMTP', autospec=True)
    def test_buffering_smtp_handler_flush(self, smtp_m):
        logger = logging.getLogger('test')
        logger.setLevel(logging.INFO)
        handler = BufferingSMTPHandler(self.mailhost, self.fromaddr, self.toaddrs,
                                       self.subject, self.capacity, fmt="%(levelname)-5s %(message)s")
        logger.addHandler(handler)

        logger.info(u"I am pleased to announce you that your bounty is ready to be collected.")
        handler.flush()
        smtp_m.assert_called_with(self.mailhost, 25)
        smtp_m().sendmail.assert_called_with(self.fromaddr, self.toaddrs,
            b'From: me@my_compagny.com\r\nTo: chris.mannix@redrock.org,bob.ruth@bassocied-bhunters.com\r\nSubject: Concerning Daisy D.\r\n\r\nINFO  I am pleased to announce you that your bounty is ready to be collected.\r\n')
        smtp_m().quit.assert_called_with()

