# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_auto_20150812_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalexampart1',
            name='density_normal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='medicalexampart1',
            name='glucose_normal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='medicalexampart1',
            name='hemoglobin_normal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='medicalexampart1',
            name='leukocytes_normal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='medicalexampart1',
            name='nitrites_normal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='medicalexampart1',
            name='pH_normal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='medicalexampart1',
            name='protein_normal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='medicalexampart1',
            name='urobilinogen_normal',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
