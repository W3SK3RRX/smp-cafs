# Generated by Django 5.0 on 2024-06-03 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manutencoes', '0005_ordemservico_delete_ordem_servico'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordemservico',
            name='funcionario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='manutencoes.funcionario'),
        ),
    ]
