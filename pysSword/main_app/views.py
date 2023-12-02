from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main Page'
        context['user'] = self.request.user
        return context
