# Generated by Django 5.1.2 on 2024-11-10 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_customuser_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='token_created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
