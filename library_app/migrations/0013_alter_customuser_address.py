# Generated by Django 4.2.20 on 2025-04-27 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0012_alter_book_end_date_alter_book_is_taken_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес'),
        ),
    ]
