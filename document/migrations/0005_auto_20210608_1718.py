# Generated by Django 3.2.3 on 2021-06-08 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0004_auto_20210606_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='document',
        ),
        migrations.AddField(
            model_name='document',
            name='tags',
            field=models.ManyToManyField(to='document.Tag'),
        ),
    ]
