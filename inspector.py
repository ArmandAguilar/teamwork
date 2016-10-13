#!user/bin/python
from tokens import *
import urllib2, base64
import json
import unicodedata
import sys
import pypyodbc as pyodbc
reload(sys)
sys.setdefaultencoding("utf-8")

def ExisteTarea(IdTask):
    urlTarea = 'https://forta.teamwork.com/tasks/' + str(IdTask) + '.json'
    Status = 'Oka'
    #try:
    #    request = urllib2.Request(urlTarea)
    #    request.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    #    response = urllib2.urlopen(request)
    #    datajson = json.loads(response.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    #    Status = datajson['STATUS']
    #except Exception as e:
    #    Status = 'Elimina'
    return Status  + '-' + str(IdTask)

def Corregir():
    #1 .- Leemos la base de datos y obtenemos los id de teamwork
    sql = 'SELECT [IdTeam] FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] order by [IdTeam] desc'
    con = pyodbc.connect(constr)
    cur = con.cursor()
    cur.execute(sql)
    for value in cur:
        Llave = value[0]
        print(Llave)
        #ExisteTarea(str(Llave))
    con.commit()
    con.close()

#def BorramosIdNoExitente(Id):
#    sql='Delete FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] Where [IdTeam] =  \'' + str(Id) + '\''
#    con = pyodbc.connect(constr)
#    cur = con.cursor()
#    cur.execute(sql)
#    con.commit()
#    con.close()
print ("############################ Begin Revinsado Datos de la Tabla AAARegistroDeTiemposDiarios ############################")
print Corregir()
print ("############################ End Revinsado Datos de la Tabla AAARegistroDeTiemposDiarios ############################")
