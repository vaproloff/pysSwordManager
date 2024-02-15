from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    View class for rendering the main page template.

    This class inherits from Django's TemplateView and is responsible for rendering the main page template
    ('main_app/index.html').

    Attributes:
        template_name (str): The template name to be rendered.

    Methods:
        get_context_data(**kwargs): Returns the context data to be passed to the template.
    """
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        """
        Returns the context data to be passed to the template.

        This method overrides the parent class method to add additional context data:
        - 'title': The title of the main page.
        - 'user': The authenticated user making the request.

        :return: Dictionary containing the context data.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        context['user'] = self.request.user
        return context
