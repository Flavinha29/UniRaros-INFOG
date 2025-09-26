from django.db import models

class Sobre(models.Model):
    titulo = models.CharField(max_length=255)
    conteudo = models.TextField()
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
