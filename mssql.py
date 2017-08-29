#!/user/bin python
# -*- coding: utf-8 -*-
from tokens import *
import unicodedata
import pymssql
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def sql_delete_RegistoTiemposDiarios():
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute('DELETE  FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios]')
    conn.commit()
    conn.close()
    return conn
def sql_delete_RegistroProyectos():
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute('DELETE  FROM [SAP].[dbo].[AAARegistroProyecto]')
    conn.commit()
    conn.close()
    return conn
def sql_sentencia(sql):
    sentencia = ''
    try:
        senetencia = sql
        conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
    except ValueError:
        sentencia = '-------Error------:' + str(sql)
    return sentencia
