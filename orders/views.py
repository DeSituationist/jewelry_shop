from django.shortcuts import get_object_or_404, render, redirect
from .models import Order, OrderItem

# Create your views here.
def create_order(request):
    ...