# Generated by Django 4.0.5 on 2022-07-01 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility_matrix', '0002_utilitymatrixdata_utility_collections_matrix'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilitymatrixdata',
            name='matrix_rung',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]