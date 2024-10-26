# Generated by Django 5.0.9 on 2024-10-08 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_recipe_cuisinetype'),
        ('images', '0002_image_total_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='recipe_assoc',
            field=models.ManyToManyField(blank=True, related_name='recipe_assoc', to='blog.recipe'),
        ),
    ]