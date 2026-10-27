from django.urls import path
from . import views

app_name='shop'

urlpatterns = [
	path('search/', views.product_search, name='product_search'),
	path('stone/<str:stone_slug>/', views.product_list, name='product_list_by_stone'),
	path('product/<int:id>/<str:slug>/', views.product_detail, name='product_detail'),
	path('', views.product_list, name='product_list'),
]