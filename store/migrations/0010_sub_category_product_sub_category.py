# Generated by Django 4.0 on 2023-07-16 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_remove_product_sub_category_delete_sub_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sub_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='store.sub_category'),
        ),
    ]
