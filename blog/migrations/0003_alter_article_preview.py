# Generated by Django 3.2.14 on 2022-08-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20220820_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='preview',
            field=models.CharField(default='', max_length=500),
        ),
    ]