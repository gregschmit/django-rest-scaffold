from django.apps import apps
from django.views import generic


class ExampleView(generic.TemplateView):
    """
    Example view for showing all scaffolds.
    """

    template_name = "rest_scaffold/example.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["models"] = [(x.__name__, x._meta.app_label) for x in apps.get_models()]
        return context
