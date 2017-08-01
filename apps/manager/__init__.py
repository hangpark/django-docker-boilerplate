"""
Site manager.

Basic app provided by the project to define services in the site.
"""

from django.core.exceptions import SuspiciousOperation, PermissionDenied
from django.http import Http404

default_app_config = 'apps.manager.apps.ManagerConfig'


class Custom404(Http404):
    """
    Custom error to generate 404 error in view logics.

    Used when requested page does not exist. You can pass a string into the
    parameter to show custom error message instead of default one.
    """

    pass


class Custom500(Exception):
    """
    Custom error to generate 500 error in view logics.

    Used when internal error occured. You can pass a string into the parameter
    to show custom error message instead of default one.
    """

    pass


class Custom403(PermissionDenied):
    """
    Custom error to generate 403 error in view logics.

    Used when user tries to access unauthorized page. You can pass a string into
    the parameter to show custom error message instead of default one.
    """

    pass


class Custom400(SuspiciousOperation):
    """
    Custom error to generate 400 error in view logics.

    Used when user request is invalid. You can pass a string into the parameter
    to show custom error message instead of default one.
    """

    pass
