# Generated by Django 4.0.1 on 2022-01-14 07:32

from django.db import migrations, models
import django.templatetags.static


class Migration(migrations.Migration):

    dependencies = [
        ('utp_app', '0007_userdatamodel_beneficiary_reference_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdatamodel',
            name='user_photo',
            field=models.ImageField(default='/static/user_photo.png', upload_to=django.templatetags.static.static),
        ),
    ]
