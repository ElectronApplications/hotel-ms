# Generated by Django 5.1 on 2024-12-15 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0016_gallery_classinfo_gallery_service_gallery_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gallery',
            options={'verbose_name': 'Gallery', 'verbose_name_plural': 'Galleries'},
        ),
        migrations.AlterModelOptions(
            name='galleryimage',
            options={'verbose_name': 'Gallery image', 'verbose_name_plural': 'Gallery images'},
        ),
    ]
