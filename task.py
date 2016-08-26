#!user/bin/python
from tokens import *
from mssql import *
import urllib2, base64
import json
import unicodedata
import sys
from datetime import datetime,time
reload(sys)
sys.setdefaultencoding("utf-8")

def task(arg):
    if arg == '281337':
        requestTask = urllib2.Request("https://forta.teamwork.com/projects/" + str(arg)  +"/tasks.json")
        requestTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
        responseTask = urllib2.urlopen(requestTask)
        datajsonTaks = json.loads(responseTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
        i = 0
        for Task in datajsonTaks['todo-items']:
            i += 1
            if Task.get('responsible-party-ids') is None:
                #print ('[++Task('+ str(Task['id']) +'): ' + str(Task['content']) + ' Responsable: None ]')
                valor = '0'
            else:
                #print ('--[Task('+ str(Task['id']) +'): ' + str(Task['content']) + ']')
                #print ('---->Responsable: ' + str(Task['responsible-party-ids']) + ' | ' + str(Task['responsible-party-names']))
                TaksTiempoDiarios(str(Task['id']))

def TaksTiempoDiarios(idtask):
    sql_delete_RegistoTiemposDiarios()
    requestActivitiesTask = urllib2.Request('https://forta.teamwork.com/tasks/' + str(idtask) + '/time_entries.json')
    requestActivitiesTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseActivitiesTask = urllib2.urlopen(requestActivitiesTask)
    datajsonActivitiesTask = json.loads(responseActivitiesTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    for activities in datajsonActivitiesTask['time-entries']:
        #print ('------>Tarea:' + str(activities['parentTaskName']) + '-' + str(activities['todo-item-name']) + ' Ejecutor:' + str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + ' Id:' + str(activities['person-id']))
        ProyectoArray = str(activities['project-name']).split(" ")
        FechaJsonArrays = str(activities['date']).split("T")
        Descripcion = str(activities['parentTaskName']) + '-' + str(activities['todo-item-name']) + '-' + str(activities['todo-list-name'])
        sql = 'Insert Into [SAP].[dbo].[AAARegistroDeTiemposDiarios] values(\'' +str(idtask) + '\',\'' + str(activities['person-id']) + '\',\'' + ProyectoArray[0] + '\',\''+ str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + '\',\'' + str(Descripcion) + '\',\'' + FechaJsonArrays[0] + '\',\'' + str(activities['hours']) + '\')'
        conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.close()
        #print sql_sentencia(sql)
        print (str(sql))


def TaskRegistroProyectos(idproyect):

    requestProyectTask = urllib2.Request('https://forta.teamwork.com/projects/' + str(idproyect) + '/tasks.json')
    requestProyectTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseProyectTask = urllib2.urlopen(requestProyectTask)
    datajsonProyectTask = json.loads(responseProyectTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    for ProyectTask  in datajsonProyectTask['todo-items']:
        ProyectoArray = str(ProyectTask['project-name']).split(" ")
        IdResposnable = ''
        ParentTask = ''
        if ProyectTask.get('responsible-party-id') is None:
            IdResposnable = ''
        else:
            IdResposnable = ProyectTask['responsible-party-ids']
        if ProyectTask.get('responsible-party-ids') is None:
            IdResposnable = ''
        else:
            IdResposnable = ProyectTask['responsible-party-id']
        if ProyectTask.get('parentTaskId') is None:
            ParentTask = ''
        else:
            ParentTask = ProyectTask['parentTaskId']
        EtiqFase = '---'
        EtiqDocumento = '---'
        EtiqDisciplina = '---'
        sql = 'Insert into AARegistroProyecto values(\''  + str(ProyectTask['id']) + '\',\'' + ProyectoArray[0] +'\',\'' + str(IdResposnable) + '\',\''+ str(ProyectTask['content']) + '\',\'' + str(ParentTask) + '\',\'' + str(ProyectTask['start-date']) + '\',\'' + str(ProyectTask['due-date-base']) + '\',\'' + str(ProyectTask['due-date']) + '\',\'' + str(ProyectTask['progress']) + '\',\'' + str(ProyectTask['completed']) + '\',\'EtiqFase\',\'EtiqDocumento\',\'EtiqDisciplina\',\'' + str(ProyectTask['description']) + '\',\'' + str(ProyectTask['estimated-minutes']) + '\')'
        print (sql)
