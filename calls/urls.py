from django.urls import path
from django.views.generic import TemplateView
from .views import ProductListAPIView, ProductDetailAPIView, ProductCreateAPIView, StateListAPIView, \
    NotificationsTemplateView

urlpatterns = [
    # Other URL patterns

    path('calls/', TemplateView.as_view(template_name='calls/product_list.html'), name='product-list'),
    path('api/calls/', ProductListAPIView.as_view(), name='api-product-list'),
    path('api/calls/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('api/calls/create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('api/calls/states/', StateListAPIView.as_view(), name='state-list'),
    path('notifications/', NotificationsTemplateView.as_view(), name='notifications_list')
]
