from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from store.cart import Cart
from store.decorators import staff_required
from store.forms import CategoryForm, ProductForm
from store.models import Category, Product


def home(request):
    products = Product.objects.all()

    return render(request, 'store/home.html', {'products': products})


def about(request):
    return render(request, 'store/about.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})


@staff_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('home')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()

    return render(request, 'store/product_form.html', {'form': form, 'title': 'Add Product'})


@staff_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_detail', pk=product.pk)
        messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/product_form.html', {'form': form, 'title': 'Edit Product'})


@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('home')

    return render(request, 'store/product_confirm_delete.html', {'product': product})


@staff_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


@staff_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('category_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()

    return render(request, 'store/category_form.html', {'form': form, 'title': 'Add Category'})


@staff_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('category_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'store/category_form.html', {'form': form, 'title': 'Edit Category'})


@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('category_list')

    return render(request, 'store/category_confirm_delete.html', {'category': category})


@login_required
def cart_view(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required
@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 0

    if quantity < 1:
        messages.error(request, 'Please enter a valid quantity.')
        return redirect('product_detail', pk=product.id)

    cart = Cart(request)
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart_view')


@login_required
@require_POST
def cart_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 0))
    except (TypeError, ValueError):
        quantity = 0

    if quantity < 1:
        messages.error(request, 'Quantity must be at least 1. Use Remove to delete an item.')
    else:
        cart = Cart(request)
        cart.update(product=product, quantity=quantity)
        messages.success(request, 'Cart updated.')

    return redirect('cart_view')


@login_required
@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    messages.success(request, f'{product.name} removed from cart.')
    return redirect('cart_view')
