#!user/bin/python
import sys
from tokens import *
from projects import *
from task import *
from mssql import *
import urllib2, base64
import json
import unicodedata
import pypyodbc as pyodbc
import pymssql
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
from mensajes import *
sys.setdefaultencoding("utf-8")
print ("############################ Start Sync Datos Teamwork ############################")
#Borramos datos de las tablas :
#sql_delete_RegistoTiemposDiarios()
#sql_delete_RegistroProyectos()
#1.- Lista de Proyectos
cargardo()

for proyecto in projectos_id:
#2.- Buscamos las tareas de cada proyectos
    task(proyecto)
    TaskRegistroProyectos(proyecto)
    #print (proyecto)

proceso('Corrigiendo Tiempo Diarios')
EliminarCambioEnTiemposDiarios()

#proceso('Procsnado SAP')
#ParaSAP()

proceso_terminado()
print ("############################ End Sync Datos Teamwork  ############################")
