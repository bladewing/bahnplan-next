from django.urls import reverse


class BreadcrumbMixin:
    breadcrumb_name = ""
    breadcrumb_url = ""
    parent = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumbs = []
        if self.parent is not None:
            breadcrumbs.append(self.parent.get_own_breadcrumb(self.parent))
        breadcrumbs.append(self.get_own_breadcrumb())
        context.update({'breadcrumbs': breadcrumbs})
        return context

    def get_active_company(self):
        return self.request.user.player.active_company

    def get_own_breadcrumb(self):
        return {'name': self.breadcrumb_name, 'link': reverse(self.breadcrumb_url)}
