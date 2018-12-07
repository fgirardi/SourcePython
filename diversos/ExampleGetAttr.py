class ABC():
	x = "Some Value"

obj = ABC()

print(obj.x)


print(getattr(obj,"x"))
