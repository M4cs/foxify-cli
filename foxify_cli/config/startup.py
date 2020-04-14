import os, requests
from foxify_cli import version
from foxify_cli.logger import info
from ruamel.yaml import YAML

CONFIG_PATH = os.path.realpath(os.path.expanduser('~') + "/.config/foxify")
DEFAULT_THEME_PATH = os.path.realpath(CONFIG_PATH + "/themes/")
DEFAULT_CONFIG = os.path.realpath(CONFIG_PATH + "/config")
DCONF = {
    "active_theme": "default",
    "active_profile": "",
    "theme_directory": DEFAULT_THEME_PATH,
    "version": version,
    "config_version": 1,
    "check_for_updates": True
}

def startup():
    if not os.path.exists(CONFIG_PATH):
        info("Foxify Directory Missing! Creating One For You...")
        os.makedirs(CONFIG_PATH)
        os.makedirs(DEFAULT_THEME_PATH)
    if not os.path.exists(DEFAULT_CONFIG):
        while True:
            info("If you have not yet setup userChrome CSS Cusotmization\nPlease Open Up Your Firefox Browser and Follow These Steps:")
            print("""\
1. Go to "about:support" by typing it into your Address Bar

2. Copy the File Path for your Profile Folder

3. Enter it below""")
            filepath = input("> ")
            print("You Entered:", filepath.strip())
            print("Is this correct? Y\\n")
            ans = input("> ")
            if ans.lower() == "y":
                DCONF['active_profile'] = os.path.realpath(filepath.strip())
                info("Writing Default Configuration...")
                with open(DEFAULT_CONFIG, 'w') as f:
                    yaml = YAML()
                    yaml.default_flow_style = False
                    yaml.dump(DCONF, f)
                info("Checking If userChrome CSS Customization is Enabled")
                with open(DCONF['active_profile'] + '/prefs.js', 'r') as f:
                    match = False
                    deact_match = False
                    for line in f.readlines():
                        if line == '"user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);"':
                            match = True
                        if line == '"user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", false);"':
                            deact_match = True
                if not match:
                    info('Enabling userChrome CSS Customization')
                    with open(DCONF['active_profile'] + '/prefs.js', 'a') as f:
                        f.write('user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", false);')
                if not match and deact_match:
                    info('Enabling userChrome CSS Customization')
                    with open(DCONF['active_profile'] + '/prefs.js', 'w') as f:
                        content = f.read()
                        content = content.replace('user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", false);', 'user_pref("toolkit.legacyUserProfileCustomizations.stylesheets", true);')
                        f.write()
                info('Checking For Chrome and Backup Directory')
                if not os.path.exists(DCONF['active_profile'] + '/chrome'):
                    os.makedirs(DCONF['active_profile'] + '/chrome')
                if not os.path.exists(DCONF['active_profile'] + '/chrome_backup'):
                    os.makedirs(DCONF['active_profile'] + '/chrome_backup')
                info('Chrome Directory and Backup Directory Created')
                break
            else:
                pass
    else:
        with open(DEFAULT_CONFIG, 'r') as f:
            yaml = YAML(typ='safe')
            config = yaml.load(f)
        if not config.get('config_version'):
            for k, v in DCONF.items():
                if not config.get(k):
                    config[k] = v
            with open(DEFAULT_CONFIG, 'w') as f:
                yaml = YAML()
                yaml.default_flow_style = False
                yaml.dump(config, f)
        if config['config_version'] != 1:
            for k, v in DCONF.items():
                if not config.get(k):
                    config[k] = v
            with open(DEFAULT_CONFIG, 'w') as f:
                yaml = YAML()
                yaml.default_flow_style = False
                yaml.dump(config, f)
        if config['check_for_updates']:
            res = requests.get('https://raw.githubusercontent.com/M4cs/foxify-cli/master/version').text
            if res == version:
                config['version'] = version
                print(version)
                with open(DEFAULT_CONFIG, 'w') as f:
                    yaml = YAML()
                    yaml.default_flow_style = False
                    yaml.dump(config, f)
            else:
                info("Update Available! Run 'pip3 install --upgrade foxify-cli' to Update to Version: " + res)