from rest_framework import serializers
from apps.categories.serializers import CategorySerializer
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Transaction
        fields = ('id', 'type', 'amount', 'description', 'note', 'date',
                  'is_recurring', 'category', 'category_detail', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate(self, data):
        category = data.get('category')
        if category and category.user != self.context['request'].user:
            raise serializers.ValidationError({'category': "Cette catégorie ne vous appartient pas."})
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)