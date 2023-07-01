from django.contrib.auth import logout

class LogoutMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.force_logout_date and \
           request.session['LAST_LOGIN_DATE'] < request.user.force_logout_date:
            logout(request)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)

        response = self.get_response(request)
        return response
