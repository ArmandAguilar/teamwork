#!user/bin/python
from tokens import *
from mssql import *

def metaDataUser(idUserTeamWork):
    dataDir = {}
    sql = 'SELECT [Id],[Nombre],[Apellidos],[Departamento],[Perfil],[Acronimo] FROM [Northwind].[dbo].[Usuarios] Where [IdTeamWok] =\'' + str(idUserTeamWork) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        dataDir['IdUsuario'] = value[0]
        dataDir['Nombre'] = value[1]
        dataDir['Apellidos'] = value[2]
        dataDir['Departamento'] = value[3]
        dataDir['Perfil'] = value[4]
        dataDir['Acronimo'] = value[5]
    conn.commit()
    conn.close()
    return dataDir

def ProyectName(IdProyecto):
    sql = 'SELECT [Proyecto] FROM [SAP].[dbo].[Presupuestos] Where [NoProyecto] =\'' + str(IdProyecto) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        NombreProyecto = value[0]
    conn.commit()
    conn.close()
    return NombreProyecto

def sap_insert(DirTiempoDiario):
    #DirSAP['NumProyecto'] = ProyectoArray[0]
    #DirSAP['Dia'] = FechaJsonArrays[0]
    #DirSAP['Tarea'] = str(Descripcion)
    #DirSAP['IdUsuarioTeam'] = str(activities['person-id'])
    Proy = ProyectName(str(DirTiempoDiario['NumProyecto']))
    DirMetaDataUser = metaDataUser(str(DirTiempoDiario['IdUsuarioTeam']))
    sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccion] VALUES (\'' + str(DirMetaDataUser[0]) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(TiempoDiario['NumProyecto']) + '\',\'NomProyecto\',\'' + str(TiempoDiario['Dia']) + '\',\'' + str(TiempoDiario['Tarea']) + '\',\'Porcentaje\',\'Producto\',\'' + str(dataDir['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Acronimo']) + '\',\'Si\')'
    #for TiempoDiario in DirTiempoDiario:
        #pass
        #funcion que completa los metadatos del usuario
        #
        #Funcion qu busca el nombre del proyecto registrado en la base de datos MSSQL
        #Proy = ProyectName(TiempoDiario['NumProyecto'])

        #Consulta para instera en la tabla AATiemposDeProduccion
        #sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccion] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(TiempoDiario['NumProyecto']) + '\',\'NomProyecto\',\'' + str(TiempoDiario['Dia']) + '\',\'' + str(TiempoDiario['Tarea']) + '\',\'Porcentaje\',\'Producto\',\'' + str(dataDir['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Acronimo']) + '\',\'Si\')'

    return sql
