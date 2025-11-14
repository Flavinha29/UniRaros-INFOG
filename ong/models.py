from django.db import models

class Ong(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    contato = models.CharField(max_length=200, blank=True)
    site = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=30, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    imagem = models.ImageField(upload_to='ongs_imagens/', blank=True, null=True)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
