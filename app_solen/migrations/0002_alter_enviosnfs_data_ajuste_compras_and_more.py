# Generated by Django 4.2.6 on 2023-11-24 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_solen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enviosnfs',
            name='data_ajuste_compras',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de Ajuste'),
        ),
        migrations.AlterField(
            model_name='enviosnfs',
            name='data_divergencia_fiscal',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data da Divergencia'),
        ),
        migrations.AlterField(
            model_name='enviosnfs',
            name='data_validacao_fiscal',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data de Validação'),
        ),
        migrations.AlterField(
            model_name='enviosnfs',
            name='observacao_compras',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Observação Compras'),
        ),
        migrations.AlterField(
            model_name='enviosnfs',
            name='observacao_fiscal',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='Observação Fiscal'),
        ),
        migrations.AlterField(
            model_name='enviosnfs',
            name='observacao_fornecedor',
            field=models.TextField(blank=True, default='Observação', max_length=200, null=True, verbose_name='Observação Fornecedor'),
        ),
    ]