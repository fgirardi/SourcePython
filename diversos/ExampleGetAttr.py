class ABC():
	x = "Some Value"
	y = ""

	def SetY(self, value):
		print("Debug SetY {0}".format(value))
		self.y = value


obj = ABC()

print("x {0}".format(obj.x))


print(getattr(obj,"x"))

getattr(obj,"SetY")("200")

print("obj.y={0}".format(obj.y))


setattr(obj,"a","definition of a")

print(obj.a)
