# Generated by Django 5.0.6 on 2024-07-12 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0026_course_level"),
    ]

    operations = [
        migrations.AddField(
            model_name="program",
            name="thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="program_thumbnails/"
            ),
        ),
    ]