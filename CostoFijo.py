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
            Horas = float(CostoFijoVal['hours'])
            Minutos = float(CostoFijoVal['minutes']) / 60
            HorasReal = Horas + Minutos
            if HorasReal is None:
                val = 'None'
            else:
                if HorasReal > 9:
                    Porcentaje = (HorasReal/HorasReal) * 100
                else:
                    Porcentaje = (HorasReal/9.0) * 100
                PorcentajeF = float("{0:.2f}".format(Porcentaje))
                sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccionClon] VALUES (Nombre,Apellidos,\'' + str(ProyectoArray[0]) + '\',\'' + str(ProyectoArray[1]) + '\',\',' + str(FechaJsonArrays[0]) + '\',\'' + str(CostoFijoVal['todo-item-name']) + '\',\'' + str(PorcentajeF) + '\',\'Producto\',\'IdUsuario\',\'0\',\'Departamento\',\'Perfil\',\'Titulo\',\'Acronimo\',\'Programado,\'' + CostoFijoVal['id'] + '\')'
                print(sql)
    #return sql

costo_fijo()
