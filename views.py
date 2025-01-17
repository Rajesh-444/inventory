from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import UserRegisterForm, InventoryItemForm, ProductForm, SupplierForm, SaleOrderForm, StockMovementForm
from .models import InventoryItem, Category, Product, Supplier, SaleOrder, StockMovement
from inventory_management.settings import LOW_QUANTITY

# Index Page
class Index(TemplateView):
    template_name = 'inventory/index.html'


# Dashboard View (includes low inventory alerts)
class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

        low_inventory = InventoryItem.objects.filter(
            user=self.request.user.id,
            quantity__lte=LOW_QUANTITY
        )

        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item has low inventory')

        low_inventory_ids = InventoryItem.objects.filter(
            user=self.request.user.id,
            quantity__lte=LOW_QUANTITY
        ).values_list('id', flat=True)

        return render(request, 'inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})


# User Registration
class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )

            login(request, user)
            return redirect('index')

        return render(request, 'inventory/signup.html', {'form': form})


# Inventory Item CRUD
class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'


# Product CRUD
class AddProduct(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('list-products')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditProduct(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'inventory/product_form.html'
    success_url = reverse_lazy('list-products')


class DeleteProduct(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'inventory/delete_product.html'
    success_url = reverse_lazy('list-products')
    context_object_name = 'product'


class ListProducts(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()  # Optionally, adjust the filtering for logged-in users


# List Suppliers View
class ListSuppliers(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'inventory/supplier_list.html'
    context_object_name = 'suppliers'

    def get_queryset(self):
        # Optionally, filter suppliers based on the logged-in user or other conditions
        return Supplier.objects.all()  # Adjust filtering if necessary


# Supplier CRUD Views
class AddSupplier(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('list-suppliers')


class EditSupplier(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'inventory/supplier_form.html'
    success_url = reverse_lazy('list-suppliers')


class DeleteSupplier(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'inventory/delete_supplier.html'
    success_url = reverse_lazy('list-suppliers')
    context_object_name = 'supplier'
    

# List Sale Orders
class ListSaleOrders(LoginRequiredMixin, ListView):
    model = SaleOrder
    template_name = 'inventory/sale_order_list.html'
    context_object_name = 'sale_orders'

    def get_queryset(self):
        # Optionally filter by user if needed
        return SaleOrder.objects.all()

# Add Sale Order
class AddSaleOrder(LoginRequiredMixin, CreateView):
    model = SaleOrder
    form_class = SaleOrderForm
    template_name = 'inventory/sale_order_form.html'
    success_url = reverse_lazy('list-sale-orders')

# Edit Sale Order
class EditSaleOrder(LoginRequiredMixin, UpdateView):
    model = SaleOrder
    form_class = SaleOrderForm
    template_name = 'inventory/sale_order_form.html'
    success_url = reverse_lazy('list-sale-orders')

# Delete Sale Order
class DeleteSaleOrder(LoginRequiredMixin, DeleteView):
    model = SaleOrder
    template_name = 'inventory/sale_order_confirm_delete.html'
    success_url = reverse_lazy('list-sale-orders')


# Stock Movement CRUD

# List Stock Movements View
class ListStockMovements(LoginRequiredMixin, ListView):
    model = StockMovement
    template_name = 'inventory/stock_movement_list.html'
    context_object_name = 'stock_movements'

    def get_queryset(self):
        # Optionally, you can filter stock movements by the logged-in user
        return StockMovement.objects.all()  # Adjust filtering if necessary (e.g., user=self.request.user)

class AddStockMovement(LoginRequiredMixin, CreateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'inventory/stock_movement_form.html'
    success_url = reverse_lazy('list-stock-movements')

    def form_valid(self, form):
        product = form.instance.product
        if form.instance.movement_type == StockMovement.OUT:
            if product.stock_quantity >= form.instance.quantity:
                product.stock_quantity -= form.instance.quantity
                product.save()
            else:
                messages.error(self.request, "Not enough stock available for this movement.")
                return redirect('add-stock-movement')
        else:
            product.stock_quantity += form.instance.quantity
            product.save()
        return super().form_valid(form)


class EditStockMovement(LoginRequiredMixin, UpdateView):
    model = StockMovement
    form_class = StockMovementForm
    template_name = 'inventory/stock_movement_form.html'
    success_url = reverse_lazy('list-stock-movements')


class DeleteStockMovement(LoginRequiredMixin, DeleteView):
    model = StockMovement
    template_name = 'inventory/delete_stock_movement.html'
    success_url = reverse_lazy('list-stock-movements')
    context_object_name = 'stock_movement'
