# Generated by Django 4.2.1 on 2023-05-11 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='eventpics/'),
        ),
    ]
