# -*- coding: utf-8 -*-

from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django_stachoutils.middlewares import ExceptionUserInfoMiddleware


class ExceptionUserInfoMiddlewareTest(TestCase):
    rf = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        cls.anon = AnonymousUser()

    def test_middleware_no_user_request(self):
        request = self.rf.get('/ok/')
        ExceptionUserInfoMiddleware().process_exception(request, BaseException)
        self.assertNotIn('USERNAME', request.META)
        self.assertNotIn('USER_EMAIL', request.META)

    def test_middleware_anonymous_user(self):
        request = self.rf.get('/ok/')
        request.user = self.anon
        ExceptionUserInfoMiddleware().process_exception(request, BaseException)
        self.assertNotIn('USERNAME', request.META)
        self.assertNotIn('USER_EMAIL', request.META)

    def test_middleware_authenticated_user(self):
        request = self.rf.get('/ok/')
        request.user = self.user
        ExceptionUserInfoMiddleware().process_exception(request, BaseException)
        self.assertIn('USERNAME', request.META)
        self.assertIn('USER_EMAIL', request.META)
        self.assertEqual(request.META['USERNAME'], 'john')
        self.assertEqual(request.META['USER_EMAIL'], 'lennon@thebeatles.com')

    def test_middleware_call(self):
        def a_view(request):
            from django.http import HttpResponse
            return HttpResponse("Hello")
        request = self.rf.get('/ok/')
        middleware = ExceptionUserInfoMiddleware(a_view)
        response = middleware(request)
        self.assertEqual(response.content, b'Hello')
