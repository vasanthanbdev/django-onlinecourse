# Generated by Django 4.2.3 on 2024-07-07 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecourse', '0007_alter_enrollment_course_alter_enrollment_learner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='choice_text',
            new_name='content',
        ),
    ]
