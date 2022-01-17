# Generated by Django 4.0.1 on 2022-01-09 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utp_app', '0006_alter_userdatamodel_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatamodel',
            name='beneficiary_reference_id',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='userdatamodel',
            name='session_key',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
