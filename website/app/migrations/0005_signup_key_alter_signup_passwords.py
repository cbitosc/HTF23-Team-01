# Generated by Django 4.2.6 on 2023-10-08 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_signup_passwords'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='key',
            field=models.CharField(default='key', max_length=100000000),
        ),
        migrations.AlterField(
            model_name='signup',
            name='passwords',
            field=models.CharField(default="{'facebook':None,'instagram':None,'twitter':None,'spotify':None,'dropbox':None,'google':None}", max_length=100000000),
        ),
    ]
