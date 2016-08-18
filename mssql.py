#!/user/bin python
# -*- coding: utf-8 -*-
import unicodedata
import pymssql
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def sql_sentencia(sql):
    conn = pymssql.connect(host=hostMSSQL,user='',password='',database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    return conn
