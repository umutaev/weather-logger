# Generated by Django 4.0.3 on 2022-03-29 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_alter_datarecordmodel_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='datarecordmodel',
            name='label',
            field=models.CharField(default=None, max_length=256, null=True),
        ),
    ]
