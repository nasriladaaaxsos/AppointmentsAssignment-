# Generated by Django 3.2.15 on 2022-09-07 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0002_auto_20220907_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='Taskuser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users', to='app2.user'),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='Taskstatus',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='statues', to='app2.taskstatus'),
        ),
    ]
