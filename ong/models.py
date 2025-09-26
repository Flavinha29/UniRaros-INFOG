from django.db import models

class Ong(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    link_doacao = models.URLField(blank=True, null=True)
    chave_pix = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome
