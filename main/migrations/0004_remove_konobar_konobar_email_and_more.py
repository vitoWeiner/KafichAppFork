# Generated by Django 5.1.1 on 2024-12-15 16:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_narudzba_narudzba_sifra_alter_pice_pice_sifra'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='konobar',
            name='konobar_email',
        ),
        migrations.RemoveField(
            model_name='konobar',
            name='konobar_korisnicko_ime',
        ),
        migrations.RemoveField(
            model_name='konobar',
            name='konobar_zaporka',
        ),
        migrations.AddField(
            model_name='konobar',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='konobar', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='narudzba',
            name='narudzba_konobar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='narudzbe', to=settings.AUTH_USER_MODEL),
        ),
    ]
