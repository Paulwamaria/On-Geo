# Generated by Django 2.2.8 on 2020-01-04 15:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ongeo', '0016_remove_allatendees_last_seen'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('name', models.CharField(max_length=60)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
