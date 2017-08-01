"""
Models of service manager.
"""

from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from .constants import *

# Basic service permissions
PERMISSION_CHOICES = (
    (PERM_NONE, _("No permission")),
    (PERM_ACCESS, _("Can access")),
    (PERM_READ, _("Can read")),
    (PERM_COMMENT, _("Can comment")),
    (PERM_WRITE, _("Can write")),
    (PERM_EDIT, _("Can edit")),
    (PERM_DELETE, _("Can delete")),
)


class Category(models.Model):
    """
    Category model.

    Category wraps a set of related services. Category is at the top level of
    the sitemap.
    """

    name = models.CharField(
        _("Category name"),
        max_length=32, unique=True)

    is_open = models.BooleanField(
        _("Shown in sitemap"),
        default=True)

    class Meta:
        ordering = ['is_open']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns URL of the first service of the category.

        Categories are not connected with a specific view initially. So URL for
        a category is set as of first service in it.
        """
        s = self.service_set.first()
        if s:
            return s.get_absolute_url()
        return '/'


class ServiceQuerySet(models.QuerySet):
    """
    Custom queryset of :class:`Service`.

    This supports filtering user-accessible services.
    """

    def accessible_for(self, user):
        """
        Returns filtered queryset by user-accessibility.
        """
        # For administrators
        if user.is_superuser:
            return self

        # For normal users
        q = Q(max_permission_anon__gte=PERM_ACCESS)
        if user.is_authenticated():
            q |= Q(max_permission_auth__gte=PERM_ACCESS)
        q |= Q(
            groupservicepermission__permission__gte=PERM_ACCESS,
            groupservicepermission__group__in=user.groups.all())
        q &= Q(is_closed=False)
        return self.filter(q).distinct()


class ServiceManager(models.Manager):
    """
    Custom manager of :class:`Service`.

    This supports filtering user-accessible services.
    """

    def get_queryset(self):
        return ServiceQuerySet(self.model, using=self._db)

    def accessible_for(self, user):
        """
        Returns filtered queryset by user-accessibility.
        """
        return self.get_queryset().accessible_for(user)


class Service(models.Model):
    """
    Service model.

    Service is an independent function of the site. User has specific permission
    for using each service and this model supports authorization. Each service
    can be implemented by extending this class to adapt powerful authorization
    support.

    There are 7 service permissions defined in `apps.service.constants`. These
    have parent-child relationship so those who have higher permission also
    have lower permissions. Also, if user has multiple permissions, highest
    permission among them would be considered as the permission.
    """

    name = models.CharField(
        _("Service name"),
        max_length=32, unique=True)

    category = models.ForeignKey(
        Category,
        verbose_name=_("Category of service"))

    url = models.CharField(
        _("URL of service"),
        max_length=32, default='/',
        help_text=_("Please write down the path without domain. Follow the format like /aaa/bbb."))

    level = models.IntegerField(
        _("Display order"),
        default=1,
        help_text=_("Ordering for services of same category"))

    description = models.TextField(
        _("Service description"),
        blank=True)

    is_closed = models.BooleanField(
        _("Is closed"),
        default=False,
        help_text=_("Every users except admins cannot access if checked."))

    max_permission_anon = models.IntegerField(
        _("Maximum permission for not logged-in users"),
        choices=PERMISSION_CHOICES, default=PERM_NONE)

    max_permission_auth = models.IntegerField(
        _("Maximum permission for logged-in users"),
        choices=PERMISSION_CHOICES, default=PERM_READ)

    permitted_groups = models.ManyToManyField(
        'auth.Group',
        through='GroupServicePermission', related_name='permitted_services',
        verbose_name=_("Group's permissions"))

    # Custom manager
    objects = ServiceManager()

    class Meta:
        ordering = ['category', 'level']
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

    def __str__(self):
        return self.category.name + "/" + self.name

    def get_absolute_url(self):
        return self.url

    def is_permitted(self, user, permission=PERM_ACCESS):
        """
        Returns whether user has given permission.
        """
        if user.is_superuser:
            return True
        if self.is_closed:
            return False
        if permission <= self.max_permission_anon:
            return True
        if permission <= self.max_permission_auth:
            return user.is_authenticated()
        return (user.groups.all() & self.permitted_groups.filter(
            groupservicepermission__permission__gte=permission)).exists()


class GroupServicePermission(models.Model):
    """
    Intermediate model to manage permissions between :class:`Group` and
    :class:`Service`.

    This manages permission of given group in a many-to-many relation between
    groups and services.
    """

    group = models.ForeignKey(
        'auth.Group',
        on_delete=models.CASCADE,
        verbose_name=_("Group"))

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name=_("Service"))

    permission = models.IntegerField(
        _("Permission"),
        choices=PERMISSION_CHOICES, default=PERM_ACCESS)

    class Meta:
        ordering = ['service', 'permission', 'group']
        verbose_name = _('Group-Service Permission')
        verbose_name_plural = _('Group-Service Permissions')

    def __str__(self):
        return "%s - %s - %s" % (self.service, self.permission, self.group)
