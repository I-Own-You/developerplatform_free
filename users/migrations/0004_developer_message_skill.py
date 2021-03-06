# Generated by Django 3.2.9 on 2021-12-17 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('username', models.CharField(max_length=20, null=True)),
                ('password', models.CharField(max_length=15, null=True)),
                ('work_position', models.CharField(max_length=30, null=True)),
                ('short_bio', models.CharField(max_length=100, null=True)),
                ('social_link_github', models.URLField(blank=True, null=True)),
                ('social_link_linkedIn', models.URLField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('description', models.CharField(max_length=20, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.developer')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('content', models.CharField(max_length=500, null=True)),
                ('subject', models.CharField(max_length=100, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False, null=True)),
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='users.developer')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='users.developer')),
            ],
            options={
                'ordering': ['is_read', '-created'],
            },
        ),
    ]
