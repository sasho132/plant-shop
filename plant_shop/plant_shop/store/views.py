from django.shortcuts import render
from django.views import generic as views
from plant_shop.store.models import Product
from django.core.paginator import Paginator


class IndexView(views.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = self.request.user
        return context


def products_view(request, slug=None):
    if slug is not None:
        products = Product.objects.all().filter(category__slug=slug).order_by('pk')
    else:
        products = Product.objects.all().order_by('pk')

    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)

    context = {
        'products': paged_products,
    }
    return render(request, 'store/products.html', context)


class ProductDetailsView(views.DetailView):
    model = Product
    template_name = 'store/product-details.html'


class ContactUsView(views.TemplateView):
    template_name = 'contact-us.html'
