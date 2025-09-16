
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('contrasena', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterModelOptions(
            name='perfilusuario',
            options={},
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='telefono',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Progreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leccion', models.CharField(max_length=200)),
                ('categoria', models.CharField(max_length=100)),
                ('fecha_completada', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Usuarios.usuario')),
            ],
        ),
    ]
