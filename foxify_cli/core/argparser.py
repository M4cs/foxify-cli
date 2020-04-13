from foxify_cli.logger import error, info
from fuzzywuzzy import fuzz, process
from foxify_cli.core.methods import (
    clear, backup, clear_backup,
    apply, themes, version,
    helpmenu, configpath, information,
    update, restore
)

class ArgParser:
    def __init__(self, args):
        self.args = args
        self.accepted_args = [
            'backup', 'apply', 'update',
            'restore', 'clear', 'themes',
            'restart', 'help', 'version',
            'backup-clear', 'config', 'info'
        ]
        self.check_for_errors()
    
    def check_for_errors(self):
        for arg in self.args:
            if arg not in self.accepted_args:
                if self.args[self.args.index(arg) -1] == "apply":
                    pass
                elif self.args[self.args.index(arg) -1] == "download":
                    pass
                else:
                    self.get_matches(arg)
                    exit(1)
                
    def get_matches(self, arg):
        matches = process.extractBests(arg, self.accepted_args, limit=2)
        if not matches:
            error("Unknown Argument:", arg)
        else:
            m = []
            for match in matches:
                m.append(match[0])
            error("Unknown Argument:", arg)
            info("Possible Matches:", ', '.join(m))
            
    def run_args(self):
        for arg in self.args:
            if "clear" == arg:
                clear()
            if "backup" == arg:
                backup()
            if "backup-clear" == arg:
                clear_backup()
            if "apply" == arg:
                if not "backup" in self.args:
                    error("Please Prefix Apply with Backup in Order to Apply New Themes!")
                    exit(1)
                if not self.args.index('backup') < self.args.index('apply'):
                    error("Please Prefix Apply with Backup in Order to Apply New Themes!")
                    exit(1)
                theme_name = self.args[self.args.index('apply') + 1]
                apply(theme_name)
            if "restore" == arg:
                restore()
            if "themes" == arg:
                themes()
            if "version" == arg:
                version()
            if "help" == arg:
                helpmenu()
            if "config" == arg:
                configpath()
            if "info" == arg:
                information()
            if "update" == arg:
                update()