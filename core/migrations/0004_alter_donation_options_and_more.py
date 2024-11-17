# Generated by Django 5.1.2 on 2024-11-06 09:17

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_case_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='donation',
            old_name='date',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='donor_name',
        ),
        migrations.AddField(
            model_name='donation',
            name='anonymous',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donation',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='donation_type',
            field=models.CharField(choices=[('regular', 'Regular Donation'), ('test', 'Test Donation'), ('offline', 'Offline Donation')], default='test', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='email',
            field=models.EmailField(default='johndoe@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='first_name',
            field=models.CharField(default='John', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='last_name',
            field=models.CharField(default='Doe', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='donation',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='description',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]