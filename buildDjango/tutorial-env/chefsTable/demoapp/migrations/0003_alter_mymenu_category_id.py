# Generated by Django 3.2.19 on 2023-06-10 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0002_auto_20230609_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymenu',
            name='category_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='category_name', to='demoapp.menucategory'),
        ),
    ]
