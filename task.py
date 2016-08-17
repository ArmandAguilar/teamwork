#!user/bin/python
from tokens import *
import urllib2, base64
import json
import unicodedata
import sys
from datetime import datetime,time
reload(sys)
sys.setdefaultencoding("utf-8")
##if datos['id'] == '281337':
#    requestTask = urllib2.Request("https://forta.teamwork.com/projects/" + str(datos['id'])  +"/tasks.json")
#    requestTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
#    responseTask = urllib2.urlopen(requestTask)
#    datajsonTaks = json.loads(responseTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
#    i = 0

#    for Task in datajsonTaks['todo-items']:
#        i += 1
#        if Task.get('responsible-party-ids') is None:
#            print ('[--Task('+ str(Task['id']) +'): ' + str(Task['content']) + ' Responsable: None ]')
#        else:
#            print ('--[Task('+ str(Task['id']) +'): ' + str(Task['content']) + ']')
#            print ('---->Responsable: ' + str(Task['responsible-party-ids']) + ' | ' + str(Task['responsible-party-names']))
def task(arg):
    if arg == '281337':
        requestTask = urllib2.Request("https://forta.teamwork.com/projects/" + str(arg)  +"/tasks.json")
        requestTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
        responseTask = urllib2.urlopen(requestTask)
        datajsonTaks = json.loads(responseTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
        i = 0
        for Task in datajsonTaks['todo-items']:
            i += 1
            if Task.get('responsible-party-ids') is None:
                print ('[++Task('+ str(Task['id']) +'): ' + str(Task['content']) + ' Responsable: None ]')
            else:
                print ('--[Task('+ str(Task['id']) +'): ' + str(Task['content']) + ']')
                print ('---->Responsable: ' + str(Task['responsible-party-ids']) + ' | ' + str(Task['responsible-party-names']))
                TaksTiempoDiarios(str(Task['id']))

def TaksTiempoDiarios(idtask):

    #print('https://forta.teamwork.com/tasks/' + str(idtask) + '/time_entries.json')
    requestActivitiesTask = urllib2.Request('https://forta.teamwork.com/tasks/' + str(idtask) + '/time_entries.json')
    requestActivitiesTask.add_header("Authorization", "BASIC " + base64.b64encode(key + ":xxx"))
    responseActivitiesTask = urllib2.urlopen(requestActivitiesTask)
    datajsonActivitiesTask = json.loads(responseActivitiesTask.read(),encoding='utf-8',cls=None,object_hook=None, parse_float=None,parse_int=None, parse_constant=None,object_pairs_hook=None)
    for activities in datajsonActivitiesTask['time-entries']:
        print ('------>Tarea:' + str(activities['parentTaskName']) + '-' + str(activities['todo-item-name']) + ' Ejecutor:' + str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + ' Id:' + str(activities['person-id']))
        ProyectoArray = str(activities['project-name']).split(" ")
        FechaJsonArrays = str(activities['date']).split("T")
        sql = 'Insert Into AARegistroTiemposDiarios values(\'' +str(idtask) + '\',\'' + str(activities['person-id']) + '\',\'' + ProyectoArray[0] + '\',\''+ str(activities['person-first-name']) + ' ' + str(activities['person-last-name']) + '\',\'' + FechaJsonArrays[0] + '\',\'' + str(activities['hours']) + '\')'
        print (str(sql))
