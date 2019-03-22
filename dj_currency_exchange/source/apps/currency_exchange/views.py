"""
doc string goes here
"""

__all__ = ['HomePage', 'ProviderList']

# Standard library imports.

# Related third party imports.
from django.views.generic import TemplateView
from django.http import HttpResponse

# Local application/library specific imports.
from .models import Provider
from .tasks import provider_load_data_task


class HomePage(TemplateView):
    template_name = 'currency_exchange/home_page/base.html'


class ProviderList(TemplateView):
    template_name = 'currency_exchange/provider_page/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['providers'] = Provider.objects.all()
        return context


def admin_run_load_data(request, provider_id):
    on_date = request.GET.get('on_date', None)
    provider_load_data_task(provider_id, on_date)
    return HttpResponse(status=200, content='OK')
