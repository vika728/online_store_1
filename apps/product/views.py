from django.views.generic import ListView, DetailView, DeleteView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from apps.product.forms import CreateProductForm, CreateReviewProductForm
from apps.product.models import Product, Category, ReviewProduct
from apps.product.permissions import SuperUserCheckMixin


class IndexPage(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/index.html'

    def get_template_names(self):
        template_name = super(IndexPage, self).get_template_names()
        search = self.request.GET.get('q')
        if search:
            template_name = 'product/search.html'
        return template_name

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        if search:
            context['products'] = Product.objects.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'product/category_detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_products'] = Product.objects.filter(category=self.slug)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'product/products_list.html'
    context_object_name = 'products'
    paginate_by = 4


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(SuperUserCheckMixin, CreateView):
    model = Product
    form_class = CreateProductForm
    template_name = 'product/product_create.html'
    success_url = reverse_lazy('product-create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class ProductEditView(SuperUserCheckMixin, View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product)
        context = {
            'product': product,
            'form': form
        }
        return render(request, 'product/product_update.html', context)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        form = CreateProductForm(instance=product, data=request.POST)
        if form.is_valid():
            product = form.save()
            return redirect(product.get_absolute_url())


class ProductDeleteView(SuperUserCheckMixin, DeleteView):
    model = Product
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('products-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Продукт успешно удален!')
        return HttpResponseRedirect(success_url)


class ReviewIndexPage(ListView):
    model = ReviewProduct
    template_name = 'review_page.html'
    context_object_name = 'all_reviews'


class ReviewCreate(CreateView):
    model = ReviewProduct
    form_class = CreateReviewProductForm
    template_name = 'product/review_create.html'
    success_url = reverse_lazy('products-list')

    def form_valid(self, form):
        user = self.request.user
        review = form.save(commit=False)
        review.user = user
        review.save()
        return super().form_valid(form)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


@login_required()
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required()
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required()
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required()
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required()
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/account/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


class ReviewIndexPage(ListView):
    model = ReviewProduct
    template_name = 'review_page.html'
    context_object_name = 'all_reviews'