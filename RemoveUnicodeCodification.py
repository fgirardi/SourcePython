import json, ast

#The u prefix means that those strings are unicode rather than 8-bit strings. The best way to not show the u prefix is to switch to Python 3, where strings are unicode by default. If that's not an
#option, the str constructor will convert from unicode to 8-bit, so simply loop recursively over the result and convert unicode to str. However, it is probably best just to leave the strings as
#unicode.


jdata = [{u'i': u'imap.gmail.com', u'p': u'aaaa'}, {u'i': u'333imap.com', u'p': u'bbbb'}]
jdata = ast.literal_eval(json.dumps(jdata))
print(jdata)
