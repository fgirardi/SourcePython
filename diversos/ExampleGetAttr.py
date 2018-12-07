class ABC():
	x = "Some Value"

obj = ABC()

print(obj.x)


print(getattr(obj,"x"))


setattr(obj,"a","definiton of a")

print(obj.a)
