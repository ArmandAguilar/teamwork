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

#  i create a function by get the Tag of each task
def get_tag_task(idTask):
    NumProyecto = ''
    link = 'https://forta.teamwork.com/tasks/' + str(idTask)  + '.json'
    print (str(link))
    requestTag = urllib2.Request('https://forta.teamwork.com/tasks/' + str(idTask)  + '.json')
    requestTag.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseTag = urllib2.urlopen(requestTag)
    datajsonTag = json.loads(responseTag.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    ArraysTags = datajsonTag['todo-item']['tags']

    for itemsTodo in ArraysTags:
        NumProArray = str(itemsTodo['name']).split(" ")

    NumProyecto = str(NumProArray[0])

    return NumProyecto

#i cretae he function by insert in sap the records in the table

def Tiempos_TemaWork(IdProyecto):
    #Get Request of proyect time
    requestTiempo = urllib2.Request('https://forta.teamwork.com/projects/' + IdProyecto + '/time.json')
    requestTiempo.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseTiempo = urllib2.urlopen(requestTiempo)
    datajsonTiempo = json.loads(responseTiempo.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    #Set var
    PorcentajeF = 0.0
    Suma = 0
    Alerta = ''
    for dataValor in datajsonTiempo['time-entries']:

        #Get the metadata of user the MMSSQL
        DirMetaDataUser = metaDataUser(str(dataValor['person-id']))

        #Get Number and Name of proyect
        NumProyecto = get_tag_task(str(dataValor['todo-item-id']))
        NomProyecto = 'Aqui el proyecto'
        #Get Descripcion of work
        DescripcionUser = str(dataValor['description'])
        DescripcionUser = str(DescripcionUser).replace('\'',' ')
        DescripcionUser = str(DescripcionUser).replace('"',' ')
        DescripcionUser = str(DescripcionUser).strip()
        #Get Date
        Fecha = dataValor['dateUserPerspective']
        FechaJsonArrays = str(Fecha).split("T")
        #i make  the % and Time
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

        #sql = 'UPDATE [SAP].[dbo].[AATiemposDeProduccionClon] SET [Nombre] = \'' +  str(DirMetaDataUser['Nombre']) + '\',[Apellidos] = \'' + str(DirMetaDataUser['Apellidos']) + '\', [NumProyecto] = \'' + str(NumProyecto) + '\',[NomProyecto] = \'' + str(NomProyecto) + '\',[Dia] = \'' + str(FechaJsonArrays[0]) + '\',[Tarea] = \'' + str(DescripcionUser) + '\',[Porcentaje] = \'' + str(PorcentajeF) + '\',[Producto] = \'' + str(ProductoF) + '\',[IdUsuario] = \'' + str(DirMetaDataUser['IdUsuario']) + '\',[Departamento] = \'' + str(DirMetaDataUser['Departamento'])  + '\',[Perfil] = \'' + str(DirMetaDataUser['Perfil']) + '\',[Titulo] = \'.\',[Acronimo] = \'' + str(DirMetaDataUser['Acronimo']) + '\' WHERE IdTemaWork=\'' + str(dataValor['id']) + '\''
        sql = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccionClon] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(NumProyecto) + '\',\'' + str(NomProyecto) + '\',\'' + str(FechaJsonArrays[0]) + '\',\'' + str(DescripcionUser) + '\' ,\'' + str(PorcentajeF) + '\' ,\'' + str(ProductoF) + '\',\'' + str(DirMetaDataUser['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Perfil'])+ '\',\'Si\',\'' + str(dataValor['id']) + '\')'
        print (str(sql))
#Run the function by insert the dates
print('#################################### Insert Proyectos Internos ##########################')
Tiempos_TemaWork('323850')
print('#################################### End Proyectos Internos    ##########################')
