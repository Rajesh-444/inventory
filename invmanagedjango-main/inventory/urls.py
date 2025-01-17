from django.contrib import admin
from django.urls import path
from . import views
from .views import (
    Index, SignUpView, Dashboard, AddItem, EditItem, DeleteItem,
    AddProduct, EditProduct, DeleteProduct, ListProducts,
    AddSupplier, EditSupplier, DeleteSupplier, ListSuppliers,AddSaleOrder
     , ListSaleOrders, EditSaleOrder,
    AddStockMovement, ListStockMovements
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    
    # Product routes
    path('add-product/', AddProduct.as_view(), name='add-product'),
    path('edit-product/<int:pk>/', EditProduct.as_view(), name='edit-product'),
    path('delete-product/<int:pk>/', DeleteProduct.as_view(), name='delete-product'),
    path('products/', ListProducts.as_view(), name='list-products'),
    
    path('suppliers/', views.ListSuppliers.as_view(), name='list-suppliers'),
    path('suppliers/add/', views.AddSupplier.as_view(), name='add-supplier'),
    path('suppliers/edit/<int:pk>/', views.EditSupplier.as_view(), name='edit-supplier'),
    path('suppliers/delete/<int:pk>/', views.DeleteSupplier.as_view(), name='delete-supplier'),
    
    # Sale Order routes
    # Sale Order URLs
    path('sale-orders/', views.ListSaleOrders.as_view(), name='list-sale-orders'),
    path('sale-orders/add/', views.AddSaleOrder.as_view(), name='add-sale-order'),  # Use AddSaleOrder here
    path('sale-orders/edit/<int:pk>/', views.EditSaleOrder.as_view(), name='edit-sale-order'),
    path('sale-orders/delete/<int:pk>/', views.DeleteSaleOrder.as_view(), name='delete-sale-order'),
    
    # Stock Movement routes
    path('add-stock-movement/', AddStockMovement.as_view(), name='add-stock-movement'),
    path('stock-movements/', ListStockMovements.as_view(), name='list-stock-movements'),
    
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
]
