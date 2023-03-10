# Generated by Django 4.1.7 on 2023-03-10 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DRUGSTORE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drugstore_name', models.CharField(max_length=256, verbose_name='약국명')),
                ('drugstore_zipcode', models.IntegerField(verbose_name='우편번호')),
                ('drugstore_address', models.CharField(max_length=256, verbose_name='주소')),
                ('drugstore_open', models.CharField(max_length=256, verbose_name='개점일')),
                ('drugstore_lng', models.FloatField(default='None', verbose_name='경도')),
                ('drugstore_lat', models.FloatField(default='None', verbose_name='위도')),
                ('drugstore_associate', models.IntegerField(choices=[(1, 'YES'), (0, 'NO')], default='0', verbose_name='제휴여부')),
            ],
            options={
                'verbose_name': '약국정보',
                'verbose_name_plural': '약국정보',
                'db_table': 'DRUGSTORE_TB',
            },
        ),
    ]
