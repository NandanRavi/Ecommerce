# Generated by Django 5.1.2 on 2024-11-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_alter_paymentdetails_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentdetails',
            name='status',
            field=models.CharField(choices=[('None', 'None'), ('success', 'Success'), ('failed', 'Failed')], default='None', max_length=10),
        ),
    ]