# Generated by Django 5.1.2 on 2024-12-06 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='apellido',
            field=models.CharField(default=1, max_length=50, verbose_name='Apellido'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(default=1, max_length=50, verbose_name='Nombre'),
            preserve_default=False,
        ),
    ]