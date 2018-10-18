from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic.base import View
from usuarios.forms import RegistrarUsuarioForm
from django.contrib.auth.models import User

# Create your views here.
class RegistrarUsuarioView(View):

	template_name = 'registrar.html'

	def get(self, request):
		return render(request, self.template_name)

	def post(self, request):
		form = RegistrarUsuarioForm(request.POST)
		if form.is_valid():
			dados_form = form.data
			usuario = User.objects.create_user(dados_form['nome'],
							   dados_form['email'],
							   dados_form['senha'])
			perfil = Perfil(nm_perfil=dados_form['nome'],
					ds_email=dados_form['email'],
					nr_telefone=dados_form['telefone'],
					nm_empresa=dados_form['nm_empresa'],
					usuario=usuario)
			perfil.save()
			return redirect('index')

		return render(request, self.template_name,{'form': form})
