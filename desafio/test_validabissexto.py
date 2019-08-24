import unittest
from validabissexto import *

class TestAvaliador(unittest.TestCase):

	def test_avalia(self):
		'''
		Este teste valida se a data informada eh valida
		'''
		validaBissexto = ValidaBissexto()

		#Consiste um ano invalido
		ano = -1
		res_esperado = False
		self.assertEqual(res_esperado, validaBissexto.setAno(ano))

	def test_bissexto_true(self):
		'''
		Verifica se o ano eh bissexto resultado esperado True 
		'''
		validaBissexto = ValidaBissexto()
		ano = 2020 
		res_esperado = True
		ig = validaBissexto.setAno(ano)
		self.assertEqual(res_esperado, validaBissexto.isBissexto())

	def test_bissexto_false(self):
		'''
		Verifica se o ano eh bissexto resultado esperado False
		'''
		validaBissexto = ValidaBissexto()
		ano = 2021 
		ig = validaBissexto.setAno(ano)
		res_esperado = False
		self.assertEqual(res_esperado, validaBissexto.isBissexto())

if __name__ == '__main__':
	unittest.main()


