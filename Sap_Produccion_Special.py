#!user/bin/python
from tokens import *
from projects import *
from sap import *
from mssql import *
import pypyodbc as pyodbc
reload(sys)
sys.setdefaultencoding("utf-8")
#Here we create a new function this fucntion
#set a json with  all avtive user and get your cost them return a json
#{ Id:UserId,Costo:$1 }
def costPersonal():
    SalaryJson = ''
    SalaryJson = '{"Person":['
    Sql = 'SELECT [IdRecurso],[CostoUnitario] FROM [SAP].[dbo].[RecursosCostos] order by [IdRecurso] asc'
    con = pyodbc.connect(constr)
    cur = con.cursor()
    cur.execute(Sql)
    for value in cur:
            SalaryJson += '{"IdUser":' +  str(value[0])  + ',"Cost":' + str(value[1]) +  '},' + '\n'

    con.commit()
    con.close()
    temp = len(SalaryJson)
    SalaryJson = SalaryJson[:temp - 2]
    SalaryJson += ']}'
    data = json.loads(SalaryJson)
    return data

def seekCostobyUser(data,IdUsuario):
    rCosto = 0.0
    for vCosto in data['Person']:
        if IdUsuario == vCosto['IdUser']:
            rCosto = vCosto['Cost']
    return rCosto

def getHistoricalCosto(IdTemaWork):
    sql = 'SELECT [Costo] FROM [SAP].[dbo].[AATiemposDeProduccionClon] Where [IdTemaWork] = \'' + str(IdTemaWork) + '\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        CostoUnitario = value[0]
    conn.commit()
    conn.close()
    return CostoUnitario

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
    if PorcentajeTotal  > 100.0:
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
    #this section run a page1 ...n
    Paginado = 1
    Limite = True
    while Limite == True:
        #
        requestTiempo = urllib2.Request('https://forta.teamwork.com/projects/' + str(IdProyecto) + '/time.json?page=' + str(Paginado))
        requestTiempo.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
        responseTiempo = urllib2.urlopen(requestTiempo)
        datajsonTiempo = json.loads(responseTiempo.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
        PorcentajeF = 0.0
        Suma = 0
        Alerta = ''
        #Ask if json have data
        Data = len(datajsonTiempo['time-entries'])
        if Data == 0:
            # set Limit to false
            Limite = False
        else:
            # i process data
            print ('================> Pagina: ' + str(Paginado) + 'Proyecto Id: ' + str(IdProyecto) + ' <================')
            for dataValor in datajsonTiempo['time-entries']:
                ProyectoArray = str(dataValor['project-name']).split(" ")
                DescripcionUser = str(dataValor['description'])
                DescripcionUser = str(DescripcionUser).replace('\'',' ')
                DescripcionUser = str(DescripcionUser).replace('"',' ')
                DescripcionUser = str(DescripcionUser).strip()
                #Cut the script by AATiemposDeProduccion
                DescripcionLimit = str(DescripcionUser[:200])

                #SAP MetaData
                DirMetaDataUser = metaDataUser(str(dataValor['person-id']))

                #Proyect's Name
                NomProyecto = ProyectName(str(ProyectoArray[0]))
                #Here we to calculate tehe cost and percentage
                Horas = float(dataValor['hours'])
                Minutos = float(dataValor['minutes']) / 60
                HorasReal = Horas + Minutos
                if HorasReal > 9:
                    Porcentaje = (HorasReal/HorasReal) * 100
                else:
                    Porcentaje = (HorasReal/9.0) * 100
                #Id Home
                IdTareaReal = str(dataValor['todo-item-id'])
                #Activitiy Cost
                Costo = CostoUnitarioRecursos(DirMetaDataUser['IdUsuario'])
                PorcentajeF = float("{0:.2f}".format(Porcentaje))
                Producto = (PorcentajeF * float(Costo)) / 100
                ProductoF = float("{0:.2f}".format(Producto))
                #Date Format
                Fecha = dataValor['dateUserPerspective']
                FechaJsonArrays = str(Fecha).split("T")
                #Ask if existe any fields
                Existe = validar_si_exiete(dataValor['id'])
                if DirMetaDataUser['Nombre'] == 'V':
                    vPass = 0
                else:
                    #Here seek if exist tags
                    existTag = 0
                    TagName = 0
                    NoProyecto = ProyectoArray[0]
                    NomProyecto = NomProyecto
                    try:
                        existTag = len(dataValor['tags'])
                        if existTag > 0:
                            TagName = dataValor['tags'][0]['name']
                    except KeyError:
                        print 'There are problems here'

                    if str(TagName) == '0':
                        #Some code here
                        NoProyecto = ProyectoArray[0]
                        NomProyecto = NomProyecto
                    else:
                        if str(TagName) == '2059':
                            #some code Here
                            NoProyecto = 2059
                            NomProyecto = 'PI. Hotel Via Montejo'
                        elif str(TagName) == '2058':
                            #some code Here
                            NoProyecto = 2058
                            NomProyecto = 'PI. Edif. Residencial Via Montejo'
                        elif str(TagName) == '2052':
                            #some code here
                            NoProyecto = 2052
                            NomProyecto = 'Proy Torre 3 C. Towers, Merida'

                    if Existe == 'Si':
                        #Here we calculate the cost with the cost historical
                        Costo = getHistoricalCosto(dataValor['id'])
                        Producto = (PorcentajeF * float(Costo)) / 100
                        ProductoF = float("{0:.2f}".format(Producto))
                        if existTag == 0:
                            sql ='UPDATE [SAP].[dbo].[AATiemposDeProduccionClon] SET [Nombre] = \'' +  str(DirMetaDataUser['Nombre']) + '\',[Apellidos] = \'' + str(DirMetaDataUser['Apellidos']) + '\',[Dia] = \'' + str(FechaJsonArrays[0]) + '\',[Tarea] = \'' + str(DescripcionUser) + '\',[Porcentaje] = \'' + str(PorcentajeF) + '\',[Producto] = \'' + str(ProductoF) + '\',[IdUsuario] = \'' + str(DirMetaDataUser['IdUsuario']) + '\',[Departamento] = \'' + str(DirMetaDataUser['Departamento'])  + '\',[Perfil] = \'' + str(DirMetaDataUser['Perfil']) + '\',[Titulo] = \'.\',[Acronimo] = \'' + str(DirMetaDataUser['Acronimo']) + '\',[HoraReal]=\'' + str(HorasReal) + '\',[IdTarea]=\'' + str(IdTareaReal) + '\',[NumProyecto]=\'' + str(NoProyecto) + '\' ,[NomProyecto]=\'' + str(NomProyecto) + '\' WHERE IdTemaWork=\'' + str(dataValor['id']) + '\''
                        else:
                            sql ='UPDATE [SAP].[dbo].[AATiemposDeProduccionClon] SET [Nombre] = \'' +  str(DirMetaDataUser['Nombre']) + '\',[Apellidos] = \'' + str(DirMetaDataUser['Apellidos']) + '\',[Dia] = \'' + str(FechaJsonArrays[0]) + '\',[Tarea] = \'' + str(DescripcionUser) + '\',[Porcentaje] = \'' + str(PorcentajeF) + '\',[Producto] = \'' + str(ProductoF) + '\',[IdUsuario] = \'' + str(DirMetaDataUser['IdUsuario']) + '\',[Departamento] = \'' + str(DirMetaDataUser['Departamento'])  + '\',[Perfil] = \'' + str(DirMetaDataUser['Perfil']) + '\',[Titulo] = \'.\',[Acronimo] = \'' + str(DirMetaDataUser['Acronimo']) + '\',[HoraReal]=\'' + str(HorasReal) + '\',[IdTarea]=\'' + str(IdTareaReal) + '\',[NumProyecto]=\'' + str(NoProyecto) + '\' ,[NomProyecto]=\'' + str(NomProyecto) + '\' WHERE IdTemaWork=\'' + str(dataValor['id']) + '\''
                        procesar_sap_clon(sql)
                        print (sql)
                    else:
                        EsInsertable = validar_dia_completo(DirMetaDataUser['IdUsuario'],FechaJsonArrays[0],PorcentajeF)
                        if EsInsertable == 'Si':
                            sql ='INSERT INTO [SAP].[dbo].[AATiemposDeProduccionClon] VALUES (\'' + str(DirMetaDataUser['Nombre']) + '\',\'' + str(DirMetaDataUser['Apellidos']) + '\',\'' + str(NoProyecto) + '\',\'' + str(NomProyecto) + '\',\'' + str(FechaJsonArrays[0]) + '\',\'' + str(DescripcionUser) + '\' ,\'' + str(PorcentajeF) + '\' ,\'' + str(ProductoF) + '\',\'' + str(DirMetaDataUser['IdUsuario']) + '\',\'0\',\'' + str(DirMetaDataUser['Departamento']) + '\',\'' + str(DirMetaDataUser['Perfil']) + '\',\'.\',\'' + str(DirMetaDataUser['Acronimo'])+ '\',\'Si\',\'' + str(dataValor['id']) + '\',\'' + str(HorasReal) + '\',\'' + str(IdTareaReal) + '\',\'' + str(Costo) + '\')'
                            procesar_sap_clon(sql)
                            print (sql)
                        else:
                            alerta = 'Id: ' + str(dataValor['id']) + ' Proyecto: ' + str(dataValor['project-id']) + '-' + str(dataValor['project-name']) + ' Usuario (' + str(DirMetaDataUser['IdUsuario']) + ') : ' + str(DirMetaDataUser['Nombre']) + ' ' + str(DirMetaDataUser['Apellidos']) + ' Dia:' +  str(FechaJsonArrays[0]) + ' Horas :' +  str(HorasReal) + ' Porcentaje: ' + str(PorcentajeF)
                            sqlDeleteClon = 'DELETE FROM [SAP].[dbo].[AATiemposDeProduccionClon] WHERE IdUsuario = \'' + str(DirMetaDataUser['IdUsuario']) + '\' and Dia = \'' + str(FechaJsonArrays[0]) + '\''
                            sqlDelete = 'DELETE FROM [SAP].[dbo].[AATiemposDeProduccion] WHERE IdUsuario = \'' + str(DirMetaDataUser['IdUsuario']) + '\' and Dia = \'' + str(FechaJsonArrays[0]) + '\''
                            print(alerta)
                            #procesar_sap_clon(sqlDeleteClon)
                            #procesar_sap_clon(sqlDelete)
        Paginado += 1
print('#################################### Insert 2050 = 446552  ##########################')
Tiempos_TemaWork(446552)
print('#################################### End Porduccion ##########################')
print('--------------------------------------------------------------------------------------------------')
print('#################################### Insert 2061 = 456496 ##########################')
Tiempos_TemaWork(456496)
print('#################################### End Porduccion ##########################')
