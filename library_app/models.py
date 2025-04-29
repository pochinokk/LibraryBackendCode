from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Телефон')
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name='Адрес')
    ROLE_CHOICES = [
        ('ADMIN', 'Администратор'),
        ('LIBRARIAN', 'Библиотекарь'),
        ('READER', 'Читатель'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='READER', verbose_name='Роль')
    def __str__(self):
        return f"{self.full_name} (Логин: {self.username})"

class Book(models.Model):
    reader = models.ForeignKey(CustomUser,
                               null=True,
                               blank=True,
                               on_delete=models.SET_NULL,
                               limit_choices_to={'role': 'READER'},
                            #    to_field='username',
                               verbose_name='Читатель',
                               help_text='Читатель данной книги')
    
    name = models.CharField(max_length=255,
                            verbose_name='Название',
                            help_text='Название книги, не более 255 символов')
    
    author = models.CharField(max_length=255,
                              verbose_name='Автор',
                              help_text='Автор книги, не более 255 символов')
    
    printing_year = models.IntegerField(null=True,
                                        blank=True,
                                        verbose_name='Год издания',
                                        help_text='Год издания')
    
    language = models.CharField(max_length=100,
                                verbose_name='Язык',
                                help_text='Язык книги, не более 100 символов')
    
    is_taken = models.BooleanField(default=False,
                                    verbose_name='На руках',
                                    help_text='Книга взята читателем или нет'
                                    )
    end_date = models.DateField(null=True,
                                blank=True,
                                verbose_name='Дата конца выдачи/брони',
                                help_text='Если книга взята, то это дата конца выдачи. Если книга не взята, то это конец брони')

    def clean(self):
        if self.end_date and not self.reader:
            raise ValidationError("Нельзя указать дату конца выдачи/брони без читателя")
        if self.reader and not self.end_date:
            raise ValidationError("Нельзя указать читателя без даты конца выдачи/брони")
        if self.is_taken and not self.reader:
            raise ValidationError("Если книга выдана, то у неё должен быть читатель")

    class Meta:
        verbose_name = 'книга'
        verbose_name_plural = 'книги'

    def __str__(self):
        return self.name