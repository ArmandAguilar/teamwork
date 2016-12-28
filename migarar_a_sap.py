#!user/bin/python
from tokens import *
from projects import *
from sap import *
from mssql import *
import pypyodbc as pyodbc
reload(sys)
sys.setdefaultencoding("utf-8")


#This funcion show if we need make update or insert
def filed_exist(IdTemaWork):
    Accion = 'No'
    sql_buscar = 'SELECT [Porcentaje] FROM [SAP].[dbo].[AATiemposDeProduccion] Where IdTemaWork = \'' + str(IdTemaWork) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
         Accion = 'Si'
    conn.commit()
    conn.close()

#This function to merge the
def migrate():
    valor = 0
    sql = 'SELECT [Nombre],[Apellidos],[NumProyecto],[NomProyecto],[Dia],[Tarea],[Porcentaje],[Producto],[IdUsuario],[Departamento],[Perfil],[Titulo],[Acronimo],[IdTemaWork] FROM  [SAP].[dbo].[AATiemposDeProduccionClon] WHERE [Dia] >= \'01-12-2016\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        Nombre = value[0]
        Apellidos = value[1]
        NumProyecto = value[2]
        NomProyecto = value[3]
        Dia = value[4]
        Tarea = value[5]
        Porcentaje = value[6]
        Producto = value[7]
        IdUsuario = value[8]
        Departamento = value[9]
        Perfil = value[10]
        Titulo = value[11]
        Acronimo = value[12]
        IdTemaWork = value[13]
        #Ask if existe somby field
        Exist = filed_exist(IdTemaWork)
        if Exist == 'Si':
            #here update the field
            sqlInsert = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccion] VALUES (\'Nombre\',\'Apellidos\',\'NumProyecto\',\'NomProyecto\',\'Dia\',\'Tarea\',\'Porcentaje\',\'Producto\',\'IdUsuario\',\'0\',\'Departamento\',\'Perfil\',\'Titulo\',\'Acronimo\',\'Si\',\'IdTeamWork\')'
            print (sqlInsert)
        else:
            #here insert the update
            sqlupdate = 'UPDATE [SAP].[dbo].[AATiemposDeProduccion] SET [Nombre] = \'' + str(Nombre) + '\' ,[Apellidos] = \'' + str(Apellidos) + '\',[NumProyecto] = \'' + str(NumProyecto) + '\',[NomProyecto] = \'' + str(NomProyecto) + '\',[Dia] = \'' + str(Dia) + '\',[Tarea] = \'' + str(Tarea) + '\',[Porcentaje] = \'' + str(Porcentaje) + '\',[Producto] = \'' + str(Producto) + '\',[IdUsuario] = \'' + str(IdUsuario) + '\',[Departamento] = \'' + str(Departamento) + '\',[Perfil] = \'' + str(Perfil) + '\',[Titulo] = \'' + str(Titulo) + '\',[Acronimo] = \'' + str(Acronimo) + '\' WHERE [IdTeamWork] = \'' + str(IdTeamWork) + '\''
            print (sqlupdate)
    conn.commit()
    conn.close()
    #return valor

migrate()
