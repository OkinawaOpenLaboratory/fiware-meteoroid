# Generated by Django 2.2.7 on 2019-11-21 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20191111_0805'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('orion_subscription_id', 'fiware_service', 'fiware_service_path')},
        ),
    ]