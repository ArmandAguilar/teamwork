#!/user/bin python
# -*- coding: utf-8 -*-
from tokens import *
import unicodedata
import pymssql
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def sql_sentencia(sql):
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    return conn
def sql_delete_RegistoTiemposDiarios():
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute('DELETE  FROM [SAP].[dbo].[AARegistroTiemposDiarios]')
    conn.commit()
    conn.close()
    return conn
