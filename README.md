
# elvui_updater
A script for automatically updating ELVUI when a new version is released.

## What it does:
This script will query the Elvui downloads page to determine if the local version matches the current release. The new version will be downloaded and installed if there is a version mismatch.

## Prerequisites:
- Python 3.4+ (https://www.python.org/downloads/)
- LXML Lib (http://lxml.de/) `pip install lxml`
- Requests Lib (http://docs.python-requests.org/en/master/) `pip install requests`

## Install the script by scheduling a task:
###### Windows
1. If Task Scheduler is not open, start Task Scheduler. For more information, see Start Task Scheduler.
2. Find and click the task folder in the console tree that you want to create the task in. For more information about how to create the task in a new task folder, see Create a New Task Folder.
3. In the Actions Pane, click Create Basic Task.
4. Follow the instructions in the Create Basic Task Wizard.
    
Instructions from: [MS Technet](https://technet.microsoft.com/en-us/library/cc748993(v=ws.11).aspx#BKMK_winui)

## Generating the settings file:
In order to initialize the installer, the WoW installation folder needs to be specified in a plaintext settings file. This file should be named 'settings' and placed in the same directory as elvui_updater. The script will query the user for the full directory and generate the file if it is not present at runtime.
