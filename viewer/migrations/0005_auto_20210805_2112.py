# Generated by Django 3.2.5 on 2021-08-05 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_alter_recipe_datepublished'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='calories',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='carbohydrateContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='cholesterolContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='fatContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='fiberContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='proteinContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='saturatedFatContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='servingSize',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='sodiumContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='sugarContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='transFatContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='nutritionalinfo',
            name='unsaturatedFatContent',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
