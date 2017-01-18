#!user/bin/python
from tokens import *
from projects import *
from sap import *
from mssql import *
import pypyodbc as pyodbc
reload(sys)
sys.setdefaultencoding("utf-8")

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
                    Sql = 'INSERT INTO TABLE VALUES(\'' + str(ProyectoArray[0]) + '\',\'' + str(IdUsuario) + '\',\'' + str(dataValor['content']) + '\',\'' + dataValor['id'] + '\')'
                    print(Sql)
                    li += 1
        Paginado += 1
    print ('No Task: ' + str(li))

allTaskCompleted('271345')
