from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Category, Product


def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {"error": "Invalid username or password."})

    return render(request, "login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    total_products = Product.objects.count()
    active_products = Product.objects.filter(status="Active").count()
    inactive_products = Product.objects.filter(status="Inactive").count()
    low_stock_products = Product.objects.filter(stock__lte=5).count()

    context = {
        "total_products": total_products,
        "active_products": active_products,
        "inactive_products": inactive_products,
        "low_stock_products": low_stock_products,
    }

    return render(request, "dashboard.html", context)


@login_required
def product_list(request):
    products = Product.objects.all().order_by("-created_at")

    search = request.GET.get("search", "")
    category = request.GET.get("category", "")
    status = request.GET.get("status", "")

    if search:
        products = products.filter(Q(name__icontains=search))

    if category:
        products = products.filter(category_id=category)

    if status:
        products = products.filter(status=status)

    categories = Category.objects.all()

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "selected_status": status,
    }

    return render(request, "product_list.html", context)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()

    return render(request, "product_form.html", {"form": form, "title": "Add Product"})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "product_form.html", {"form": form, "title": "Edit Product"})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(request, "product_confirm_delete.html", {"product": product})
