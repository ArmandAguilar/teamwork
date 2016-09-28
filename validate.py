#!user/bin/python
from tokens import *
import pymssql


def validate_up_in(IdTareas,IdProyecto,IdUsuario,ListaTarea):
    accion = 'Insert'
    sql_buscar = 'SELECT [IdTareas] FROM [SAP].[dbo].[AAARegistroProyecto] Where [IdTareas]=\'' + str(IdTareas) + '\' and [IdProyecto]=\'' + str(IdProyecto) + '\' and [IdUsuario]=\'' + str(IdUsuario) + '\' and [ListaTarea]=\'' + str(ListaTarea) + '\''
    print(sql_buscar)
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
    Accion = 'Si'
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
        Accion = 'No'
    return Accion
#funcion que verifica la 9 hrs
def time9(IdUserTeam,Dia):
    Varicado9hrs = 'No'
    sql_verifica9hrs = 'SELECT [Tiempo] FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] IdUsuario=\'' + str(IdUserTeam) + '\' and Dia=\'' + str(Dia) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_verifica9hrs)
    for value in cur:
         SumHoras = SumHoras + float(value[0])
    conn.commit()
    conn.close()
    if SumHoras >= 9:
        Varicado9hrs = 'Si'
    return
#Esta funcion borra un dia
def BorramosDia(IdUsuarioTeam,Dia):
    sql_borrar ='DELETE FROM [SAP].[dbo].[AATiemposDeProduccionClon] WHERE IdUsuario=\'' + str(IdUsuarioTeam) + '\' and Dia=\'' + str(Dia) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_borrar)
    conn.commit()
    conn.close()
    return sql_borrar
