# Generated by Django 5.0.6 on 2024-07-11 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0004_alter_question_figure_alter_quiz_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="progress",
            name="score",
            field=models.JSONField(default=dict, verbose_name="Score"),
        ),
    ]
