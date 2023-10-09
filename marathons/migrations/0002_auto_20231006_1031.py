# Generated by Django 3.2.16 on 2023-10-06 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marathons', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='marathon',
            options={'ordering': ['-publish'], 'verbose_name': 'Марафон', 'verbose_name_plural': 'Марафоны'},
        ),
        migrations.AddField(
            model_name='marathon',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='marathon',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='marathon',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique_for_date='publish'),
        ),
        migrations.AddField(
            model_name='marathon',
            name='status',
            field=models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published')], default='DF', max_length=2),
        ),
        migrations.AddIndex(
            model_name='marathon',
            index=models.Index(fields=['-publish'], name='marathons_m_publish_96d825_idx'),
        ),
    ]
