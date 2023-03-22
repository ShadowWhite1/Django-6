from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    # настройте сериализатор для продукта

    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    # настройте сериализатор для позиции продукта на складе

    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    # настройте сериализатор для склада

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        print(validated_data)
        positions = validated_data.pop('positions')

        print(positions)

        # создаем склад по его параметрам
        stock = super().create(validated_data)
        print(stock)
        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        for position in positions:
            StockProduct.objects.create(stock_id=stock.id, **position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions_data = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        for position_data in positions_data:
            obj_created = StockProduct.objects.filter(stock_id=stock.id).update_or_create(
                stock=stock,
                product=position_data['product'],
                defaults={
                    'quantity': position_data['quantity'],
                    'price': position_data['price']
                }
            )

        return stock
