from rest_framework import serializers


def validate_number(value):
    """
    Валидация для поля 'number'.
    Убедитесь, что значение больше 0.
    """
    if value <= 0:
        raise serializers.ValidationError(
            "Number должен быть положительным числом."
        )
    return value


def validate_status(value):
    """
    Валидация для поля 'status'.
    Проверяет, что значение поля 'status' равно 'created' при создании задачи.
    """
    if value != 'created':
        raise serializers.ValidationError(
            "Статус должен быть 'created' при создании новой задачи."
        )
    return value
