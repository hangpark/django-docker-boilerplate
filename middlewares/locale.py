"""
Middleware to set user's locale.
"""

from django.conf import settings
from django.utils import translation
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin


class SessionBasedLocaleMiddleware(MiddlewareMixin):
    """
    This middleware sets the locale of an user as the value of ``lang`` via
    GET parameter.

    ``lang`` value is saved in user's session as ``language`` to maintain its
    configuration.

    This code is modified from
    https://djangosnippets.org/snippets/1948/ to fit with Django 1.10.
    """

    def process_request(self, request):
        """
        Translates contents to a language passed by ``lang`` via GET parameter
        or configured as ``language`` in user's session.

        This methods sets the locale from the request if any language code is
        not given. Also, it stores the given language in user's session if
        the language is passed via GET parameter.
        """
        if request.method == 'GET' and 'lang' in request.GET:
            language = request.GET['lang']
            request.session['language'] = language
        elif 'language' in request.session:
            language = request.session['language']
        else:
            language = translation.get_language_from_request(request)
        for lang in settings.LANGUAGES:
            if lang[0] == language:
                translation.activate(language)

        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        """
        Returns the translated response.
        """
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
