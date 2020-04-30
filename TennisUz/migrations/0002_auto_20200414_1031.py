# Generated by Django 3.0.5 on 2020-04-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TennisUz', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='last_name',
            new_name='second_name',
        ),
        migrations.AddField(
            model_name='game',
            name='nn',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='set',
            name='nn',
            field=models.IntegerField(default=1),
        ),
    ]
