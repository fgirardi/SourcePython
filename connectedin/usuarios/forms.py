from django import forms
from django.contrib.auth.models import User

class RegistrarUsuarioForm(forms.Form):

	nn_usuario = forms.CharField(required=True)
	ds_email = forms.EmailField(required=True)
	ds_senha = forms.CharField(required=True)
	nr_telefone = forms.CharField(required=True)
	nm_empresa = forms.CharField(required=True)

	def is_valid(self):
		valid = True
		if not super(RegistrarUsuarioForm, self).is_valid():
			self.adiciona_erro('Por favor, verifique os dados informados')
			valid = False
		#Testing if the user already exists. key is name
		user_exists = User.objects.filter(username=self.data['nome']).exists()
		if user_exists:
			self.adiciona_erro('Usuario ja existe')
			valid = False 

		return valid

	def adiciona_erro(self, message):
		erros = self._erros.setdefault(forms.forms.NON_FIELD_ERROS,forms.utils.ErrorList())
		error.append(message)
