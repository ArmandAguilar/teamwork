# Teamwork To MMSQL

> This script was made for can sync field that be in the Teamwork DB and downloaded this registers and loads in our data base in MMSQL server.

### Tools used in this project

- Python 2.7.11
- pypyodbc
- urllib2
- json
- simplejson
- unicodedata
- datetime,time
- sys

### Descriptions of scripts

**migarar_a_sap** : This script make a migration between tow tables compare the register of table (AATiemposProduccionClon) and make the insert or update of the register in the  table (AATimeposProduccion).

**SAP_New_Administrative** : This script connect with the TeamworkApi and download all register of all user that have a register in your project of 9 hour,then the script insert the registres in the table AATimeposDeProduccionClon o make the update if theregistre exist in the table. (Only Administrative registers).


**Sap_produccion** : This script connect with the TeamworkApi and download all register of all user that have a register in your project of 9 hour,then the script insert the registres in the table AATimeposDeProduccionClon o make the update if the registre exist in the table. (Only Production registers).

**Tokes** :  This scrip have all tokes and connection string of app.

**projects** : This script give a list of all project that generate a cost and that are active in the pipe drive and EstadoDeProyectos.

**mssql** : This script  have function of make insert or update in DB MSSQL.

**validate** : This script have function of validation of register for example the script can know if a user have more of 9 hr in a project and don’t permit the insert o update of register.

**tareas** : This script make sync of all task  of all proyect of teamwork DB and them insert or update this task in MSSQL table AATareasTeamWork.
