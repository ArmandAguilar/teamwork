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

cargardo()

proceso('Corrigiendo Tiempo Diarios')

print ("############################ End Sync Datos Teamwork  ############################")
