#!user/bin/python
from tokens import *
from projects import *
from task import *
from mssql import *
import urllib2, base64
import json
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pymssql
print ("############################ Start Sync Datos Teamwork ############################")
#Borramos datos de las tablas :
#sql_delete_RegistoTiemposDiarios()
#sql_delete_RegistroProyectos()
#1.- Lista de Proyectos
for proyecto in projectos_id:
#2.- Buscamos las tareas de cada proyectos
    print("------------------- Begin Task -------------------")
    task(proyecto)
    print("------------------- End Task -------------------")
    print("------------------- Begin TaskRegistroProyectos -------------------")
    TaskRegistroProyectos(proyecto)
    print("------------------- End TaskRegistroProyectos -------------------")

print("------------------- Begin ReordenarSAP -------------------")
print(ReordenarSAP())
print("------------------- End ReordenarSAP -------------------")
print ("############################ End Sync Datos Teamwork  ############################")
