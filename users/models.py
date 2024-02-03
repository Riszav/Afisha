
from django.db import models
from django.contrib.auth.models import User
import random

from django.utils import timezone
from datetime import timedelta


class ConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}: {self.code} {self.is_expired()}'

    class Meta:  # Мета класс - Это класс, который содержит дополнительную информацию о модели
        db_table = 'confirm_code'  # Название таблицы в базе данных (по умолчанию appname_classname (post_postinfo))
        verbose_name = 'Код подтврждения'  # Название модели в единственном числе
        verbose_name_plural = 'Коды подтверждения'  # Название модели во множественном числе

    def generate(self):
        rand_code = ''
        for i in range(6):
            # rand_code += ' ' if i == 3 else ''
            rand_code += str(random.randint(0, 9))
        self.code = rand_code
        # self.code = ''.join(choice('0123456789') for _ in range(6))

    def is_expired(self):
        return timezone.now() - self.created_at > timedelta(hours=72)