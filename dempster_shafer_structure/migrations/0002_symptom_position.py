# Generated by Django 4.0.5 on 2022-07-06 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dempster_shafer_structure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='symptom',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
