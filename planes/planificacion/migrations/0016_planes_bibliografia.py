# Generated by Django 5.1.4 on 2025-01-24 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planificacion', '0015_planes_evaluacion_aprendizaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='planes',
            name='bibliografia',
            field=models.TextField(default='Unknown'),
        ),
    ]
