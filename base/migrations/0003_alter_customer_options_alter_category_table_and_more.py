# Generated by Django 5.1.2 on 2024-10-27 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_category_table_alter_customer_table_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={},
        ),
        migrations.AlterModelTable(
            name='category',
            table=None,
        ),
        migrations.AlterModelTable(
            name='customer',
            table=None,
        ),
        migrations.AlterModelTable(
            name='customuser',
            table=None,
        ),
        migrations.AlterModelTable(
            name='order',
            table=None,
        ),
        migrations.AlterModelTable(
            name='orderitems',
            table=None,
        ),
        migrations.AlterModelTable(
            name='paymentdetails',
            table=None,
        ),
        migrations.AlterModelTable(
            name='product',
            table=None,
        ),
        migrations.AlterModelTable(
            name='subcategory',
            table=None,
        ),
    ]
