from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Product, State
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from .serializers import ProductSerializer, StateSerializer


# Custom pagination class
class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100
class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination  # Set your CustomPagination class here

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get query parameters for filtering
        filters = {}
        for key, value in self.request.query_params.items():
            # Assuming filter keys match with model fields (e.g., 'name', 'description', etc.)
            if key in ['name', 'description']:  # Add more fields as needed
                filters[key + '__icontains'] = value  # Perform case-insensitive partial matching

        # Apply filters to queryset
        if filters:
            queryset = queryset.filter(**filters)

        return queryset


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):  # Use RetrieveUpdateDestroyAPIView
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []  # Example permission, adjust as needed
    lookup_field = 'pk'  # Assuming 'id' is the field to look up the product

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = []

class StateListAPIView(ListAPIView):
    serializer_class = StateSerializer
    permission_classes = []
    queryset = State.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()

        import random

        # Assuming you have a queryset named 'queryset' with length x

        # Define the number of random items you want to retrieve (e.g., n)
        n = 3  # Replace this with your desired number

        # Get the total count of items in the queryset
        total_count = queryset.count()

        # If the desired number of items (n) is greater than the total count (x), adjust n
        if n > total_count:
            n = total_count

        # Get the primary keys (IDs) of all items in the queryset
        all_ids = list(queryset.values_list('id', flat=True))

        # Get a random sample of n unique IDs from all_ids
        random_ids = random.sample(all_ids, n)

        # Retrieve the random subset from the queryset using the random IDs
        random_subset = queryset.filter(id__in=random_ids)

        # Get query parameters for filtering
        len = queryset.count()


        return random_subset

class NotificationsTemplateView(TemplateView):
    template_name='notifications_template.html'