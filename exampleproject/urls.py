from django.conf.urls import url
from django.contrib import admin

from apps.manager.views import MainPageView, ErrorView

handler400 = ErrorView.as_view(template_name='error/400.jinja', status_code=400)
handler403 = ErrorView.as_view(template_name='error/403.jinja', status_code=403)
handler404 = ErrorView.as_view(template_name='error/404.jinja', status_code=404)
handler500 = ErrorView.as_view(template_name='error/500.jinja', status_code=500)

urlpatterns = [
    # Main page
    url(r'^$', MainPageView.as_view(), name='main'),

    # Basic app redirections
    url(r'^admin/', admin.site.urls),

    # Service redirections

    # Custom static pages
]
