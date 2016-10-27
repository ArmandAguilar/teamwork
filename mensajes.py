import sys
from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format


def cargardo():
    cprint(figlet_format('Procesando', font='slant'),'yellow', 'on_green', attrs=['bold'])

def proceso(texto):
    cprint(figlet_format(texto, font='slant'),'yellow', 'on_red', attrs=['bold'])

def proceso_terminado():
    cprint(figlet_format('Termino', font='slant'),'yellow', 'on_blue', attrs=['bold'])
