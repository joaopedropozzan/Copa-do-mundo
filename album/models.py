from django.contrib.auth.models import User
from django.db import models

class Selecao(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Seleção"
        verbose_name_plural = "Seleções"

    def __str__(self):
        return self.nome


class Figurinha(models.Model):
    selecao = models.ForeignKey(Selecao, on_delete=models.CASCADE, related_name='figurinhas')
    nome_jogador = models.CharField(max_length=100)
    numero = models.IntegerField()
    posicao = models.CharField(max_length=50, blank=True, null=True)
    eh_rara = models.BooleanField(default=False)

    class Meta:
        unique_together = ('selecao', 'numero')
        ordering = ['selecao', 'numero']

    def __str__(self):
        return f"{self.selecao.nome} - {self.numero}: {self.nome_jogador}"


class AlbumUser(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='album')
    figurinha = models.ForeignKey(Figurinha, on_delete=models.CASCADE, related_name='colecionadores')
    quantidade = models.PositiveIntegerField(default=0)
    eh_repetida = models.BooleanField(default=False)

    class Meta:

        unique_together = ('usuario', 'figurinha')
        verbose_name = "Figurinha do Usuário"
        verbose_name_plural = "Abuns dos Usuários"

    def __str__(self):
        return f"{self.usuario.username} -> {self.figurinha} (Qtda: {self.quantidade})"
