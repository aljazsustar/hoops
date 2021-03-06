# Generated by Django 3.0.5 on 2020-04-29 13:48

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hoops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 4, 29, 13, 48, 41, 629218, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempts_successful', models.PositiveSmallIntegerField()),
                ('attempts_made', models.PositiveSmallIntegerField()),
                ('practice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hoops.Practice')),
            ],
        ),
    ]
