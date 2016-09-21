#!user/bin/python
from tokens import *
import pymssql


def validate_up_in(IdTareas,IdProyecto,IdUsuario,ListaTarea):
    accion = 'Insert'
    sql_buscar = 'SELECT [IdTareas] FROM [SAP].[dbo].[AAARegistroProyecto] Where [IdTareas]=\'' + str(IdTareas) + '\' and [IdProyecto]=\'' + str(IdProyecto) + '\' and [IdUsuario]=\'' + str(IdUsuario) + '\' and [ListaTarea]=\'' + str(ListaTarea) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
        accion = 'Update'
    conn.commit()
    conn.close()
    return accion

def validate_up_in_AAARegistroDeTiemposDiarios(idTaskTeamwork):
    accion = 'Insert'
    sql_buscar = 'SELECT [IdTarea] FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] where [IdTeam] = \'' + str(idTaskTeamwork) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
        accion = 'Update'
    conn.commit()
    conn.close()
    return accion

def validar_100(idUsuario,Dia):
    Accion = 'No'
    Porcentaje = 0.0
    sql_buscar = 'SELECT [Porcentaje] FROM [SAP].[dbo].[AATiemposDeProduccionClon] Where [IdUsuario] = \'' + str(idUsuario) + '\' and  Dia=\'' + str(Dia) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
         Porcentaje = Porcentaje + float(value[0])
    conn.commit()
    conn.close()
    if Porcentaje >= 100:
        Accion = 'Si'
    return Accion
