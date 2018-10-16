### example01 -------------------

mydict  =   { "alpha":0,
              "bravo":"0",
              "charlie":"three",
              "delta":[],
              "echo":False,
              "foxy":"False",
              "golf":"",
              "hotel":"   ",                        
            }
newdict =   dict([(vkey, vdata) for vkey, vdata in mydict.iteritems() if(vdata) ])
print newdict

### result01 -------------------
'''
{'foxy': 'False', 'charlie': 'three', 'hotel': '   ', 'bravo': '0'}
'''
