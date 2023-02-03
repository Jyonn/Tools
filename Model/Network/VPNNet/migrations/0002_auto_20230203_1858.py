# Generated by Django 3.1.12 on 2023-02-03 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VPNNet', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='date',
        ),
        migrations.AddField(
            model_name='session',
            name='record',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='VPNNet.record', verbose_name='记录'),
        ),
    ]
