from django.db import models

class Perfil(models.Model):

	nm_perfil = models.CharField(max_length=255, null=False)
	ds_email = models.CharField(max_length=255, null=False)
	nr_telefone = models.CharField(max_length=20, null=False)
	nm_empresa = models.CharField(max_length=255, null=False)
