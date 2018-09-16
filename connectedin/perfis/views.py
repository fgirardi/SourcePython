from django.shortcuts import render
from perfis.models import Perfil

def index(request):
	return render(request, 'index.html')

def exibir(request, perfil_id):

	perfil = Perfil()

	if perfil_id == '1':
		perfil = Perfil('Fabiano Girardi',
				'fabiano.girardi@hotmail.com', 
				'77777',
				'Fgirardi ME')
	if perfil_id == '2':
		perfil = Perfil('Guilherme Orlando Girardi',
				'guilherme.girardi@hotmail.com', 
				'88888',
				'Fgirardi ME')


		return render(request, 'perfil.html',{"perfil" : perfil})
