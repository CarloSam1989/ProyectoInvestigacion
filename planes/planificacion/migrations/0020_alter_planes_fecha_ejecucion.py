# Generated by Django 5.1.4 on 2025-01-24 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planificacion', '0019_rename_analisis_tecnica_cierre_planes_an_tecnica_cierre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planes',
            name='fecha_ejecucion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
