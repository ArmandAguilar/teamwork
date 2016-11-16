#!user/bin/python
from tokens import *
import urllib2, base64
import json
import unicodedata
import sys
from datetime import datetime,time
reload(sys)
sys.setdefaultencoding("utf-8")

def costo_fijo():
    CostoF = 'Sql'
    #https://forta.teamwork.com/tasks/9486586/time_entries.json
    requestCostoFijoTask = urllib2.Request('https://forta.teamwork.com/projects/317730/time.json')
    requestCostoFijoTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseCostoFijoTask = urllib2.urlopen(requestCostoFijoTask)
    datajsonCostoFijoTask = json.loads(responseCostoFijoTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    for CostoFijoVal in datajsonCostoFijoTask['time-entries']:
        #Verificamo si tenga la tarea asiganda
        if CostoFijoVal['todo-item-id']  == "":
            valor = 0
        else:
            ProyectoArray = str(CostoFijoVal['todo-list-name']).split(" ")
            FechaJsonArrays = str(CostoFijoVal['date']).split("T")
            sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccionClon] VALUES (<Nombre, varchar(100),>,<Apellidos, varchar(100),>,\'' + ProyectoArray[0] + '\',\'' + ProyectoArray[1] + '\',\'', + FechaJsonArrays[0] + '\',\'' + CostoFijoVal['todo-item-name'] + '\',<Porcentaje, float,>,<Producto, float,>,<IdUsuario, int,>,<IdInternet, int,>,<Departamento, varchar(50),>,<Perfil, varchar(50),>,<Titulo, varchar(20),>,<Acronimo, varchar(50),>,<Programado, varchar(3),>,<IdTemaWork, int,>)'

    print(sql)
    print(FechaJsonArrays[0])
    return

costo_fijo()
