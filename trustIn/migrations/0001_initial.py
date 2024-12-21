# Generated by Django 5.1.4 on 2024-12-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('file', models.FileField(upload_to='reports/%Y/%m/', verbose_name='PDF файл')),
                ('month', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')], verbose_name='Месяц')),
                ('year', models.PositiveIntegerField(default=2024, verbose_name='Год')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
            ],
            options={
                'verbose_name': 'Отчет',
                'verbose_name_plural': 'Отчеты',
                'ordering': ['-year', '-month'],
                'unique_together': {('month', 'year')},
            },
        ),
    ]
