# Generated by Django 3.0.6 on 2020-05-13 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('hoops', '0012_auto_20200511_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherconditions',
            name='location',
            field=models.CharField(default='ljubljana', max_length=80),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
