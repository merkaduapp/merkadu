# Generated by Django 4.2.9 on 2024-02-28 18:12

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_market_logotipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='static/merkadu', validators=[app.models.validate_webp_extension], verbose_name='image'),
        ),
    ]