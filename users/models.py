from django.db import models
from django.contrib.auth.models import AbstractUser

from lms.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}

class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите Email"
    )

    phone_number = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        blank=True,
        null=True,
    )

    avatars = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите фотографию",
    )
    city = models.CharField(
        max_length=40,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Введите город",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.email}"


class Payments(models.Model):
    method_choices = [
        ('CASH', 'Наличными'),
        ('TRANSFER', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Пользователь'),
    date_payment = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты'),
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Оплаченный курс', **NULLABLE),
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name='Оплаченный урок', **NULLABLE),
    payment_sum = models.PositiveIntegerField(verbose_name='Cумма платежа')
    payment_method = models.CharField(max_length=50, choices=method_choices, verbose_name='Способ оплаты')
    session_id = models.CharField(max_length=255, verbose_name='ID сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='Ссылка на оплату', **NULLABLE)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user} - {self.paid_course if self.paid_course else self.paid_lesson}'
