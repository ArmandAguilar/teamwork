#!user/bin/python
from tokens import *
from projects import *
from sap import *
from mssql import *
import pypyodbc as pyodbc
import urllib2, base64
import json
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def validar_si_exiete(IdTemaWork):
    Accion = 'No'
    sql_buscar = 'SELECT [Porcentaje] FROM [SAP].[dbo].[AATiemposDeProduccionClon] Where IdTemaWork = \'' + str(IdTemaWork) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
         Accion = 'Si'
    conn.commit()
    conn.close()

    return Accion
def validar_dia_completo(IdUsuario,Dia,Porcentajes):
    OtroPorciento = float(Porcentajes)
    Fecha = str(Dia).replace('/','-')
    Permitir = 'Si'
    Porcentaje = 0.0
    sql_buscar = 'SELECT [Porcentaje] FROM [SAP].[dbo].[AATiemposDeProduccionClon] Where [IdUsuario] = \'' + str(IdUsuario) + '\' and Dia = \'' + str(Fecha) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql_buscar)
    for value in cur:
         Porcentaje = Porcentaje + float(value[0])
    conn.commit()
    conn.close()
    PorcentajeTotal = Porcentaje + OtroPorciento
    if PorcentajeTotal  > 100:
        Permitir = 'No'
    return Permitir
def procesar_sap_clon(sql):
    valor = 'Procesando..'
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    return valor
def Tiempos_TemaWork(IdProyecto):
    Link = 'https://forta.teamwork.com/projects/' + IdProyecto + '/time.json'
    requestTiempo = urllib2.Request('https://forta.teamwork.com/projects/' + IdProyecto + '/time.json')
    requestTiempo.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseTiempo = urllib2.urlopen(requestTiempo)
    datajsonTiempo = json.loads(responseTiempo.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    PorcentajeF = 0.0
    Suma = 0
    Alerta = ''
    for dataValor in datajsonTiempo['time-entries']:
        if len(dataValor['todo-list-name']) == 0:
            Passv = 0
        else:
            ProyectoArray = str(dataValor['todo-list-name']).split(" ")
            #Fecha = str(dataValor['date']).split("T")
            DescripcionUser = str(dataValor['description'])
            DescripcionUser = str(DescripcionUser).replace('\'',' ')
            DescripcionUser = str(DescripcionUser).replace('"',' ')
            DescripcionUser = str(DescripcionUser).strip()

            #Metadatos de SAP
            DirMetaDataUser = metaDataUser(str(dataValor['person-id']))

            #Nombre del proyecto
            NumProyecto = str(ProyectoArray[0])
            NomProyecto = str(ProyectoArray[1])
            #Calculamos el Porcenta y el Costo
            Horas = float(dataValor['hours'])
            Minutos = float(dataValor['minutes']) / 60
            HorasReal = Horas + Minutos
            if HorasReal > 9:
                Porcentaje = (HorasReal/HorasReal) * 100
            else:
                Porcentaje = (HorasReal/9.0) * 100
                #Costo de Actividad
                Costo = CostoUnitarioRecursos(DirMetaDataUser['IdUsuario'])
                PorcentajeF = float("{0:.2f}".format(Porcentaje))
                Producto = (PorcentajeF * float(Costo)) / 100
                ProductoF = float("{0:.2f}".format(Producto))
                #Formateando Fecha
                Fecha = dataValor['dateUserPerspective']
                FechaJsonArrays = str(Fecha).split("T")
                #Verifcamos si existe le registro
                Existe = validar_si_exiete(dataValor['id'])
                if DirMetaDataUser['Nombre'] == 'V':
                        vPass = 0
                else:
                    if Existe == 'Si':
                        sql = 'UPDATE [SAP].[dbo].[AATiemposDeProduccionClon] SET [Nombre] = \'' +  str(DirMetaDataUser['Nombre']) + '\',[Apellidos] = \'' + str(DirMetaDataUser['Apellidos']) + '\', [NumProyecto] = \'' + str(NumProyecto) + '\',[NomProyecto] = \'' + str(NomProyecto) + '\',[Dia] = \'' + str(FechaJsonArrays[0]) + '\',[Tarea] = \'' + str(DescripcionUser) + '\',[Porcentaje] = \'' + str(PorcentajeF) + '\',[Producto] = \'' + str(ProductoF) + '\',[IdUsuario] = \'' + str(DirMetaDataUser['IdUsuario']) + '\',[Departamento] = \'' + str(DirMetaDataUser['Departamento'])  + '\',[Perfil] = \'' + str(DirMetaDataUser['Perfil']) + '\',[Titulo] = \'.\',[Acronimo] = \'' + str(DirMetaDataUser['Acronimo']) + '\' WHERE IdTemaWork=\'' + str(dataValor['id']) + '\''
                        procesar_sap_clon(sql)
                        print (sql)
                    else:

                        g
                        EsInsertable = validar_dia_completo(DirMetaDataUser['IdUsuario'],FechaJsonArrays[0],PorcentajeF)
                        print(str(EsInsertable) + ' ' + str(DirMetaDataUser['IdUsuario']) + ' ' + str(FechaJsonArrays[0]) + ' '  + str(PorcentajeF))
                        if str(EsInsertable) == 'Si':
                            sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccionClon] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(NumProyecto) + '\',\'' + str(NomProyecto) + '\',\'' + str(FechaJsonArrays[0]) + '\',\'' + str(DescripcionUser) + '\' ,\'' + str(PorcentajeF) + '\' ,\'' + str(ProductoF) + '\',\'' + str(DirMetaDataUser['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Acronimo'])+ '\',\'Si\',\'' + str(dataValor['id']) + '\')'
                            #sqlSAP = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccion] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(NumProyecto) + '\',\'' + str(NomProyecto) + '\',\'' + str(FechaJsonArrays[0]) + '\',\'' + str(DescripcionUser) + '\' ,\'' + str(PorcentajeF) + '\' ,\'' + str(ProductoF) + '\',\'' + str(DirMetaDataUser['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Acronimo'])+ '\',\'Si\',\'' + str(dataValor['id']) + '\')'
                            #procesar_sap_clon(sqlSAP)
                            procesar_sap_clon(sql)
                            print(sql)
                        else:
                            alerta = 'Proyecto: ' + str(dataValor['project-id']) + '-' + str(dataValor['project-name']) + ' Usuario (' + str(DirMetaDataUser['IdUsuario']) + ') : ' + str(DirMetaDataUser['Nombre']) + ' ' + str(DirMetaDataUser['Apellidos']) + ' Dia:' +  str(FechaJsonArrays[0]) + ' Horas :' +  str(HorasReal) + ' Porcentaje: ' + str(PorcentajeF)
                            print(alerta)
#Costo Administrativo 317730
print('#################################### Insert Costo Administrativo ##########################')
Tiempos_TemaWork('317730')
print('#################################### End Costo Administrativo    ##########################')
