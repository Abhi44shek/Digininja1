# Generated by Django 4.0.1 on 2022-05-28 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_contact_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
