#!user/bin/python
from tokens import *
from projects import *
from task import *
import urllib2, base64
import json
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import pymssql
print ("############################ Start Sync Datos Teamwork ############################")
#1.- Lista de Proyectos
for proyecto in projectos_id:
#2.- Buscamos las tareas de cada proyectos
    task(proyecto)
    #TaskRegistroProyectos(proyecto)

print ("############################ End Sync Datos Teamwork  ############################")
