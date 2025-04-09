# Generated by Django 4.2 on 2025-04-02 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Diagnostic', '0002_alter_medecin_options_remove_medecin_est_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='suivimedical',
            name='stade_mrc',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='suivimedical',
            name='diagnostic',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='suivimedical',
            name='traitement',
            field=models.TextField(blank=True),
        ),
    ]
