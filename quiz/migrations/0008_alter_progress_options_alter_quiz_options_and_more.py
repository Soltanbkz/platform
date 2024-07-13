# Generated by Django 5.0.6 on 2024-07-11 19:33

import django.core.validators
import django.db.models.deletion
import re
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0024_remove_program_picture"),
        ("quiz", "0007_alter_progress_options_alter_quiz_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="progress",
            options={
                "verbose_name": "User Progress",
                "verbose_name_plural": "User progress records",
            },
        ),
        migrations.AlterModelOptions(
            name="quiz",
            options={"verbose_name": "Quiz", "verbose_name_plural": "Quizzes"},
        ),
        migrations.AlterModelOptions(
            name="sitting",
            options={"permissions": (("view_sittings", "Can see completed exams."),)},
        ),
        migrations.AlterField(
            model_name="mcquestion",
            name="choice_order",
            field=models.CharField(
                blank=True,
                choices=[
                    ("content", "Content"),
                    ("random", "Random"),
                    ("none", "None"),
                ],
                help_text="The order in which multichoice choice options are displayed to the user",
                max_length=30,
                null=True,
                verbose_name="Choice Order",
            ),
        ),
        migrations.AlterField(
            model_name="progress",
            name="score",
            field=models.CharField(
                max_length=1024,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^\\d+(?:,\\d+)*\\Z"),
                        code="invalid",
                        message="Enter only digits separated by commas.",
                    )
                ],
                verbose_name="Score",
            ),
        ),
        migrations.AlterField(
            model_name="progress",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="answers_at_end",
            field=models.BooleanField(
                default=False,
                help_text="Correct answer is NOT shown after question. Answers displayed at the end.",
                verbose_name="Answers at end",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("assignment", "Assignment"),
                    ("exam", "Exam"),
                    ("practice", "Practice Quiz"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="description",
            field=models.TextField(
                blank=True,
                help_text="A detailed description of the quiz",
                verbose_name="Description",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="draft",
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text="If yes, the quiz is not displayed in the quiz list and can only be taken by users who can edit quizzes.",
                verbose_name="Draft",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="exam_paper",
            field=models.BooleanField(
                default=False,
                help_text="If yes, the result of each attempt by a user will be stored. Necessary for marking.",
                verbose_name="Exam Paper",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="pass_mark",
            field=models.SmallIntegerField(
                blank=True,
                default=50,
                help_text="Percentage required to pass exam.",
                validators=[django.core.validators.MaxValueValidator(100)],
                verbose_name="Pass Mark",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="random_order",
            field=models.BooleanField(
                default=False,
                help_text="Display the questions in a random order or as they are set?",
                verbose_name="Random Order",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="single_attempt",
            field=models.BooleanField(
                default=False,
                help_text="If yes, only one attempt by a user will be permitted.",
                verbose_name="Single Attempt",
            ),
        ),
        migrations.AlterField(
            model_name="quiz",
            name="title",
            field=models.CharField(max_length=60, verbose_name="Title"),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="complete",
            field=models.BooleanField(default=False, verbose_name="Complete"),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="course",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="course.course",
                verbose_name="Course",
            ),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="current_score",
            field=models.IntegerField(verbose_name="Current Score"),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="end",
            field=models.DateTimeField(blank=True, null=True, verbose_name="End"),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="incorrect_questions",
            field=models.CharField(
                blank=True,
                max_length=1024,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^\\d+(?:,\\d+)*\\Z"),
                        code="invalid",
                        message="Enter only digits separated by commas.",
                    )
                ],
                verbose_name="Incorrect questions",
            ),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="question_list",
            field=models.CharField(
                max_length=1024,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^\\d+(?:,\\d+)*\\Z"),
                        code="invalid",
                        message="Enter only digits separated by commas.",
                    )
                ],
                verbose_name="Question List",
            ),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="question_order",
            field=models.CharField(
                max_length=1024,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^\\d+(?:,\\d+)*\\Z"),
                        code="invalid",
                        message="Enter only digits separated by commas.",
                    )
                ],
                verbose_name="Question Order",
            ),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="quiz",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="quiz.quiz",
                verbose_name="Quiz",
            ),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="start",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Start"),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="sitting",
            name="user_answers",
            field=models.TextField(
                blank=True, default="{}", verbose_name="User Answers"
            ),
        ),
    ]