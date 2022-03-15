# Generated by Django 4.0.2 on 2022-03-10 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BarkerApp', '0004_alter_request_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='connected_profiles',
            field=models.ManyToManyField(blank=True, to='BarkerApp.Profile'),
        ),
        migrations.CreateModel(
            name='Bark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=280)),
                ('media', models.TextField()),
                ('date', models.DateTimeField()),
                ('replies', models.ManyToManyField(blank=True, to='BarkerApp.Bark')),
                ('reply_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='BarkerApp.bark')),
            ],
        ),
    ]