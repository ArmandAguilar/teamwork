#!user/bin/python
from tokens import *
import pymssql


def validate_up_in(IdTareas,IdProyecto,IdUsuario,ListaTarea):
    sql_buscar = 'SELECT [IdTareas] FROM [SAP].[dbo].[AAARegistroProyecto] Where [IdTareas]=\'' + IdTareas + '\' and [IdProyecto]=\'' + IdProyecto + '\' and [IdUsuario]=\'' + IdUsuario + '\' and [ListaTarea]=\'' + ListaTarea + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
        print value
    conn.commit()
    conn.close()
    return value
