from rest_framework import serializers

from .models import Task
from .validators import validate_number, validate_status


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'number', 'status', 'created_at', 'updated_at']

    number = serializers.IntegerField(validators=[validate_number])
    status = serializers.ChoiceField(
        choices=Task.STATUSES, validators=[validate_status]
    )

    def validate(self, data):
        validate_number(data['number'])
        validate_status(data['status'])
        return data

    def create(self, validated_data):
        number = validated_data['number']
        if Task.objects.filter(number=number).exists():
            raise serializers.ValidationError(
                {'number': 'Задача с таким номером уже существует.'}
            )
        return Task.objects.create(**validated_data)
