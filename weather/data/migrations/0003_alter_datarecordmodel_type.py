# Generated by Django 4.0.3 on 2022-03-29 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_alter_datarecordmodel_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datarecordmodel',
            name='type',
            field=models.CharField(max_length=11, verbose_name=[('TEMPERATURE', 'Temperature'), ('HUMIDITY', 'Humidity'), ('PRESSURE', 'Pressure')]),
        ),
    ]
