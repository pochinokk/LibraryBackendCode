# Generated by Django 4.2.20 on 2025-04-27 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0008_remove_book_publication_date_book_printing_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='return_date',
        ),
        migrations.AddField(
            model_name='book',
            name='end_date',
            field=models.DateField(blank=True, help_text='Дата, возврата или конца брони', null=True, verbose_name='Дата возврата'),
        ),
        migrations.AddField(
            model_name='book',
            name='isReserved',
            field=models.BooleanField(default=False, help_text='Отметь, если книга зарезервирована, для взятия в будущем', verbose_name='Забронирована'),
        ),
    ]
