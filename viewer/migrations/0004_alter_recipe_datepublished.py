# Generated by Django 3.2.5 on 2021-08-05 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0003_auto_20210805_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='datePublished',
            field=models.DateField(blank=True, null=True),
        ),
    ]
