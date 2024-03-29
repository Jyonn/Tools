# Generated by Django 3.0.6 on 2021-10-31 18:26

import SmartDjango.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Foto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', SmartDjango.models.fields.CharField(max_length=20, unique=True)),
            ],
            options={
                'abstract': False,
                'default_manager_name': 'objects',
            },
        ),
        migrations.AlterModelOptions(
            name='album',
            options={},
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=SmartDjango.models.fields.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='album',
            name='space',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Foto.Space'),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together={('name', 'space')},
        ),
    ]
