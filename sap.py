#!user/bin/python
from tokens import *
from mssql import *
from validate import *
import pypyodbc as pyodbc

def IdUserSAP(idUserTeamWork):
    dataIdUsuario = 0
    sql = 'SELECT [Id] FROM [Northwind].[dbo].[Usuarios] Where [IdTemWork] =\'' + str(idUserTeamWork) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        dataIdUsuario = value[0]
    conn.commit()
    conn.close()
    return dataIdUsuario
def validar_100(idUsuario,Dia,Tiempo):
    OtroPorciento = (float(Tiempo)/9.0) * 100
    Fecha = str(Dia).replace('/','-')
    Accion = 'No'
    Porcentaje = 0.0
    sql_buscar = 'SELECT [Porcentaje] FROM [SAP].[dbo].[AATiemposDeProduccionClon] Where [IdUsuario] = \'' + str(idUsuario) + '\' and Dia = \'' + str(Fecha) + '\''
    con = pyodbc.connect(constr)
    cur = con.cursor()
    cur.execute(sql_buscar)
    for value in cur:
         Porcentaje = Porcentaje + float(value[0])
    con.commit()
    con.close()
    PorcentajeTotal = Porcentaje + OtroPorciento
    if PorcentajeTotal  > 100:
        Accion = 'Si'
    val = 'Accion :' + str(Accion) + 'Usuario :' + str(idUsuario) + 'Dia:' + str(Fecha) + 'Porcentaje:' + str(OtroPorciento)
    return Accion
def metaDataUser(idUserTeamWork):
    dataDir = {}
    dataDir['IdUsuario'] = 'V'
    dataDir['Nombre'] = 'V'
    dataDir['Apellidos'] = 'V'
    dataDir['Departamento'] = 'V'
    dataDir['Perfil'] = 'V'
    dataDir['Acronimo'] = 'V'
    sql = 'SELECT [Id],[Nombre],[Apellidos],[Departamento],[Perfil],[Acronimo] FROM [Northwind].[dbo].[Usuarios] Where [IdTemWork] =\'' + str(idUserTeamWork) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        dataDir['IdUsuario'] = 12
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

def CostoUnitarioRecursos(IdUsuario):
    sql = 'SELECT [CostoUnitario] FROM [SAP].[dbo].[RecursosCostos] Where [IdRecurso] = \'' + str(IdUsuario) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        CostoUnitario = value[0]
    conn.commit()
    conn.close()
    return CostoUnitario
def RegistroExistenteEnSap(IdTeamWok):
    Accion = 'Insert'
    sql = 'SELECT [Id] FROM [SAP].[dbo].[AATiemposDeProduccionClon] WHERE [IdTemaWork] = \'' + str(IdTeamWok) + '\''
    con = pyodbc.connect(constr)
    cur = con.cursor()
    cur.execute(sql)
    for value in cur:
        Accion = "Update"
    con.commit()
    con.close()
    return Accion
def sap_insert(DirTiempoDiario):
    #DirSAP['NumProyecto'] = ProyectoArray[0]
    #DirSAP['Dia'] = FechaJsonArrays[0]
    #DirSAP['Tarea'] = str(Descripcion)
    #DirSAP['IdUsuarioTeam'] = str(activities['person-id'])
    Proy = ProyectName(str(DirTiempoDiario['NumProyecto']))
    DirMetaDataUser = metaDataUser(str(DirTiempoDiario['IdUsuarioTeam']))
    Costo = CostoUnitarioRecursos(str(DirMetaDataUser['IdUsuario']))
    HorasMarcadas = float(DirTiempoDiario['Horas'])
    if HorasMarcadas > 9:
        Porcentaje = (float(DirTiempoDiario['Horas'])/HorasMarcadas) * 100
    else:
        Porcentaje = (float(DirTiempoDiario['Horas'])/9.0) * 100

    PorcentajeF = float("{0:.2f}".format(Porcentaje))
    Producto = (PorcentajeF * float(Costo)) / 100
    ProductoF = float("{0:.2f}".format(Producto))
    #sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccionClon] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(DirTiempoDiario['NumProyecto']) + '\',\'' + str(Proy) + '\',CAST(\'' + str(DirTiempoDiario['Dia']) + '\' as SMALLDATETIME)' + ',\'' + str(DirTiempoDiario['Tarea']) + '\',\'' + str(PorcentajeF) + '\',\'' + str(ProductoF) + '\',\'' + str(DirMetaDataUser['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Acronimo']) + '\',\'Si\',\'' + str(DirTiempoDiario['IdJson']) + '\')'
    sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccionClon] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(DirTiempoDiario['NumProyecto']) + '\',\'' + str(Proy) + '\',\'' + str(DirTiempoDiario['Dia']) + '\',\'' + str(DirTiempoDiario['Tarea']) + '\',\'' + str(PorcentajeF) + '\',\'' + str(ProductoF) + '\',\'' + str(DirMetaDataUser['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Acronimo']) + '\',\'Si\',\'' + str(DirTiempoDiario['IdJson']) + '\')'
    con = pyodbc.connect(constr)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    return sql
def sap_update(DirTiempoDiario):
    #DirSAP['NumProyecto'] = ProyectoArray[0]
    #DirSAP['Dia'] = FechaJsonArrays[0]
    #DirSAP['Tarea'] = str(Descripcion)
    #DirSAP['IdUsuarioTeam'] = str(activities['person-id'])
    Proy = ProyectName(str(DirTiempoDiario['NumProyecto']))
    DirMetaDataUser = metaDataUser(str(DirTiempoDiario['IdUsuarioTeam']))
    Costo = CostoUnitarioRecursos(str(DirMetaDataUser['IdUsuario']))
    HorasMarcadas = int(DirTiempoDiario['Horas'])
    if HorasMarcadas > 9:
        Porcentaje = (int(DirTiempoDiario['Horas'])/HorasMarcadas) * 100
    else:
        Porcentaje = (float(DirTiempoDiario['Horas'])/9.0) * 100
    PorcentajeF = float("{0:.2f}".format(Porcentaje))
    Producto = (PorcentajeF * float(Costo)) / 100
    ProductoF = float("{0:.2f}".format(Producto))
    sql = 'UPDATE [SAP].[dbo].[AATiemposDeProduccionClon] SET [Nombre] = \'' + str(DirMetaDataUser['Nombre']) + '\',[Apellidos] = \''+ str(DirMetaDataUser['Apellidos']) +'\',[NumProyecto] = \'' + str(DirTiempoDiario['NumProyecto'])  + '\',[NomProyecto] = \'' + str(Proy)+ '\',[Dia] = \'' + str(DirTiempoDiario['Dia']) + '\',[Tarea] = \'' + str(DirTiempoDiario['Tarea']) + '\',[Porcentaje] = \'' + str(PorcentajeF) + '\',[Producto] = \'' + str(ProductoF) + '\',[IdUsuario] = \'' + str(DirMetaDataUser['IdUsuario']) + '\',[IdInternet] = \'0\',[Departamento] = \'' + str(DirMetaDataUser['Departamento']) + '\',[Perfil] = \''+  str(DirMetaDataUser['Perfil']) + '\',[Titulo] = \'.\',[Acronimo] = \'' + str(DirMetaDataUser['Acronimo']) + '\',[Programado] = \'Si\' WHERE [IdTemaWork] = \'' + str(DirTiempoDiario['IdJson']) + '\''
    con = pyodbc.connect(constr)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()
    return sql
