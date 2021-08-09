from django.urls import reverse
from django.views.generic import TemplateView


class BreadcrumbTemplateView(TemplateView):
    breadcrumb_name = ""
    breadcrumb_url = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'breadcrumbs': [{'name': self.breadcrumb_name, 'link': reverse(self.breadcrumb_url)}]})
        return context

    def get_active_company(self):
        return self.request.user.player.active_company
