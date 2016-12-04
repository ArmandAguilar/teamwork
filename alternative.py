#!user/bin/python
from tokens import *
from projects import *
from sap import *
from mssql import *
import pypyodbc as pyodbc
reload(sys)
sys.setdefaultencoding("utf-8")

#def validar_si_exiete(idUsuario,Dia,Procentaje):
#    Accion = 'No'
#    Fecha = str(Dia).replace('/','-')
#    sql_buscar = 'SELECT [Porcentaje] FROM [SAP].[dbo].[AATiemposDeProduccionClon] Where [IdUsuario] = \'' + str(idUsuario) + '\' and Dia = \'' + str(Fecha) + '\' and Porcentaje = \'' + str(Procentaje) + '\''
#    con = pyodbc.connect(constr)
#    cur = con.cursor()
#    cur.execute(sql_buscar)
#    for value in cur:
#         Accion = 'Si'
#    con.commit()
#    con.close()

#    return Accion


def Tiempos_TemaWork(IdProyecto):
    requestTiempo = urllib2.Request('https://forta.teamwork.com/projects/' + IdProyecto + '/time.json')
    requestTiempo.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseTiempo = urllib2.urlopen(requestTiempo)
    datajsonTiempo = json.loads(responseTiempo.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    PorcentajeF = 0.0
    Suma = 0
    for dataValor in datajsonTiempo['time-entries']:

        ProyectoArray = str(dataValor['project-name']).split(" ")
        #Fecha = str(dataValor['date']).split("T")
        DescripcionUser = str(dataValor['description'])
        DescripcionUser = str(DescripcionUser).replace('\'',' ')
        DescripcionUser = str(DescripcionUser).replace('"',' ')
        DescripcionUser = str(DescripcionUser).strip()

        #Metadatos de SAP
        DirMetaDataUser = metaDataUser(str(dataValor['person-id']))

        #Nombre del proyecto
        NomProyecto = ProyectName(str(ProyectoArray[0]))
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

        #Fecha
        for DateValue in dataValor['date']:
            Fecha = DateValue[1]

        sqlInsert = 'INSERT INTO [SAP].[dbo].[AATiemposDeProduccionClon] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(ProyectoArray[0]) + '\',\'' + str(NomProyecto) + '\',\'' + str(Fecha) + '\',\'' + str(DescripcionUser) + '\' ,\'' + str(PorcentajeF) + '\' ,\'' + str(ProductoF) + '\',\'' + str(DirMetaDataUser['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Perfil'])+ '\',\'Si\',\'' + str(dataValor['id']) + '\')'
        sqlUpdate = 'UPDATE [SAP].[dbo].[AATiemposDeProduccionClon] SET [Nombre] = \'' +  str(DirMetaDataUser['Nombre']) + '\',[Apellidos] = \'' + str(DirMetaDataUser['Apellidos']) + '\' [NumProyecto] = \'' + str(ProyectoArray[0]) + '\',[NomProyecto] = \'' + str(NomProyecto) + '\',[Dia] = \'' + str(Fecha) + '\',[Tarea] = \'' + str(DescripcionUser) + '\',[Porcentaje] = \'' + str(PorcentajeF) + '\',[Producto] = \'' + str(ProductoF) + '\',[IdUsuario] = \'' + str(DirMetaDataUser['IdUsuario']) + '\',[Departamento] = \'' + str(DirMetaDataUser['Departamento'])  + '\',[Perfil] = \'' + str(DirMetaDataUser['Perfil']) + '\',[Titulo] = \'.\',[Acronimo] = \'' + str(DirMetaDataUser['Acronimo']) + '\' WHERE IdTemaWork=\'' + str(dataValor['id']) + '\''
        print(Fecha)

for proyecto in projectos_id:

    Tiempos_TemaWork(proyecto)
