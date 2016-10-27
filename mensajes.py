import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format


def cargardo():
    cprint(figlet_format('Procesando', font='starwars'),'yellow', 'on_green', attrs=['normal'])

def proceso(texto):
    cprint(figlet_format(texto, font='starwars'),'yellow', 'on_red', attrs=['normal'])

def proceso_terminado():
    cprint(figlet_format('Procesando', font='starwars'),'yellow', 'on_blue', attrs=['normal'])
