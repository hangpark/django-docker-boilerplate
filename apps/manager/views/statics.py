"""
Views for static pages.
"""

from .base import PageView


class MainPageView(PageView):
    """
    Main page view.
    """

    template_name = 'manager/main.jinja'


class ErrorView(PageView):
    """
    Custom error page view.

    Error handler calls this view. This error view supports site navigation.
    """

    status_code = 200

    def render_to_response(self, context, **response_kwargs):
        """
        Sets HTTP response code.
        """
        response_kwargs['status'] = self.status_code
        return super().render_to_response(context, **response_kwargs)
