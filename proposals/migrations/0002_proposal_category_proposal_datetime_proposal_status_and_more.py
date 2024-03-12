# Generated by Django 5.0.2 on 2024-02-28 19:24

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='category',
            field=models.CharField(choices=[('General', 'General'), ('Classes', 'Classes'), ('Adminstrative', 'Adminstrative'), ('Technical', 'Technical')], default='Entered', max_length=20),
        ),
        migrations.AddField(
            model_name='proposal',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='proposal',
            name='status',
            field=models.CharField(choices=[('Entered', 'Entered'), ('In progress', 'n progress'), ('Finished', 'Finished'), ('Rejected', 'Rejected')], default='General', max_length=20),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='content',
            field=models.TextField(),
        ),
    ]
