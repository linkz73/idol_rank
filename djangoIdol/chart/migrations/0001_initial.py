# Generated by Django 2.2.5 on 2019-12-24 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='TITLE')),
                ('slug', models.SlugField(allow_unicode=True, help_text='제목을 위한 별칭으로 한개의 단어로 사용', unique=True, verbose_name='SLUG')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='DESCRIPTION')),
                ('content', models.TextField(verbose_name='CONTENT')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='CREATE DATE')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='MODIFY DATE')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'chart',
                'verbose_name_plural': 'chart',
                'db_table': 'chart',
                'ordering': ('-modify_date',),
            },
        ),
    ]
