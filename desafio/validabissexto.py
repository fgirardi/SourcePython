import os

class Interface:

	def __init__(self):
		self.valorSaida = -1 
		self.msgRequest = "Informe o Ano:"
		self.msgSair = "Informe {0} para sair"
		self.msgResultado = "Ano {0} bissexto {1}"
		self.msgAnoInvalido = "O ano informado {0} deve ser maior igual que 0 e menor que 9999"

	def getValorSaida(self):
		return self.valorSaida

	def getMsgAnoInvalido(self, ano):
		return self.msgAnoInvalido.format(ano)

	def getMsgResultado(self, ano, isBissexto):
		return self.msgResultado.format(ano, "Sim" if isBissexto == True else "Nao")

	def getMsgRequest(self):
		return input(self.msgRequest)

	def getMsgSair(self):
		return self.msgSair.format(self.valorSaida)

class ValidaBissexto:

	def __init__(self):
		self.nrAno = 0

	def getAno(self):
		return self.nrAno

	def setAno(self ,ano):
		'''
		Funcao que consiste e set o atributo ano, retorna True qdo tiver setado
		'''
		if ano >= 0 and ano <= 9999:
			self.nrAno = ano
			return True

		return False
	
	def isBissexto(self):
		'''
		Retorna True para ano bissexto
		'''
		return (self.nrAno%4 == 0 and self.nrAno%100 != 0) or (self.nrAno%400 == 0)

def main():
	interface = Interface()
	validaBissexto = ValidaBissexto()
	os.system('cls||clear')
	while True:
		print(interface.getMsgSair())
		ano = interface.getMsgRequest()
		if ano == interface.getValorSaida():
			break
		os.system('cls||clear')
		if validaBissexto.setAno(ano):
			print(interface.getMsgResultado(ano, validaBissexto.isBissexto()))
		else:
			print(interface.getMsgAnoInvalido(ano))

if __name__ == '__main__':
	main()

