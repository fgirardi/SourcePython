text = """> some_Varying_TEXT

DSJFKDAFJKDAFJDSAKFJADSFLKDLAFKDSAF
GATACAACATAGGATACA
GGGGGAAAAAAAATTTTTTTTT
CCCCAAAA

> some_Varying_TEXT2

DJASDFHKJFHKSDHF
HHASGDFTERYTERE
GAGAGAGAGAG
PPPPPAAAAAAAAAAAAAAAP
"""

import re

regex = re.compile(r'^>([^\n\r]+)[\n\r]([A-Z\n\r]+)', re.MULTILINE)
matches = [m.groups() for m in regex.finditer(text)]

for m in matches:
    print 'Name: %s\nSequence:%s' % (m[0], m[1])
