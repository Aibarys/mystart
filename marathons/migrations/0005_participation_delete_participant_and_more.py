# Generated by Django 4.2.5 on 2023-10-14 13:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20231009_1824'),
        ('marathons', '0004_alter_marathon_file_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('marathon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marathons.marathon')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.userprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.AddField(
            model_name='marathon',
            name='participants',
            field=models.ManyToManyField(related_name='marathons_participated', through='marathons.Participation', to='users.userprofile'),
        ),
    ]
