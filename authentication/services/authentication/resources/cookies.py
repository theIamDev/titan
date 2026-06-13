from django.conf import settings

class Cookies():

    def __init__(self, response):
        self.response = response

    def set_cookie(self, key, value,max_age):
        self.response.set_cookie(
            key=key,
            value=value,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            secure=settings.AUTH_COOKIE_SECURE,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            path=settings.AUTH_COOKIE_PATH,
            max_age=max_age,
        )

    def delete_cookie(self, key):
        self.response.set_cookie(
            key=key,
            value="",
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            secure=settings.AUTH_COOKIE_SECURE,
            samesite=settings.AUTH_COOKIE_SAMESITE,
            path=settings.AUTH_COOKIE_PATH,
            max_age=0 
        )