# Generated by Django 3.0.2 on 2020-01-12 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('helpnet', '0003_auto_20200111_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='req_made',
            fields=[
                ('req_id', models.AutoField(primary_key=True, serialize=False)),
                ('req_type', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=20)),
                ('username', models.CharField(blank=True, max_length=200, null=True)),
                ('req_time', models.CharField(max_length=6)),
                ('location', models.CharField(max_length=20)),
                ('nprespond', models.CharField(blank=True, default=0, max_length=5, null=True)),
                ('auth_resp', models.CharField(blank=True, max_length=200, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='helpnet.person')),
            ],
        ),
    ]
