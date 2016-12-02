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
#funcion que registra  en AAARegistroDeTiemposDiarios
def TaksTiempoDiarios(idtask):
    #print('https://forta.teamwork.com/tasks/' + str(idtask) + '/time_entries.json')
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
        #Calculamos las Horas
        Horas = float(activities['hours'])
        Minutos = float(activities['minutes']) / 60
        HorasReal = Horas + Minutos
        DescripcionUser = str(activities['description'])
        DescripcionUser = str(DescripcionUser).replace('\'',' ')
        DescripcionUser = str(DescripcionUser).replace('"',' ')
        DescripcionUser = str(DescripcionUser).strip()
        if tipoConsultas == 'Insert':
            sql = 'Insert Into [SAP].[dbo].[AAARegistroDeTiemposDiarios] values(\'' + str(idtask) + '\',\'' + str(activities['person-id']) + '\',\'' + ProyectoArray[0] + '\',\''+ str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + '\',\'' + str(Descripcion) + '\',\'' + str(DescripcionUser) + '\',\'' + FechaJsonArrays[0] + '\',\'' + str(HorasReal) + '\',\'' + str(activities['id']) + '\',\'' + str(activities['project-id']) + '\')'
        else:
            UserName = str(activities['person-first-name']) + ' ' + str(activities['person-last-name'])
            sql = 'UPDATE [SAP].[dbo].[AAARegistroDeTiemposDiarios] SET [IdUsuario] = \'' + str(activities['person-id']) + '\',[IdProyecto] = \'' + ProyectoArray[0] + '\',[Usuario] = \'' + str(UserName)  + '\',[Descripcion] = \'' +  str(Descripcion)  + '\',DescipcionUsuario=\'' + str(DescripcionUser) + '\',[Fecha] = \'' + FechaJsonArrays[0] + '\',[Tiempo] = \'' + str(HorasReal) + '\' WHERE [IdTeam] = \'' + str(activities['id']) + '\''
        sql_sentencia(sql)

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
        #Eliminos los caratres peligroso para la consulta
        Tarea = ProyectTask['content']
        Tarea = str(Tarea).replace('\'',' ')
        Tarea = str(Tarea).replace('"',' ')
        Tarea = str(Tarea).strip()
        Descripcion = str(ProyectTask['description'])
        Descripcion = str(Descripcion).replace('\'',' ')
        Descripcion = str(Descripcion).replace('"',' ')
        Descripcion = str(Descripcion).strip()
        #print (str(Descripcion))
        #IdUsuario
        try:
            int(IdResposnable)
            tipoConsulta = validate_up_in(str(ProyectTask['id']),str(ProyectoArray[0]),str(IdResposnable),str(ParentTask))
            print(tipoConsulta)
            if tipoConsulta == 'Insert':
                sql = 'Insert into AAARegistroProyecto values(\''  + str(ProyectTask['id']) + '\',\'' + str(ProyectoArray[0]) +'\',\'' + str(IdResposnable) + '\',\''+ str(Tarea) + '\',\'' + str(ParentTask) + '\',\'' + str(StartDate) + '\',\'' + str(DueDateBase) + '\',\'' + str(DueDate) + '\',\'' + str(ProyectTask['progress']) + '\',\'' + str(ProyectTask['completed']) + '\',\'EtiqFase\',\'EtiqDocumento\',\'EtiqDisciplina\',\'' + str(ProyectTask['estimated-minutes']) + '\',\'' + str(Descripcion) + '\')'
            else:
                sql = 'UPDATE [SAP].[dbo].[AAARegistroProyecto] SET [Tarea] = \'' + str(Tarea) + '\',[FechaInicio] = \'' + str(StartDate) + '\',[FechaFinalProgramada] = \'' + str(DueDateBase) + '\',[FechaFinalR] = \'' + str(DueDate) + '\',[Avance] = \'' + str(ProyectTask['progress']) + '\',[Completada] = \'' + str(ProyectTask['completed']) + '\',[EtqFase] = \'----\',[EtqDocumento] = \'---\',[EtqDiciplina] = \'---\',[TiempoEstimado] = \'' + str(ProyectTask['estimated-minutes']) + '\',[Descripcion] = \'' + str(Descripcion) + '\' WHERE [IdTareas]=\'' + str(ProyectTask['id']) + '\' and [IdProyecto]=\'' + ProyectoArray[0] + '\' and [IdUsuario]=\'' + str(IdResposnable) + '\' and [ListaTarea]=\'' + str(ParentTask) + '\''
            print (str(sql))
            sql_sentencia(sql)
        except ValueError:
            #print ('cadean' + '.-' + str(IdResposnable))
            AIdResposnable = str(IdResposnable).split(",")
            for idUser in AIdResposnable:
                #print ('algos' + '.-' + str(idUser))
                tipoConsulta = validate_up_in(str(ProyectTask['id']),ProyectoArray[0],str(idUser),str(ParentTask))
                if tipoConsulta == 'Insert':
                    sql = 'Insert into AAARegistroProyecto values(\''  + str(ProyectTask['id']) + '\',\'' + str(ProyectoArray[0]) +'\',\'' + str(idUser) + '\',\''+ str(Tarea) + '\',\'' + str(ParentTask) + '\',\'' + str(StartDate) + '\',\'' + str(DueDateBase) + '\',\'' + str(DueDate) + '\',\'' + str(ProyectTask['progress']) + '\',\'' + str(ProyectTask['completed']) + '\',\'EtiqFase\',\'EtiqDocumento\',\'EtiqDisciplina\',\'' + str(ProyectTask['estimated-minutes']) + '\',\'' + str(Descripcion) + '\')'
                else:
                    #update
                    sql = 'UPDATE [SAP].[dbo].[AAARegistroProyecto] SET [Tarea] = \'' + str(Tarea) + '\',[FechaInicio] = \'' + str(StartDate) + '\',[FechaFinalProgramada] = \'' + str(DueDateBase) + '\',[FechaFinalR] = \'' + str(DueDate) + '\',[Avance] = \'' + str(ProyectTask['progress']) + '\',[Completada] = \'' + str(ProyectTask['completed']) + '\',[EtqFase] = \'----\',[EtqDocumento] = \'---\',[EtqDiciplina] = \'---\',[TiempoEstimado] = \'' + str(ProyectTask['estimated-minutes']) + '\',[Descripcion] = \'' + str(Descripcion) + '\' WHERE [IdTareas]=\'' + str(ProyectTask['id']) + '\' and [IdProyecto]=\'' + ProyectoArray[0] + '\' and [IdUsuario]=\'' + str(idUser) + '\' and [ListaTarea]=\'' + str(ParentTask) + '\''
                print (str(sql))
                sql_sentencia(sql)

#Esta funcion Borra los registros no activos en la tabla AAARegistroDeTiemposDiarios
def EliminarCambioEnTiemposDiarios():
    Regreso = 'Oka'
    SqlWhere = ''
    StWhere = ''
    requestProyectArchived = urllib2.Request('https://forta.teamwork.com/projects.json?status=ARCHIVED')
    requestProyectArchived.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseProyectArchived = urllib2.urlopen(requestProyectArchived)
    datajsonProyectArchived = json.loads(responseProyectArchived.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    for ProyectTaskArchivade  in datajsonProyectArchived['projects']:
        SqlWhere += '[IdProyectoTeam]<>\''  + str(ProyectTaskArchivade['id']) +  '\' and '

    if len(SqlWhere) > 0 :
        StWhere = ' and ' + SqlWhere[:-5]
    else:
        StWhere = ' '
    task_id = []
    k = 0
    sql = 'SELECT [IdTarea] FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] Where [Fecha] >= \'01-01-2016\' ' + str(StWhere)
    con = pyodbc.connect(constr)
    cur = con.cursor()
    cur.execute(sql)
    for value in cur:
        task_id.insert(k,str(value[0]))
    con.commit()
    con.close()
    for value in task_id:
        VerifcaEnTeamworkJson(str(value))
    return sql
#Elimina los datos no encontrados en team del mssql
def VerifcaEnTeamworkJson(idtask):
    Estado = 'Oka'
    requestActivitiesTask = urllib2.Request('https://forta.teamwork.com/tasks/' + idtask + '/time_entries.json')
    requestActivitiesTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseActivitiesTask = urllib2.urlopen(requestActivitiesTask)
    datajsonActivitiesTask = json.loads(responseActivitiesTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)

    if len(datajsonActivitiesTask['time-entries']) == 0:
        Estado = 'Borramos Actividad ' + str(idtask)
        sql = 'DELETE  FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] Where [IdProyectoTeam]=\'' + str(idtask) + '\''
        con = pyodbc.connect(constr)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()
    return Estado
#Esta funcione lee los cambio de la tabla AAARegistroDeTiemposDiarios para insertar en la tabla de sap
def ParaSAP():
    Regreso = 'Oka'
    #Quitamos los proyectos archivados
    SqlWhere = ''
    StWhere = ''
    DirSAP = {}
    requestProyectArchived = urllib2.Request('https://forta.teamwork.com/projects.json?status=ARCHIVED')
    requestProyectArchived.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseProyectArchived = urllib2.urlopen(requestProyectArchived)
    datajsonProyectArchived = json.loads(responseProyectArchived.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    for ProyectTaskArchivade  in datajsonProyectArchived['projects']:
        SqlWhere += '[IdProyectoTeam]<>\''  + str(ProyectTaskArchivade['id']) +  '\' and '

    if len(SqlWhere) > 0 :
        StWhere = ' and ' + SqlWhere[:-5]
    else:
        StWhere = ' '
    #1 Recorremos todos los rgistros
    #Diccionario  inicializacion
    try:
        sql = 'SELECT [IdTarea],[IdUsuario],[IdProyecto],[Usuario],[Descripcion],[Tiempo],[IdTeam],CONVERT(VARCHAR,Fecha,103) As Fehca FROM [SAP].[dbo].[AAARegistroDeTiemposDiarios] Where [Fecha] >= \'01-01-2016\' ' + str(StWhere)
        print (sql)
        ssuma = 0
        con = pyodbc.connect(constr)
        cur = con.cursor()
        cur.execute(sql)
        for value in cur:
            IdTarea = str(value[0])
            IdUsuario = str(value[1])
            IdProyecto = str(value[2])
            Usuario = str(value[3])
            Descripcion = str(value[4])
            Tiempo = str(value[5])
            IdTeam = str(value[6])
            Fecha = str(value[7])
            #obtenemos el Id del usuario
            IdUserSap = IdUserSAP(str(IdUsuario))
            #Verificamos si el usuario tiene 100%23
            Es100 = validar_100(str(IdUserSap),str(Fecha),str(Tiempo))
            valor =  str(ssuma) + '_' + str(Es100) + ' IdSAP:' + str(IdUserSap) + ' Tiempo:' + str(Tiempo) + 'Fecha:' + str(Fecha)
            if Es100 == 'No':
                print(Es100)
                TipoAccion = RegistroExistenteEnSap(str(IdTeam))
                #print(TipoAccion)
                if TipoAccion == 'Insert':
                     ssuma = ssuma + 1
                     DirSAP['NumProyecto'] = str(IdProyecto)
                     DirSAP['Dia'] = str(Fecha).replace('/','-')
                     DirSAP['Tarea'] = str(Descripcion)
                     DirSAP['IdUsuarioTeam'] = str(IdUsuario)
                     DirSAP['Horas'] = str(Tiempo)
                     DirSAP['IdJson'] = str(IdTeam)
                     sql = sap_insert(DirSAP)
                else:
                    DirSAP['NumProyecto'] = str(IdProyecto)
                    DirSAP['Dia'] = str(Fecha).replace('/','-')
                    DirSAP['Tarea'] = str(Descripcion)
                    DirSAP['IdUsuarioTeam'] = str(IdUsuario)
                    DirSAP['Horas'] = str(Tiempo)
                    DirSAP['IdJson'] = str(IdTeam)
                    sql = sap_update(DirSAP)
            else:
                print('Dia con 100 Detctado' + 'Usuario:' + str(IdUsuario)  + 'Dia:' + str(Fecha) + 'NumProyecto:' + str(IdProyecto))
        con.commit()
        con.close()
    except ValueError:
        sentencia = '-------Error------:' + str(sql)
    return sql
