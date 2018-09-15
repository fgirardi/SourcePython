import re

match = re.search('([a-z]+)\s([a-z])', 'Guilherme Orlando Girardi')
if match:
	print("[{0}]".format(match.group(0)))
	print("[{0}]".format(match.group(1)))
	print("[{0}]".format(match.group(2)))
else:
	print('sad')
