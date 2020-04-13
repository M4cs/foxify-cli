<img src="https://mbcdn.sfo2.cdn.digitaloceanspaces.com/Foxify.png">

# foxify-cli
[![GitHub issues](https://img.shields.io/github/issues/M4cs/foxify-cli)](https://github.com/M4cs/foxify-cli/issues)
[![GitHub stars](https://img.shields.io/github/stars/M4cs/foxify-cli)](https://github.com/M4cs/foxify-cli/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/M4cs/foxify-cli)](https://github.com/M4cs/foxify-cli/network/members)

Customize Firefox from the command line and control all your custom userChrome CSS themes with one tool!

# Overview

As of Firefox 57 (the Quantum Update), Mozilla has enabled custom user customization using userChrome.css. This file is found in the chrome folder of your profile and allows you to customize the look of your browser. There is a huge community around this sort of themeing and it can get easy to mess up your theme or lose it when you install a new theme. With Foxify you have the ability to manage your themes for Firefox and apply them dynamically!

Foxify was heavily inspired by the command-line program [Spiceify for Spotify](https://github.com/khanhas/spicetify-cli), which offers similiar features but for Spotify!

<a href="https://www.reddit.com/r/FirefoxCSS/comments/fz8h2o/moonlight_userchrome/"><img src="https://i.redd.it/rma9z4itq7s41.png"  alt="img" align="right" width="400px"></a>
### Where To Find Themes:

#### FirefoxCSS Reddit: [Link](https://www.reddit.com/r/FirefoxCSS/)

#### UserChrome Tweaks: [Link](https://github.com/Timvde/UserChrome-Tweaks)

#### Firefox CSS Hacks: [Link](https://github.com/MrOtherGuy/firefox-csshacks)

### Requirements:

<a href="https://www.reddit.com/r/nordtheme/comments/g0mnyt/nordic_firefox_theme/"><img src="https://i.redd.it/omdp7nyz6ms41.png" alt="img" align="right" width="400px"></a>
**OS:** Windows, Mac, Linux

**Software Reqs:**

  - Python 3.6+
  - Firefox 57 or Higher
  
### Getting Started:

**Installing Foxify:**

To install Foxify you can simply use the Python Pip package manager. 

Run:
```
pip3 install foxify-cli
```
*pip3 may throw an error if you only have python3 installed. in that case run `pip install foxify-cli`*

You can also install Foxify by cloning the GitHub repo and installing manually:

```
git clone https://github.com/M4cs/foxify-cli
cd foxify-cli
python3 setup.py install
```

### Using Foxify:

Once you install Foxify you should now have access to the command `foxify`. This command will be what you will run before all arguments available. Below you can see the list of commands:

| Command | Description |
| :--: | :--: |
| apply [theme_name] | Apply a theme based on the themes available in your theme directory. |
| backup | Backup your current userChrome files to the ackup directory. |
| backup-clear | Delete the current backup. |
| clear | Remove the active theme on your Firefox profile. |
| help | Display the help menu. |
| restore | Restore your Firefox theme from a backup if one exists for your active profile. |
| themes | See path to theme directory and available themes. |
| update | Check for updates of Foxify from the remote repo. |
| version | Display the current version of Foxify. |
| config | Display config directory and current settings. |
| info | Display info about Foxify and how to get themes. |

### Common Command Combinations:

Backup and Apply a Theme:
```
foxify backup apply [theme_name]
```

Backup Active Theme:
```
foxify backup
```

Delete Backup:
```
foxify backup-clear
```

Restore From Backup:
```
foxify restore
```

Remove Active Theme:
```
foxify clear
```

Check Config Values:
```
foxify config
```

# License

Licensed under the GNU GPUv3 License by Max Bridgland, 2020
