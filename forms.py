from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem, Product, Supplier, SaleOrder, StockMovement


# User Registration Form
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Inventory Item Form
class InventoryItemForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)

    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'category']


# Product Form (for CRUD operations on products)
class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = forms.IntegerField(min_value=0)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'supplier']


# Supplier Form (for CRUD operations on suppliers)
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'address']


from django import forms
from .models import SaleOrder

class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = SaleOrder
        fields = ['product', 'quantity', 'total_price', 'status']
        widgets = {
            'status': forms.Select(choices=SaleOrder.STATUS_CHOICES),
        }



# Stock Movement Form (for CRUD operations on stock movements)
class StockMovementForm(forms.ModelForm):
    movement_type = forms.ChoiceField(choices=[('In', 'In'), ('Out', 'Out')])
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = StockMovement
        fields = ['product', 'quantity', 'movement_type', 'notes']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be a positive integer.")
        return quantity
