from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    """Модель данных Контакт"""
    first_name = models.CharField(max_length=100, verbose_name='Имя', blank=False, null=False)
    last_name = models.CharField(max_length=100, verbose_name='Фамилия', blank=True, null=True)
    phone = PhoneNumberField(
        verbose_name='Номер телефона',
        blank=True,
        null=True,
        unique=True,
    )
    email = models.EmailField(verbose_name='E-mail', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        app_label = 'contacts'
