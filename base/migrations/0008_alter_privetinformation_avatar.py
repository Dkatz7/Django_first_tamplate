# Generated by Django 4.1 on 2023-01-19 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_privetinformation_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privetinformation',
            name='avatar',
            field=models.ImageField(blank=True, default='/placeholder.png', null=True, upload_to=''),
        ),
    ]
