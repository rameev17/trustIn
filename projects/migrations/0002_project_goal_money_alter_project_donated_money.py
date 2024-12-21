# Generated by Django 5.1.4 on 2024-12-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='goal_money',
            field=models.IntegerField(default=0, verbose_name='Целевая сумма'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='donated_money',
            field=models.IntegerField(verbose_name='Собранные деньги'),
        ),
    ]