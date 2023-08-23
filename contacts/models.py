from django.db import models


class Contact(models.Model):
    """Модель данных Контакт"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        app_label = 'contacts'
