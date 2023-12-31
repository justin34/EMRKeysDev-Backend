# Generated by Django 4.2.3 on 2023-08-21 12:49

from django.db import migrations, models
import django.db.models.deletion
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_patient_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom', models.CharField(max_length=100)),
                ('severity', models.CharField(choices=[('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')], default='mild', max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_picture',
            field=models.ImageField(default='/profilePictures/DefaultProfilePic.png', upload_to=home.models.upload_path),
        ),
        migrations.CreateModel(
            name='AINote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.CharField(max_length=10000, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.patient')),
                ('symptoms', models.ManyToManyField(null=True, to='home.symptom')),
            ],
        ),
    ]
