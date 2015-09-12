# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20150909_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='gender',
            field=models.CharField(default=b'm', max_length=6, choices=[(b'm', b'Hombre'), (b'f', b'Mujer')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='residence',
            name='administrator',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='residence',
            name='location',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='child',
            name='birthdate',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='child',
            name='birthplace',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='child',
            name='first_name',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='child',
            name='last_name',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='child',
            name='photo',
            field=models.ImageField(null=True, upload_to=b'photos', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='child',
            name='residence',
            field=models.ForeignKey(blank=True, to='tracker.Residence', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='psychologicalexam',
            name='background_notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='psychologicalexam',
            name='emotional_notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='psychologicalexam',
            name='intelectual_notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='psychologicalexam',
            name='organicity_notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='psychologicalexam',
            name='physical_description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='psychologicalexam',
            name='psychomotor_notes',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='psychologicalexam',
            name='recommendation',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='residence',
            name='residence_name',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialexam',
            name='antecedents',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialexam',
            name='economic_situation',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialexam',
            name='family_situation',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialexam',
            name='general_comments',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialexam',
            name='health_situation',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialexam',
            name='housing_situation',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialexam',
            name='recommendation',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='socialexam',
            name='social_diagnosis',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
