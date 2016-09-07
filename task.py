#!user/bin/python
from tokens import *
from mssql import *
from validate import *
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
                print ('[++Task('+ str(Task['id']) +'): ' + str(Task['content']) + ' Responsable: None ]')
                valor = '0'
            else:
                print ('--[Task('+ str(Task['id']) +'): ' + str(Task['content']) + ']')
                print ('---->Responsable: ' + str(Task['responsible-party-ids']) + ' | ' + str(Task['responsible-party-names']))
                TaksTiempoDiarios(str(Task['id']))

def TaksTiempoDiarios(idtask):
    requestActivitiesTask = urllib2.Request('https://forta.teamwork.com/tasks/' + str(idtask) + '/time_entries.json')
    requestActivitiesTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseActivitiesTask = urllib2.urlopen(requestActivitiesTask)
    datajsonActivitiesTask = json.loads(responseActivitiesTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    #Aqui se programa un diccionario para validar los dias y insterar o actualizar el regisro
    for activities in datajsonActivitiesTask['time-entries']:
        print ('------>Tarea:' + str(activities['parentTaskName']) + '-' + str(activities['todo-item-name']) + ' Ejecutor:' + str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + ' Id:' + str(activities['person-id']))
        ProyectoArray = str(activities['project-name']).split(" ")
        FechaJsonArrays = str(activities['date']).split("T")
        Descripcion = str(activities['parentTaskName']) + '-' + str(activities['todo-item-name']) + '-' + str(activities['todo-list-name'])

        sql = 'Insert Into [SAP].[dbo].[AAARegistroDeTiemposDiarios] values(\'' +str(idtask) + '\',\'' + str(activities['person-id']) + '\',\'' + ProyectoArray[0] + '\',\''+ str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + '\',\'' + str(Descripcion) + '\',\'' + FechaJsonArrays[0] + '\',\'' + str(activities['hours']) + '\',\'' + activities['id']+ '\')'
        sql_sentencia(sql)
        print (str(sql))
#funcion que registra  en AAARegistroProyecto
def TaskRegistroProyectos(idproyect):

    requestProyectTask = urllib2.Request('https://forta.teamwork.com/projects/' + str(idproyect) + '/tasks.json')
    requestProyectTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseProyectTask = urllib2.urlopen(requestProyectTask)
    datajsonProyectTask = json.loads(responseProyectTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    for ProyectTask  in datajsonProyectTask['todo-items']:
        ProyectoArray = str(ProyectTask['project-name']).split(" ")
        IdResposnable = 0
        ParentTask = ''
        if ProyectTask.get('responsible-party-id') is None:
            IdResposnable = 0
        else:
            IdResposnable = ProyectTask['responsible-party-ids']
        if ProyectTask.get('responsible-party-ids') is None:
            IdResposnable = 0
        else:
            IdResposnable = ProyectTask['responsible-party-id']
        if ProyectTask.get('parentTaskId') is None:
            ParentTask = '0'
        else:
            ParentTask = ProyectTask['parentTaskId']
            if ParentTask == '':
                ParentTask = '0'
            else:
                ParentTask = ProyectTask['parentTaskId']
        EtiqFase = '---'
        EtiqDocumento = '---'
        EtiqDisciplina = '---'
        #StartDate
        if ProyectTask['start-date'] is None:
            StartDate = '1999-01-01 00:00:00'
        else:
            if ProyectTask['start-date'] == '':
                StartDate = '1999-01-01 00:00:00'
            else:
                StartDate = datetime.strptime(str(ProyectTask['start-date']),'%Y%m%d')

        #DueDateBase
        if ProyectTask['due-date-base'] is None:
            DueDateBase = '1999-01-01 00:00:00'
        else:
            if ProyectTask['due-date-base'] == '':
                DueDateBase = '1999-01-01 00:00:00'
            else:
                DueDateBase = datetime.strptime(str(ProyectTask['due-date-base']),'%Y%m%d')

        #DueDate
        if ProyectTask['due-date'] is None:
            DueDate = '1999-01-01 00:00:00'
        else:
            if ProyectTask['due-date'] == '':
                DueDate = '1999-01-01 00:00:00'
            else:
                DueDate = datetime.strptime(str(ProyectTask['due-date']),'%Y%m%d')
        #Aqui se programa un diccionario para validar los dias y insterar o actualizar el regisro
        tipoConsulta = ''
        #IdUsuario
        try:
            int(IdResposnable)
            tipoConsulta = validate_up_in(str(ProyectTask['id']),ProyectoArray[0],str(IdResposnable),str(ParentTask))
            if tipoConsulta == 'Insert':
                sql = 'Insert into AAARegistroProyecto values(\''  + str(ProyectTask['id']) + '\',\'' + ProyectoArray[0] +'\',\'' + str(IdResposnable) + '\',\''+ str(ProyectTask['content']) + '\',\'' + str(ParentTask) + '\',\'' + str(StartDate) + '\',\'' + str(DueDateBase) + '\',\'' + str(DueDate) + '\',\'' + str(ProyectTask['progress']) + '\',\'' + str(ProyectTask['completed']) + '\',\'EtiqFase\',\'EtiqDocumento\',\'EtiqDisciplina\',\'' + str(ProyectTask['description']) + '\',\'' + str(ProyectTask['estimated-minutes']) + '\')'
            else:
                sql = 'UPDATE [SAP].[dbo].[AAARegistroProyecto] SET [Tarea] = \'' + str(ProyectTask['content']) + '\',[FechaIncio] = \'' + str(StartDate) + '\',[FechaFinalProgramada] = \'' + str(DueDateBase) + '\',[FehaFinalR] = \'' + str(DueDate) + '\',[Avance] = \'' + str(ProyectTask['progress']) + '\',[Completada] = \'' + str(ProyectTask['completed']) + '\',[EtqFase] = \'----\',[EtqDocumento] = \'---\',[EtqDiciplina] = \'---\',[Cantidad] = \'\',[TiempoEstimado] = \'\' WHERE [IdTareas]=\'' + str(ProyectTask['id']) + '\' and [IdProyecto]=\'' + ProyectoArray[0] + '\' and [IdUsuario]=\'' + str(IdResposnable) + '\' and [ListaTarea]=\'' + str(ParentTask) + '\''
            print (str(sql))
            sql_sentencia(sql)
        except ValueError:
            #print ('cadean' + '.-' + str(IdResposnable))
            AIdResposnable = str(IdResposnable).split(",")
            for idUser in AIdResposnable:
                #print ('algos' + '.-' + str(idUser))
                tipoConsulta = validate_up_in(str(ProyectTask['id']),ProyectoArray[0],str(idUser),str(ParentTask))
                if tipoConsulta == 'Insert':
                    sql = 'Insert into AAARegistroProyecto values(\''  + str(ProyectTask['id']) + '\',\'' + ProyectoArray[0] +'\',\'' + str(idUser) + '\',\''+ str(ProyectTask['content']) + '\',\'' + str(ParentTask) + '\',\'' + str(StartDate) + '\',\'' + str(DueDateBase) + '\',\'' + str(DueDate) + '\',\'' + str(ProyectTask['progress']) + '\',\'' + str(ProyectTask['completed']) + '\',\'EtiqFase\',\'EtiqDocumento\',\'EtiqDisciplina\',\'' + str(ProyectTask['description']) + '\',\'' + str(ProyectTask['estimated-minutes']) + '\')'
                else:
                    #update
                    sql = 'UPDATE [SAP].[dbo].[AAARegistroProyecto] SET [Tarea] = \'' + str(ProyectTask['content']) + '\',[FechaIncio] = \'' + str(StartDate) + '\',[FechaFinalProgramada] = \'' + str(DueDateBase) + '\',[FehaFinalR] = \'' + str(DueDate) + '\',[Avance] = \'' + str(ProyectTask['progress']) + '\',[Completada] = \'' + str(ProyectTask['completed']) + '\',[EtqFase] = \'----\',[EtqDocumento] = \'---\',[EtqDiciplina] = \'---\',[Cantidad] = \'\',[TiempoEstimado] = \'\' WHERE [IdTareas]=\'' + str(ProyectTask['id']) + '\' and [IdProyecto]=\'' + ProyectoArray[0] + '\' and [IdUsuario]=\'' + str(idUser) + '\' and [ListaTarea]=\'' + str(ParentTask) + '\''
                sql_sentencia(sql)
                print (str(sql))
