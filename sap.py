#!user/bin/python
from tokens import *
from mssql import *

def metaDataUser(idUserTeamWork):
    dataDir = {}
    sql = 'SELECT [Id],[Nombre],[Apellidos],[Departamento],[Perfil],[Acronimo] FROM [Northwind].[dbo].[Usuarios] Where [TeamWok] =\'' + str(idUserTeamWork) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
        dataDir['IdUsuario'] = value['Id']
        dataDir['Nombre'] = value['Nombre']
        dataDir['Apellidos'] = value['Apellidos']
        dataDir['Departamento'] = value['Departamento']
        dataDir['Perfil'] = value['Perfil']
        dataDir['Acronimo'] = value['Acronimo']
    conn.commit()
    conn.close()
    return dataDir

def ProyectName(IdProyecto):
    sql = 'SELECT [Proyecto] FROM [SAP].[dbo].[Presupuestos] Where [NoProyecto] =\'' + str(IdProyecto) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
        NombreProyecto = value['Proyecto']
    conn.commit()
    conn.close()
    return NombreProyecto

def sap_insert(DirTiempoDiario):
    #DirSAP['NumProyecto'] = ProyectoArray[0]
    #DirSAP['Dia'] = FechaJsonArrays[0]
    #DirSAP['Tarea'] = str(Descripcion)
    #DirSAP['IdUsuarioTeam'] = str(activities['person-id'])
    for TiempoDiario in DirTiempoDiario:
        #pass
        #funcion que completa los metadatos del usuario
        DirMetaDataUser = metaDataUser(TiempoDiario['IdUsuarioTeam'])
        #Funcion qu busca el nombre del proyecto registrado en la base de datos MSSQL
        Proy = ProyectName()
        #Consulta para instera en la tabla AATiemposDeProduccion
        sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccion] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(TiempoDiario['NumProyecto']) + '\',\'NomProyecto\',\'' + str(TiempoDiario['Dia']) + '\',\'' + str(TiempoDiario['Tarea']) + '\',\'Porcentaje\',\'Producto\',\'' + str(dataDir['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Acronimo']) + '\',\'Si\')'

    return sql
