#!user/bin/python
from tokens import *
import urllib2, base64
import json
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

request = urllib2.Request("https://forta.teamwork.com/projects.json")
request.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
response = urllib2.urlopen(request)
datajson = json.loads(response.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
projectos_id = []
k = 0
for datos in datajson['projects']:

    if datos['id'] == '271006':
        Vacio = "o"
    elif datos['id'] == '237790':
        Vacio = "o"
    elif datos['id'] == '258970':
        Vacio = "o"
    elif datos['id'] == '251282':
        Vacio = "o"
    elif datos['id'] == '306189':
        Vacio = "o"
    elif datos['id'] == '273773':
        Vacio = "o"
    elif datos['id'] == '314193':
        Vacio = "o"
    elif datos['id'] == '317730':
        Vacio = "o"
    elif datos['id'] == '317767':
        Vacio = "o"
    elif datos['id'] == '317752':
        Vacio = "o"
    elif datos['id'] == '317730':
        Vacio = "o"
    elif datos['id'] == '323850':
        Vacio = "o"
    elif datos['id'] == '321120':
        Vacio = "o"
    elif datos['id'] == '321122':
        Vacio = "o"
    elif datos['id'] == '321533':
        Vacio = "o"
    elif datos['id'] == '321123':
        Vacio = "o"
    elif datos['id'] == '323789':
        Vacio = "o"
    elif datos['id'] == '323016':
        Vacio = "o"
    elif datos['id'] == '317749':
        Vacio = "o"
    elif datos['id'] == '385329':
        Vacio = "o"
    elif datos['id'] == '377496':
        Vacio = "o"
    elif datos['id'] == '393042':
        Vacio = "o"
    elif datos['id'] == '381402':
        Vacio = "o"
    elif datos['id'] == '402515':
        Vacio = "o"
    elif datos['id'] == '404137':
        Vacio = "o"
    elif datos['id'] == '413494':
        Vacio = "o"
    elif datos['id'] == '419603':
        Vacio = "o"
    elif datos['id'] == '419712':
        Vacio = "o"
    elif datos['id'] == '420710':
        Vacio = "o"
    elif datos['id'] == '420741':
        Vacio = "o"
    elif datos['id'] == '402515':
        Vacio = "o"
    elif datos['id'] == '336576':
        Vacio = "o"
    elif datos['id'] == '420774':
        Vacio = "o"
    elif datos['id'] == '416311':
        Vacio = "o"
    elif datos['id'] == '418014':
        Vacio = "o"
    elif datos['id'] == '411841':
        Vacio = "o"
    else:
        #print(str(datos['id']) + '.-' + str(datos['name']) )
        ProyectoArray = str(datos['name']).split(" ")
        #Aks is the first array is number
        CadValue = unicode(ProyectoArray[0])
        if CadValue.isnumeric():
            if str(datos['id']) == '0000':
                varr = 0
            else:
                projectos_id.insert(k,str(datos['id']))
        else:
            valor = (str(ProyectoArray[0]))
#print projectos_id
