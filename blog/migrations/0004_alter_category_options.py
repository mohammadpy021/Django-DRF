# Generated by Django 4.2.2 on 2025-01-12 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_articles_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته\u200cبندی', 'verbose_name_plural': 'دسته\u200cبندی ها'},
        ),
    ]
