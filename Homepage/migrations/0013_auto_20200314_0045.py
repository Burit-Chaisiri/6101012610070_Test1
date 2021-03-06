# Generated by Django 3.0.4 on 2020-03-14 00:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0012_lecture_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='userSaved',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='userSaved', to='Homepage.Profile'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='Homepage.Profile'),
        ),
    ]
