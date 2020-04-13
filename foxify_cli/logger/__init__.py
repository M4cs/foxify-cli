from colorama import Fore as f
from colorama import Style as s

def error(*msgs):
    print(f.RED + s.BRIGHT + "[ERROR]" + f.RESET + s.RESET_ALL, *msgs)

def warning(*msgs):
    print(f.YELLOW + s.BRIGHT + "[WARNING]" + f.RESET + s.RESET_ALL, *msgs)

def info(*msgs):
    print(f.LIGHTBLUE_EX + s.BRIGHT + "[INFO]" + f.RESET + s.RESET_ALL, *msgs)
    
def success(*msgs):
    print(f.GREEN + s.BRIGHT + "[SUCCESS]" + f.RESET + s.RESET_ALL, *msgs)