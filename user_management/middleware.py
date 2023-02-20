from django.conf import settings


class CustomMiddleware(object):
    def __init__(self, get_response):
        """
        One-time configuration and initialisation.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        if 'next' in request.GET:
            settings.LOGIN_REDIRECT_URL = request.GET.get('next')
        return None

    def process_exception(self, request, exception):
        """
        Called when a view raises an exception.
        """
        print("process exception")
        return None

    def process_template_response(self, request, response):
        """
        Called just after the view has finished executing.
        """
        print("process template")
        return response
