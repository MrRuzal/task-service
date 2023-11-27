from django.db import models


class Task(models.Model):
    STATUSES = [
        ('created', 'Created'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]

    number = models.IntegerField(unique=True, verbose_name='Номер')
    status = models.CharField(
        max_length=20,
        choices=STATUSES,
        default='created',
        verbose_name='Статус',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата и время создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Дата и время обновления'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.number}: {self.status}'
