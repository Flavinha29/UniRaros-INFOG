from django.db import models
from django.utils import timezone

class Conteudo(models.Model):
    CATEGORIAS = [
        ('Genética', 'Genética'),
        ('Neurológica', 'Neurológica'),
        ('Metabólica', 'Metabólica'),
        ('Imunológica', 'Imunológica'),
        ('Outras', 'Outras'),
    ]

    nome = models.CharField(max_length=200)
    resumo = models.CharField(max_length=300, blank=True)
    descricao_completa = models.TextField(blank=True)
    sintomas = models.TextField(blank=True)
    diagnostico = models.TextField(blank=True)
    tratamento = models.TextField(blank=True)

    imagem = models.ImageField(upload_to='conteudos_imagens/', blank=True, null=True)
    arquivo_pdf = models.FileField(upload_to='conteudos_pdfs/', blank=True, null=True)

    link_referencia = models.URLField(max_length=300, blank=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='Outras')

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome