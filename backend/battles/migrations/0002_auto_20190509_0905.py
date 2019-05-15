# Generated by Django 2.1.7 on 2019-05-09 09:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('halloffame', '0001_initial'),
        ('battles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='attacker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='round_attackers', to='halloffame.Hero'),
        ),
        migrations.AddField(
            model_name='round',
            name='battle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='battles.Battle'),
        ),
        migrations.AddField(
            model_name='round',
            name='defender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='round_defenders', to='halloffame.Hero'),
        ),
        migrations.AddField(
            model_name='battle',
            name='attendees',
            field=models.ManyToManyField(related_name='battles', to='halloffame.Hero'),
        ),
        migrations.AddField(
            model_name='battle',
            name='looser',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lost_battles', to='halloffame.Hero'),
        ),
    ]