"""
Site manager application.
"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ManagerConfig(AppConfig):
    """
    Settings for site manager application.
    """

    name = 'apps.manager'
    verbose_name = _("Site Manager")
