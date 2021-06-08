# Generated by Django 3.2.4 on 2021-06-08 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_well_well_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='well',
            name='oilfield',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wells', to='info.oilfield', verbose_name='Месторождение'),
        ),
    ]