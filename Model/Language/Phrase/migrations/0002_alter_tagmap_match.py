# Generated by Django 5.0.3 on 2024-04-10 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Phrase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagmap',
            name='match',
            field=models.BooleanField(blank=True, help_text='null未知 true匹配 false相反', null=True, verbose_name='是否匹配'),
        ),
    ]