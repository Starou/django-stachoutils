from builtins import str
from builtins import object


# https://gist.github.com/sidmitra/646372
class ExceptionUserInfoMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        try:
            # TODO replace with `is_authenticated` attribute when support
            # for django < 1.10 is dropped and django-2.0 is supported.
            if request.user.is_authenticated():
                request.META['USERNAME'] = str(request.user.username)
                request.META['USER_EMAIL'] = str(request.user.email)
        except:
            pass
