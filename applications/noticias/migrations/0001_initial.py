# Generated manually for noticias app

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=500, verbose_name='Título')),
                ('resumen', models.TextField(blank=True, null=True, verbose_name='Resumen')),
                ('imagen_preview', models.URLField(blank=True, max_length=1000, null=True, verbose_name='Imagen de vista previa')),
                ('link', models.URLField(max_length=1000, verbose_name='Enlace a la noticia')),
                ('fuente', models.CharField(max_length=200, verbose_name='Fuente de la noticia')),
                ('fecha_publicacion', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de publicación')),
                ('fecha_scraping', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de scraping')),
            ],
            options={
                'verbose_name': 'Noticia',
                'verbose_name_plural': 'Noticias',
                'ordering': ['-fecha_publicacion'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='noticia',
            unique_together={('link', 'fuente')},
        ),
    ]
