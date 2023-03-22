from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter

#from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all().prefetch_related('positions')
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title', 'description']

    # pagination_class = LimitOffsetPagination


class StockViewSet(ModelViewSet):

    queryset = Stock.objects.all().prefetch_related('positions')
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['products']
    search_fields = ['$products__title', '$products__description']

