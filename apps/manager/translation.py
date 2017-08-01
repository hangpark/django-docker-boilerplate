"""
Modules for i18n of service manager.

Supported by `django-modeltranslation`.
"""

from modeltranslation.translator import TranslationOptions, register

from .models import Category, Service


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """
    I18n support of :class:`Category` model.
    """

    fields = ('name',)


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    """
    I18n support of :class:`Service` model.
    """

    fields = ('name',)
