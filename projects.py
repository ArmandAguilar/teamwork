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
        Vacio = ""
    elif datos['id'] == '271006':
        Vacio = ""
    elif datos['id'] == '237790':
        Vacio = ""
    elif datos['id'] == '258970':
        Vacio = ""
    elif datos['id'] == '251282':
        Vacio = ""
    elif datos['id'] == '306189':
        Vacio = ""
    elif datos['id'] == '273773':
        Vacio = "1"
    else:
        ##print(str(datos['id']) + '.-' + str(datos['name']) )
        ProyectoArray = str(datos['name']).split(" ")
        projectos_id.insert(k,str(datos['id']))

#print projectos_id
