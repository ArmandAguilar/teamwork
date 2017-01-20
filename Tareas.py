#!user/bin/python
from tokens import *
from projects import *
from sap import *
from mssql import *
import pypyodbc as pyodbc
from datetime import datetime,time
reload(sys)
sys.setdefaultencoding("utf-8")

def procesar_mssql(sql):
    valor = 'Procesando..'
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()
    return valor
def ExistenteTask(IdTeamWok):
    Accion = 'Insert'
    sql = 'SELECT [Id] FROM [SAP].[dbo].[AATareasTeamWork] WHERE [IdTeamWork] = \'' + str(IdTeamWok) + '\''
    con = pyodbc.connect(constr)
    cur = con.cursor()
    cur.execute(sql)
    for value in cur:
        Accion = "Update"
    con.commit()
    con.close()
    return Accion
#This fucntion get all task whith status Close */
def allTaskCompleted(IdProyecto):
    #pass
    #this section run a page1 ...n
    Paginado = 1
    li = 0
    Limite = True
    while Limite == True:
        #
        requestTask = urllib2.Request('https://forta.teamwork.com/projects/' + IdProyecto + '/tasks.json?filter=completed&page=' + str(Paginado))
        requestTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
        responseTask = urllib2.urlopen(requestTask)
        datajsonTask = json.loads(responseTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
        #Ask if json have data
        Data = len(datajsonTask['todo-items'])
        if Data == 0:
            # set Limit to false
            Limite = False
        else:
            # i process data
            print ('================> Pagina: ' + str(Paginado) + 'Proyecto Id: ' + IdProyecto + ' <================')
            for dataValor in datajsonTask['todo-items']:
                #Get the NumProyecto
                ProyectoArray = str(dataValor['project-name']).split(" ")
                if dataValor.get('responsible-party-id') is None:
                    passt = 0
                else:
                    IdUsuarioTeam = str(dataValor['responsible-party-id']).split(",")
                    IdUsuario = IdUserSAP(str(IdUsuarioTeam[0]))
                    Accion = ExistenteTask(str(dataValor['id']))
                    TaskWord = str(dataValor['content'])
                    TaskWord = str(TaskWord).replace('\'',' ')
                    TaskWord = str(TaskWord).replace('"',' ')
                    TaskWord = str(TaskWord).strip()
                    TaskWords = str(TaskWord[:300])
                    #FechaInicio
                    AFI = str(dataValor['start-date'])
                    AFIs =  str(AFI[0:4])
                    MFI = str(dataValor['start-date'])
                    MFIs =  str(MFI[4:6])
                    DFI = str(dataValor['start-date'])
                    DFIs =  str(DFI[6:8])
                    #FechaProgramada
                    FechaProgramada = str(dataValor['due-date'])
                    AFP = str(dataValor['start-date'])
                    AFPs =  str(AFP[0:4])
                    MFP = str(dataValor['start-date'])
                    MFPs =  str(MFP[4:6])
                    DFP = str(dataValor['start-date'])
                    DFPs =  str(DFP[6:8])

                    FechaFinal = str(dataValor['created-on']).split("T")
                    FF = FechaFinal[0]

                    FI = str(AFIs) + '-' + str(MFIs) + '-' + str(DFIs)
                    FP = str(AFPs) + '-' + str(MFPs) + '-' + str(DFPs)

                    Avance = str(dataValor['progress'])
                    TiempoEstimado = str(dataValor['estimated-minutes'])
                    if Accion == "Update":
                        Sql= 'UPDATE [SAP].[dbo].[AATareasTeamWork] SET [NoProyecto] = \'' + str(ProyectoArray[0]) + '\',[IdUsuario] = \'' + str(IdUsuario) + '\',[Tarea] = \'' + str(TaskWords) + '\' WHERE [IdTeamWork] = \'' + str(dataValor['id']) + '\''
                        #procesar_mssql(Sql)
                        print(Sql)
                    else:
                        va = 0
                        Sql = 'INSERT INTO [SAP].[dbo].[AATareasTeamWork] VALUES (\'' + str(ProyectoArray[0]) + '\',\'' + str(IdUsuario) + '\',\'' + str(dataValor['id']) + '\',\'' + str(TaskWords) + '\',\'' + str(FI) + '\',\'' + str(FP) + '\',\'' + str(FF) + '\',\'Avance\',\'EtiqFase\',\'EtiqDocumento\',\'EtiqDiciplica\',\'TiempoEstimado\',\'Evaluada\')'
                        #procesar_mssql(Sql)
                        print(Sql)
        Paginado += 1
print('#################################### Insert Task ############################')
for proyecto in projectos_id:
    allTaskCompleted(proyecto)
print('#################################### End Task ###############################')
