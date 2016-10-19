#!user/bin/python
from tokens import *
from mssql import *
from validate import *
from sap import *
import urllib2, base64
import json
import unicodedata
import sys
from datetime import datetime,time
reload(sys)
sys.setdefaultencoding("utf-8")

def task(arg):
    #if arg == '281337':
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
#funcion que registra  en #funcion que registra  en AAARegistroProyecto
def TaksTiempoDiarios(idtask):
    requestActivitiesTask = urllib2.Request('https://forta.teamwork.com/tasks/' + str(idtask) + '/time_entries.json')
    requestActivitiesTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseActivitiesTask = urllib2.urlopen(requestActivitiesTask)
    datajsonActivitiesTask = json.loads(responseActivitiesTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    #Aqui se programa un diccionario para validar los dias y insterar o actualizar el regisro
    tipoConsultas = ''

    for activities in datajsonActivitiesTask['time-entries']:
        #print ('------>Tarea:' + str(activities['parentTaskName']) + '-' + str(activities['todo-item-name']) + ' Ejecutor:' + str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + ' Id:' + str(activities['person-id']))
        ProyectoArray = str(activities['project-name']).split(" ")
        FechaJsonArrays = str(activities['date']).split("T")
        Descripcion = str(activities['parentTaskName']) + '-' + str(activities['todo-item-name']) + '-' + str(activities['todo-list-name'])
        #Validamos si es una actualizacion o un insert
        tipoConsultas=validate_up_in_AAARegistroDeTiemposDiarios(activities['id'])
        if tipoConsultas == 'Insert':
            sql = 'Insert Into [SAP].[dbo].[AAARegistroDeTiemposDiarios] values(\'' +str(idtask) + '\',\'' + str(activities['person-id']) + '\',\'' + ProyectoArray[0] + '\',\''+ str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + '\',\'' + str(Descripcion) + '\',\'' + FechaJsonArrays[0] + '\',\'' + str(activities['hours']) + '\',\'' + str(activities['id']) + '\')'
        else:
            UserName = str(activities['person-first-name']) + ' ' + str(activities['person-last-name'])
            sql = 'UPDATE [SAP].[dbo].[AAARegistroDeTiemposDiarios] SET [IdUsuario] = \'' + str(activities['person-id']) + '\',[IdProyecto] = \'' + ProyectoArray[0] + '\',[Usuario] = \'' + str(UserName)  + '\',[Descripcion] = \'' +  str(Descripcion)  + '\',[Fecha] = \'' + FechaJsonArrays[0] + '\',[Tiempo] = \'' + str(activities['hours']) + '\' WHERE [IdTeam] = \'' + str(activities['id']) + '\''
            #Falata localizar el tiempo
            #BorramosDia(str(activities['person-id']),FechaJsonArrays[0],)

        sql_sentencia(sql)
        #Quite esta zona
        #Aqui Verificamos si el registo del usuario cumple con las nueve 9 o mas
        #Si.- El registro es >=9 insertamos en la tambla de AAARegistrosDeProduccionClon
        #No .- Seleciionamos Dia y Usuario y lo borramos si ya existe en el sistema
        #Si es actualizacion de un dia borramos el dia y se carga de nuevo si es >=9
        #Dos agumentos ne la funcion time9
        #
        #mayoriguala9 = time9(str(activities['person-id']),str(FechaJsonArrays[0]))
        #if mayoriguala9 == 'No':
            #Preparamos el dicionario para insertar datos en sap
            #print ('-------------!!! Kawuabonga !!!------------------')
            #DirSAP['NumProyecto'] = ProyectoArray[0]
            #DirSAP['Dia'] = FechaJsonArrays[0]
            #DirSAP['Tarea'] = str(Descripcion)
            #DirSAP['IdUsuarioTeam'] = str(activities['person-id'])
            #DirSAP['Horas'] = str(activities['hours'])
            #DirSAP['IdJson'] = str(activities['id'])
            #print (str(sap_insert(DirSAP)))
        #print ('-------------------------------')
        #print (str(sql))
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
        Tarea = ProyectTask['content']
        Tarea = str(Tarea).replace('\'','.')
        print (str(Tarea))
        #IdUsuario
        try:
            int(IdResposnable)

            tipoConsulta = validate_up_in(str(ProyectTask['id']),ProyectoArray[0],str(IdResposnable),str(ParentTask))
            if tipoConsulta == 'Insert':
                sql = 'Insert into AAARegistroProyecto values(\''  + str(ProyectTask['id']) + '\',\'' + ProyectoArray[0] +'\',\'' + str(IdResposnable) + '\',\''+ str(Tarea) + '\',\'' + str(ParentTask) + '\',\'' + str(StartDate) + '\',\'' + str(DueDateBase) + '\',\'' + str(DueDate) + '\',\'' + str(ProyectTask['progress']) + '\',\'' + str(ProyectTask['completed']) + '\',\'EtiqFase\',\'EtiqDocumento\',\'EtiqDisciplina\',\'' + str(ProyectTask['description']) + '\',\'' + str(ProyectTask['estimated-minutes']) + '\')'
            else:
                sql = 'UPDATE [SAP].[dbo].[AAARegistroProyecto] SET [Tarea] = \'' + str(Tarea) + '\',[FechaIncio] = \'' + str(StartDate) + '\',[FechaFinalProgramada] = \'' + str(DueDateBase) + '\',[FehaFinalR] = \'' + str(DueDate) + '\',[Avance] = \'' + str(ProyectTask['progress']) + '\',[Completada] = \'' + str(ProyectTask['completed']) + '\',[EtqFase] = \'----\',[EtqDocumento] = \'---\',[EtqDiciplina] = \'---\',[Cantidad] = \'\',[TiempoEstimado] = \'\' WHERE [IdTareas]=\'' + str(ProyectTask['id']) + '\' and [IdProyecto]=\'' + ProyectoArray[0] + '\' and [IdUsuario]=\'' + str(IdResposnable) + '\' and [ListaTarea]=\'' + str(ParentTask) + '\''
            print (str(sql))
            ##sql_sentencia(sql)
        except ValueError:
            #print ('cadean' + '.-' + str(IdResposnable))
            AIdResposnable = str(IdResposnable).split(",")
            for idUser in AIdResposnable:
                #print ('algos' + '.-' + str(idUser))
                tipoConsulta = validate_up_in(str(ProyectTask['id']),ProyectoArray[0],str(idUser),str(ParentTask))
                if tipoConsulta == 'Insert':
                    sql = 'Insert into AAARegistroProyecto values(\''  + str(ProyectTask['id']) + '\',\'' + ProyectoArray[0] +'\',\'' + str(idUser) + '\',\''+ str(Tarea) + '\',\'' + str(ParentTask) + '\',\'' + str(StartDate) + '\',\'' + str(DueDateBase) + '\',\'' + str(DueDate) + '\',\'' + str(ProyectTask['progress']) + '\',\'' + str(ProyectTask['completed']) + '\',\'EtiqFase\',\'EtiqDocumento\',\'EtiqDisciplina\',\'' + str(ProyectTask['description']) + '\',\'' + str(ProyectTask['estimated-minutes']) + '\')'
                else:
                    #update
                    sql = 'UPDATE [SAP].[dbo].[AAARegistroProyecto] SET [Tarea] = \'' + str(Tarea) + '\',[FechaIncio] = \'' + str(StartDate) + '\',[FechaFinalProgramada] = \'' + str(DueDateBase) + '\',[FehaFinalR] = \'' + str(DueDate) + '\',[Avance] = \'' + str(ProyectTask['progress']) + '\',[Completada] = \'' + str(ProyectTask['completed']) + '\',[EtqFase] = \'----\',[EtqDocumento] = \'---\',[EtqDiciplina] = \'---\',[Cantidad] = \'\',[TiempoEstimado] = \'\' WHERE [IdTareas]=\'' + str(ProyectTask['id']) + '\' and [IdProyecto]=\'' + ProyectoArray[0] + '\' and [IdUsuario]=\'' + str(idUser) + '\' and [ListaTarea]=\'' + str(ParentTask) + '\''
                #sql_sentencia(sql)
                #print (str(sql))
#Esta funcione lee los cambio de la tabla AAARegistroDeTiemposDiarios para insertar en la tabla de sap

def ReordenarSAP():
    Regreso = 'Oka'
    #1 Recorremos todos los rgistros
    #Diccionario  inicializacion
    DirSAP = {}
    try:
        sql = 'SELECT [IdTarea],[IdUsuario],[IdProyecto],[Usuario],[Descripcion],[Tiempo],[IdTeam],CONVERT(VARCHAR,Fecha,103) As Fehca FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] Where [Fecha] >= \'01-01-2016\''
        con = pyodbc.connect(constr)
        cur = con.cursor()
        cur.execute(sql)
        for value in cur:
            IdTarea = value[0]
            IdUsuario = value[1]
            IdProyecto = value[2]
            Usuario = value[3]
            Descripcion = value[4]
            Tiempo = value[5]
            IdTeam = value[6]
            Fecha = value[7]
            #obtenemos el Id del usuario
            IdUserSap = IdUserSAP(str(IdUsuario))
            #Verificamos si el usuario tiene 100%
            Es100 = validar_100(str(IdUserSap),str(Fecha),str(Tiempo))
            if Es100 == 'No':
                TipoAccion = RegistroExistenteEnSap(str(IdTeam))
                if TipoAccion == 'Insert':
                    DirSAP['NumProyecto'] = IdProyecto
                    DirSAP['Dia'] = str(Fecha).replace('/','-')
                    DirSAP['Tarea'] = Descripcion
                    DirSAP['IdUsuarioTeam'] = IdUsuario
                    DirSAP['Horas'] = Tiempo
                    DirSAP['IdJson'] = IdTeam
                    sap_insert(DirSAP)
                    print ('Inserte en SAP')
                else:
                    DirSAP['NumProyecto'] = IdProyecto
                    DirSAP['Dia'] = str(Fecha).replace('/','-')
                    DirSAP['Tarea'] = Descripcion
                    DirSAP['IdUsuarioTeam'] = IdUsuario
                    DirSAP['Horas'] = Tiempo
                    DirSAP['IdJson'] = IdTeam
                    print(sap_update(DirSAP))
                    print ('Update en SAP')
            else:
                print('Dia con 100 Detctado' + 'Usuario:' + str(IdUsuario)  + 'Dia:' + str(Fecha) + 'NumProyecto:' + str(IdProyecto))
        con.commit()
        con.close()
    except ValueError:
        sentencia = '-------Error------:' + str(sql)
    return sql
