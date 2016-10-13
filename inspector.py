#!user/bin/python
from tokens import *
import urllib2, base64
import json
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def ExisteTarea(IdTask):
    request = urllib2.Request('https://forta.teamwork.com/tasks/' + str(IdTask) + '.json')
    request.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    response = urllib2.urlopen(request)
    datajson = json.loads(response.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    Status = datajson['status']
    return Status

#def Corregir(arg):
#    #1 .- Leemos la base de datos y obtenemos los id de teamwork
#    sql = 'SELECT [IdTeam] FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] order by [IdTeam] desc'
#    con = pyodbc.connect(constr)
#    cur = con.cursor()
#    for value in cur:
#        pass
#    cur.execute(sql)
#    con.commit()
#    con.close()

#def BorramosIdNoExitente(Id):
#    sql='Delete FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] Where [IdTeam] =  \'' + str(Id) + '\''
#    con = pyodbc.connect(constr)
#    cur = con.cursor()
#    cur.execute(sql)
#    con.commit()
#    con.close()

print ExisteTarea(11111)
