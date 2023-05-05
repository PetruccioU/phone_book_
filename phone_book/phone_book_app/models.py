from django.db import models
from django.urls import reverse

# Create your models here.


class PhoneCard(models.Model):
    phone_number = models.CharField(max_length=255, verbose_name='Номер телефона')
    name = models.CharField(max_length=255, verbose_name='ФИО физического лица/Название организации')
    company_division_name = models.CharField(max_length=255, blank=True, verbose_name='Название отдела организации')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес проживания/организации')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано ли")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Тип регистрации")

    def __str__(self):
        return self.phone_number

    # For dynamic URL use get_absolute_url.
    def get_absolute_url(self):
        return reverse('card', kwargs={'phone_card_slug': self.slug})

    class Meta:
        verbose_name='Карточка абонента'
        verbose_name_plural ='Карточки абонентов'
        ordering = ['id']


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Тип регистрации')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL:")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Тип регистрации:'
        verbose_name_plural ='Типы регистрации:'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
