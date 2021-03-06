# Generated by Django 2.2.6 on 2019-11-05 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191105_1032'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiware_service', models.CharField(blank=True, default='', max_length=64)),
                ('fiware_service_path', models.CharField(default='/', max_length=64)),
                ('orion_subscription_id', models.CharField(max_length=64)),
                ('endpoint_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Endpoint')),
            ],
            options={
                'unique_together': {('fiware_service', 'fiware_service_path')},
            },
        ),
    ]
