# Generated by Django 4.0.5 on 2022-06-05 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]