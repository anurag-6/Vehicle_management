# Generated by Django 4.1.2 on 2022-10-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vh_number', models.CharField(max_length=20, verbose_name='Vehicle Number')),
                ('vh_type', models.CharField(choices=[('Two Wheeler', '2 Wheeler'), ('Three Wheeler', '3 Wheeler'), ('Four Wheeler', '4 Wheeler')], max_length=20, verbose_name='Vehicle Type')),
                ('vh_model', models.CharField(max_length=20, verbose_name='Vehicle Model')),
                ('vh_disc', models.TextField(verbose_name='Vehicle Discription')),
            ],
            options={
                'db_table': 'Vehicles',
            },
        ),
    ]
