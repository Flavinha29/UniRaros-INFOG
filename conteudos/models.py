from django.db import models

class Conteudo(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
