# Generated by Django 3.0.6 on 2020-05-31 10:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import movie_store.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('year', models.IntegerField()),
                ('director', models.TextField()),
                ('genres', models.ManyToManyField(to='movie_store.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('rental_date', models.DateTimeField(default=movie_store.models.get_current_datetime, editable=False)),
                ('return_date', models.DateTimeField(default=None, editable=False, null=True)),
                ('fee', models.FloatField(default=0, editable=False)),
                ('returned', models.BooleanField(default=False)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie_store.Movie')),
                ('owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
