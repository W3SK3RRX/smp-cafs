# Generated by Django 5.0 on 2024-05-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manutencoes', '0002_ordem_servico'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordem_servico',
            name='numero_ordem_servico',
            field=models.IntegerField(default=0),
        ),
    ]
