from foxify_cli.config.startup import CONFIG_PATH
from foxify_cli import version
from ruamel.yaml import YAML
from foxify_cli.logger import info, success, warning, error
from tqdm import tqdm
from time import sleep
from colorama import Fore, Style
from sys import platform
import zipfile
import requests
import shutil, os, psutil
import subprocess

FNULL = open(os.devnull, 'w')

def check_for_process(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def getversion():
    info("Foxify v" + version)
    exit(0)
    
def helpmenu():
    print("""\
Available Commands:

apply          -     Apply a theme based on the themes available
                     in your theme directory.
              
backup         -     Backup your current userChrome files to the
                     backup directory.
              
backup-clear   -     Delete your current backup.


clear          -     Remove the active theme on your Firefox profile.


help           -     Display this help menu.


restore        -     Restore your Firefox theme from a backup if one
                     exists for your active profile.

themes         -     See available themes in your theme directory and
                     the path to your theme directory.
                     
update         -     Check for updates of Foxify from the remote repo.


version        -     Display the current version of Foxify.


config         -     Display config directory and current settings.


info           -     Display info about Foxify and how to get themes.
          """)
    
def themes():
    themes = ""
    for file in os.listdir(os.path.realpath(CONFIG_PATH + "/themes")):
        themes = themes + file + ", "
    info("Theme Directory:", os.path.realpath(CONFIG_PATH + "/themes"))
    info("Available Themes:", themes[:-2])
    
def configpath():
    info("Config Directory:", CONFIG_PATH)
    with open(CONFIG_PATH + '/config', 'r') as f:
        yaml = YAML(typ='safe')
        config = yaml.load(f)
        for k, v in config.items():
            info(k.upper(), "|", v)

def backup():
    info("Backing Up Old Files")
    profile_dir = ""
    with open(CONFIG_PATH + '/config', 'r') as f:
        yaml = YAML(typ='safe')
        config = yaml.load(f)
        profile_dir = config['active_profile']
    if profile_dir:
        try:
            if len(os.listdir(os.path.realpath(profile_dir + '/chrome_backup/'))) >= 1:
                warning("Removing Prior Backup...")
                for file in os.listdir(os.path.realpath(profile_dir + '/chrome_backup/')):
                    if os.path.isdir(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file)):
                        shutil.rmtree(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file))
                    else:
                        os.remove(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file))
            for file in tqdm(os.listdir(os.path.realpath(profile_dir + '/chrome')), ncols=35, smoothing=True, bar_format=Fore.LIGHTCYAN_EX + Style.BRIGHT + "[PROGRESS] " + Fore.RESET + Style.RESET_ALL + '{n_fmt}/{total_fmt} | {bar}'):
                sleep(0.001)
                full_name = os.path.join(os.path.realpath(profile_dir + '/chrome'), file)
                if os.path.isdir(full_name):
                    shutil.copytree(full_name, os.path.realpath(profile_dir + '/chrome_backup/' + file))
                else:
                    shutil.copy(full_name, os.path.realpath(profile_dir + '/chrome_backup/' + file))
            success("Backed Up Files")
        except FileExistsError:
            error("Please Run 'foxify backup-clear' and remove your old backup first!")
            
def information():
    print(Fore.BLUE + """\
███████╗ ██████╗ ██╗  ██╗██╗███████╗██╗   ██╗
██╔════╝██╔═══██╗╚██╗██╔╝██║██╔════╝╚██╗ ██╔╝
█████╗  ██║   ██║ ╚███╔╝ ██║█████╗   ╚████╔╝ 
██╔══╝  ██║   ██║ ██╔██╗ ██║██╔══╝    ╚██╔╝  
██║     ╚██████╔╝██╔╝ ██╗██║██║        ██║   
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝        ╚═╝""")
    info("Version:", version)
    info("Created by Max Bridgland <https://github.com/M4cs>")
    info("Find More FirefoxCSS Themes At These Links:")
    print("https://www.reddit.com/r/FirefoxCSS/")
    print("https://github.com/Timvde/UserChrome-Tweaks")
    print("https://github.com/MrOtherGuy/firefox-csshacks")
    print(Fore.RESET + Style.RESET_ALL)
            
def clear_backup():
    warning("You are about to clear your backup! This means all backup files will be deleted.\nAre you sure you want to continue? Y\\n")
    ans = input("> ")
    if ans.lower() == "y":
        warning("Starting Backup Deletion!")
        with open(CONFIG_PATH + '/config', 'r') as f:
            yaml = YAML(typ='safe')
            config = yaml.load(f)
            profile_dir = config['active_profile']
            for file in tqdm(os.listdir(os.path.realpath(profile_dir + '/chrome_backup')), ncols=35, smoothing=True, bar_format=Fore.LIGHTCYAN_EX + Style.BRIGHT + "[PROGRESS] " + Fore.RESET + Style.RESET_ALL + '{n_fmt}/{total_fmt} | {bar}'):
                if os.path.isdir(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file)):
                    shutil.rmtree(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file))
                else:
                    os.remove(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file))
        success("Deletion Complete.")
    else:
        warning("Skipping Backup Clearing")
        
def update():
    with open(CONFIG_PATH + '/config', 'r') as f:
        yaml = YAML(typ='safe')
        config = yaml.load(f)
        if not config['check_for_updates']:
            res = requests.get('https://raw.githubusercontent.com/M4cs/foxify-cli/master/version').text
            if config['version'] != res:
                info("Update Available! Run 'pip3 install --upgrade foxify-cli' to Update to Version: " + res)
        

def restore():
    warning("You are about to restore from your backup! This means all current custom files will be restored with older ones.\nAre you sure you want to continue? Y\\n")
    ans = input("> ")
    if ans.lower() == "y":
        with open(CONFIG_PATH + '/config', 'r') as f:
            yaml = YAML(typ='safe')
            config = yaml.load(f)
            profile_dir = config['active_profile']
            info("Deleting Current Customization Files...")
            for file in tqdm(os.listdir(os.path.realpath(profile_dir + '/chrome')), ncols=35, smoothing=True, bar_format=Fore.LIGHTCYAN_EX + Style.BRIGHT + "[PROGRESS] " + Fore.RESET + Style.RESET_ALL + '{n_fmt}/{total_fmt} | {bar}'):
                if os.path.isdir(os.path.join(os.path.realpath(profile_dir + '/chrome'), file)):
                    shutil.rmtree(os.path.join(os.path.realpath(profile_dir + '/chrome'), file))
                else:
                    os.remove(os.path.join(os.path.realpath(profile_dir + '/chrome'), file))
            info("Starting Restore Process...")
            for file in tqdm(os.listdir(os.path.realpath(profile_dir + '/chrome_backup')), ncols=35, smoothing=True, bar_format=Fore.LIGHTCYAN_EX + Style.BRIGHT + "[PROGRESS] " + Fore.RESET + Style.RESET_ALL + '{n_fmt}/{total_fmt} | {bar}'):
                if os.path.isdir(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file)):
                    shutil.copytree(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file), os.path.realpath(profile_dir + '/chrome/' + file))
                else:
                    shutil.copy(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file), os.path.realpath(profile_dir + '/chrome/' + file))
            success("Completed Restore Process, Killing Firefox!")
            if check_for_process("firefox"):
                if platform == "linux" or platform == "linux2" or platform == "darwin":
                    subprocess.call(['killall', 'firefox'], stdout=FNULL, stderr=subprocess.STDOUT)
                elif platform == "win32":
                    subprocess.call(['taskkill', '/f', '/im', 'firefox.exe'], stdout=FNULL, stderr=subprocess.STDOUT)
                success("Closed Firefox! Re-open to see your new theme!")
            else:
                info("Couldn't find a process for Firefox, if you are running it you may have to close it manually!")
            
def clear():
    while True:
        warning("You are about to remove your current theme. Would you like to back it up? Y\\n")
        ans = input("> ")
        if ans.lower() == "y":
            warning("Backing Up Files!")
            with open(CONFIG_PATH + '/config', 'r') as f:
                yaml = YAML(typ='safe')
                config = yaml.load(f)
                profile_dir = config['active_profile']
                for file in tqdm(os.listdir(os.path.realpath(profile_dir + '/chrome_backup')), ncols=35, smoothing=True, bar_format=Fore.LIGHTCYAN_EX + Style.BRIGHT + "[PROGRESS] " + Fore.RESET + Style.RESET_ALL + '{n_fmt}/{total_fmt} | {bar}'):
                    if os.path.isdir(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file)):
                        shutil.rmtree(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file))
                    else:
                        os.remove(os.path.join(os.path.realpath(profile_dir + '/chrome_backup'), file))
            backup()
            warning("Starting Theme Removal!")
            with open(CONFIG_PATH + '/config', 'r') as f:
                yaml = YAML(typ='safe')
                config = yaml.load(f)
                profile_dir = config['active_profile']
                for file in tqdm(os.listdir(os.path.realpath(profile_dir + '/chrome')), ncols=35, smoothing=True, bar_format=Fore.LIGHTCYAN_EX + Style.BRIGHT + "[PROGRESS] " + Fore.RESET + Style.RESET_ALL + '{n_fmt}/{total_fmt} | {bar}'):
                    if os.path.isdir(os.path.join(os.path.realpath(profile_dir + '/chrome'), file)):
                        shutil.rmtree(os.path.join(os.path.realpath(profile_dir + '/chrome'), file))
                    else:
                        os.remove(os.path.join(os.path.realpath(profile_dir + '/chrome'), file))
            break
        elif ans.lower() == "n":   
            warning("Starting Theme Removal!")
            with open(CONFIG_PATH + '/config', 'r') as f:
                yaml = YAML(typ='safe')
                config = yaml.load(f)
                profile_dir = config['active_profile']
                for file in tqdm(os.listdir(os.path.realpath(profile_dir + '/chrome')), ncols=35, smoothing=True, bar_format=Fore.LIGHTCYAN_EX + Style.BRIGHT + "[PROGRESS] " + Fore.RESET + Style.RESET_ALL + '{n_fmt}/{total_fmt} | {bar}'):
                    if os.path.isdir(os.path.join(os.path.realpath(profile_dir + '/chrome'), file)):
                        shutil.rmtree(os.path.join(os.path.realpath(profile_dir + '/chrome'), file))
                    else:
                        os.remove(os.path.join(os.path.realpath(profile_dir + '/chrome'), file))
            break
        else:
            warning("Unknown Option Please Try Again!")
    info("Attempting to Kill Firefox...")
    if check_for_process("firefox"):
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            subprocess.call(['killall', 'firefox'], stdout=FNULL, stderr=subprocess.STDOUT)
        elif platform == "win32":
            subprocess.call(['taskkill', '/f', '/im', 'firefox.exe'], stdout=FNULL, stderr=subprocess.STDOUT)
        success("Closed Firefox!")
    else:
        info("Couldn't find a process for Firefox, if you are running it you may have to close it manually!")
    config = {}
    with open(CONFIG_PATH + '/config', 'r') as f:
        yaml = YAML(typ='safe')
        config = yaml.load(f)
        config['active_theme'] = 'default'
    with open(CONFIG_PATH + '/config', 'w') as f:
        yaml = YAML()
        yaml.default_flow_style = False
        yaml.dump(config, f)
        
def apply(theme_name):
    if os.path.exists(os.path.realpath(CONFIG_PATH + "/themes/" + theme_name)):
        info("Applying " + theme_name + " to Firefox...")
        with open(CONFIG_PATH + '/config', 'r') as f:
            yaml = YAML(typ='safe')
            config = yaml.load(f)
            profile_dir = config['active_profile']
            if theme_name == config['active_theme']:
                error('That theme is already active!')
                exit(1)
            for file in tqdm(os.listdir(os.path.realpath(CONFIG_PATH + '/themes/' + theme_name)), ncols=35, smoothing=True, bar_format=Fore.LIGHTCYAN_EX + Style.BRIGHT + "[PROGRESS] " + Fore.RESET + Style.RESET_ALL + '{n_fmt}/{total_fmt} | {bar}'):
                if file != ".git":
                    if os.path.isdir(os.path.join(os.path.realpath(CONFIG_PATH + '/themes/' + theme_name), file)):
                        shutil.copytree(os.path.join(os.path.realpath(CONFIG_PATH + '/themes/' + theme_name), file), os.path.realpath(profile_dir + '/chrome/' + file))
                    else:
                        shutil.copy(os.path.join(os.path.realpath(CONFIG_PATH + '/themes/' + theme_name), file), os.path.realpath(profile_dir + '/chrome/' + file))
        success("Applied Theme Closing Firefox...")
        if check_for_process("firefox"):
            if platform == "linux" or platform == "linux2" or platform == "darwin":
                subprocess.call(['killall', 'firefox'], stdout=FNULL, stderr=subprocess.STDOUT)
            elif platform == "win32":
                subprocess.call(['taskkill', '/f', '/im', 'firefox.exe'], stdout=FNULL, stderr=subprocess.STDOUT)
            success("Closed Firefox! Re-open to see your new theme!")
        else:
            info("Couldn't find a process for Firefox, if you are running it you may have to close it manually!")
        with open(CONFIG_PATH + '/config', 'r') as f:
            yaml = YAML(typ='safe')
            config = yaml.load(f)
            config['active_theme'] = theme_name
        with open(CONFIG_PATH + '/config', 'w') as f:
            yaml = YAML()
            yaml.default_flow_style = False
            yaml.dump(config, f)
    else:
        error("No Theme Found: " + theme_name)
        exit(1)