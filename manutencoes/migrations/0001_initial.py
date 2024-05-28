# Generated by Django 5.0 on 2024-05-09 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setor',
            fields=[
                ('id_setor', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome_setor', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id_funcionario', models.BigAutoField(primary_key=True, serialize=False)),
                ('nome_funcionario', models.CharField(max_length=40)),
                ('telefone_funcionario', models.CharField(max_length=14)),
                ('setor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='manutencoes.setor')),
            ],
        ),
    ]
