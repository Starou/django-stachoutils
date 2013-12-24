# https://gist.github.com/sidmitra/646372
class ExceptionUserInfoMiddleware(object):
    """
    Adds user details to request context on receiving an exception, so that they show up in the error emails.
    Add to settings.MIDDLEWARE_CLASSES and keep it outermost(i.e. on top if possible). This allows
    it to catch exceptions in other middlewares as well.
    """
    
    def process_exception(self, request, exception):
        """
        Process the exception.

        :Parameters:
        - `request`: request that caused the exception
        - `exception`: actual exception being raised
        """
        
        try:
            if request.user.is_authenticated():
                request.META['USERNAME'] = str(request.user.username)
                request.META['USER_EMAIL'] = str(request.user.email)
        except:
            pass
