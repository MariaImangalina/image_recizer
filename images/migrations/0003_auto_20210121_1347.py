# Generated by Django 3.0.6 on 2021-01-21 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20210113_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(upload_to='images'),
        ),
    ]
