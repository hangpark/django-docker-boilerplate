"""
Basic views for site manager.
"""

import os

from django.contrib.auth.mixins import AccessMixin
from django.http import Http404
from django.views.generic import TemplateView

from apps.manager.constants import *
from apps.manager.models import Category, Service


class PermissionContextMixin(object):
    """
    Mixin that makes templates be able to use service permission constants.
    """

    def get_permission_context(self, context):
        """
        Adds basic 7 service permissions into the context.
        """
        context['PERM_NONE'] = PERM_NONE
        context['PERM_ACCESS'] = PERM_ACCESS
        context['PERM_READ'] = PERM_READ
        context['PERM_COMMENT'] = PERM_COMMENT
        context['PERM_WRITE'] = PERM_WRITE
        context['PERM_EDIT'] = PERM_EDIT
        context['PERM_DELETE'] = PERM_DELETE
        return context

    def get_context_data(self, **kwargs):
        """
        Sets context data.

        Gets data from :meth:`super` method and then adds basic service
        permissions by calling :meth:`get_permission_context`.
        """
        context = super().get_context_data(**kwargs)
        return self.get_permission_context(context)


class PermissionRequiredServiceMixin(AccessMixin):
    """
    Mixin to generate 403 error for unauthorized users.

    Stores the service object in `service` field if it exists. Then tests user
    permission for stored service and generates 403 error if user does not
    have.

    Required permission is saved in `required_permission` field and its default
    value is 'accessible'.
    """

    service_name = None
    required_permission = PERM_ACCESS
    raise_exception = True

    def get_service(self, request, *args, **kwargs):
        """
        Returns service from user's request.

        Basically it returns service which has same URL with `url` parameter of
        regular expression for user's request URL. If `url` parameter is not
        passed, then returns service which has same name with `service_name`.

        You can override this method to implement other ways to retrieve
        a desired service.
        """
        if (kwargs.get('url', None)):
            url = os.path.join('/', kwargs['url'])
            return Service.objects.filter(url=url).first()
        return Service.objects.filter(name_ko=self.service_name).first()

    def has_permission(self, request, *args, **kwargs):
        """
        Returns whether user has permission to use the service.

        404 error would be occured if :meth:`get_service` failed to retrieve.
        Otherwise, it saves the service object in `service` field.
        """
        service = self.get_service(request, *args, **kwargs)
        if not service:
            raise Http404
        self.service = service
        return service.is_permitted(request.user, self.required_permission)

    def dispatch(self, request, *args, **kwargs):
        """
        Pre-protects unauthorized user before view logic has been executed.
        """
        if not self.has_permission(request, *args, **kwargs):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class NavigatorMixin(object):
    """
    Mixins to pass site navigator to the context.

    Site navigator is defined by hierarchy structure between categories and
    services.
    """

    def get_context_data(self, **kwargs):
        """
        Adds all categories together with their user-accessible services into
        the context.
        """
        context = super().get_context_data(**kwargs)
        context['navigator'] = []
        categories = Category.objects.all()
        for category in categories:
            context['navigator'].append({
                'category': category,
                'services': Service.objects.filter(
                    category=category).accessible_for(self.request.user),
            })
        return context


class PageView(NavigatorMixin, TemplateView):
    """
    Page view.

    This view is for displaying static pages or services which do not need
    authorization. Site navigation is provided.

    Individual page should be a service. Service is not determined by which
    view it uses, but is when it is registered into database as a
    :class:`Service` object. Thus, contents served by :class:`PageView` can
    also be registered as a service.
    """

    pass


class ServiceView(
        PermissionContextMixin, PermissionRequiredServiceMixin, PageView):
    """
    Basic service view.

    Each view of services is implemented by extending this view in usual.
    Authorization and few more context is already implemented by mixins.

    You can determine the name of related service at `service_name`. If URL
    pattern regular expression does not have `url` parameter, please do so.

    You can determine the minimum permission to use this view at
    `required_permission`. Users do not have it would be moved to 403 error
    page. More complicate logics can be implemented by overriding this.
    """

    def get_context_data(self, **kwargs):
        """
        Adds service object into the context.
        """
        context = super().get_context_data(**kwargs)
        context['service'] = self.service
        return context
