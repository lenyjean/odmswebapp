# Generated by Django 4.2 on 2023-05-04 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_alter_documents_receiver_alter_documents_tracking_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='tracking_no',
            field=models.CharField(default='b3e567', editable=False, max_length=255),
        ),
        migrations.AlterField(
            model_name='user',
            name='contact',
            field=models.CharField(max_length=13),
        ),
    ]