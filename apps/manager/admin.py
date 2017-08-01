"""
Settings for admin pages of site manager.
"""

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Category, GroupServicePermission, Service


class CategoryAdmin(TranslationAdmin):
    """
    Custom admin for :class:`Category` class.

    I18n is supported with user-friendly interface by `django-modeltranslation`.
    """

    pass


class ServiceAdmin(TranslationAdmin):
    """
    Custom admin for :class:`Service` class.

    I18n is supported with user-friendly interface by `django-modeltranslation`.
    """

    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(GroupServicePermission)
