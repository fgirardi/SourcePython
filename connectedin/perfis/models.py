from django.db import models

class Perfil(models.Model):
	# quando herdar de models.Model, nao precisa do construtor __init__
	nm_perfil = models.CharField(max_length=255, null=False)
	ds_email = models.CharField(max_length=255, null=False)
	nr_telefone = models.CharField(max_length=20, null=False)
	nm_empresa = models.CharField(max_length=255, null=False)

	def convidar(self, perfil_convidado):
		Convite(solicitante = self, convidado = perfil_convidado).save()

class Convite(models.Model):

	solicitante = models.ForeignKey(Perfil, related_name = 'convites_feitos')
	convidado = models.ForeignKey(Perfil, related_name = 'convites_recebidos')
