# Generated by Django 3.2.8 on 2021-12-03 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0003_alter_evento_responsable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='responsable',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eventos.responsable'),
        ),
    ]