import re

#r = raw string cru nao escapa nada
regexp = r'(\d\d)(\w)'
match = '12a563a2223a
         fabiano girardi'

result = re.search(regexp, match)
print result.group()

results = re.finditer(regexp, match)

for result in results:
	print("%s | %s | %s | [%s-%s]" % (result.group(0), result.group(1), result.group(2), result.start(), result.end()))
