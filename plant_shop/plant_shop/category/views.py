from django.views import generic as views


class CategoriesView(views.TemplateView):
    template_name = 'store/categories.html'