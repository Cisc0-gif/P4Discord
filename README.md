# P4Discord - A Remote Perforce Client for Discord!

P4Discord is a Discord app that allows you to manage your locally-hosted Perforce server with Discord from anywhere in the world! Using James Ives [Perforce Commit Discord Bot](https://github.com/JamesIves/perforce-commit-discord-bot), and my own [Discord-Bot-Template](https://github.com/Cisc0-gif/Discord-Bot-Template), I created this bot as a wrapper for p4v, p4d, and p4broker so that you can manage perforce without having to connect to your server with SSH or Remote Desktop software.

## Features
* Sends submitted Change reports to your Discord server (Workspace, Time of Submission, Changelist #, Affected Files, etc)
* DMs Admin when P4 server crashes
* Give members of your Discord server Admin to control the P4 server
* Remotely Start, Stop, check the Status of your P4 server, and check external storage drives

## Setup

1. On your server machine, clone this repo onto your C: drive (```/p4 checkdrive``` checks if your storage drive is connected or not, so you should run this bot off an internal drive to prevent failure)
2. Use ```pip install -r requirements.txt``` to install necessary packages (Reliably tested with Python 3.7.2, anything past that is untested and may have dependency issues!)
3. Configure ```TOKEN```, ```webhookURL```, and ```startup.bat``` with necessary values (Bot Token, Webhook URL, filepath). WIN + R, enter "shell:startup", and place ```startup.bat``` in startup folder.
4. Then use ```python bot.py```. A second window should open, displaying the webhook.py console, and your main window should display a live chat log.
5. *Highly recommend going into your server system's BiOS settings and enabling Power On After Power Loss to automatically reboot in-case of power outages!*

## Commands

* ```/p4 start``` to start Helix Core Server + Helix Core Broker (*superuser* and *admin* users only)
* ```/p4 stop``` to stop Helix Core Server (*superuser* and *admin* users only)
* ```/p4 status``` to check if server is running
* ```/p4 checkdrive``` to check if server storage drive is connected
* ```/p4 presence NAME``` to set bot's game status on discord
* ```/p4 users``` to get list of members in server
* ```/p4 admins``` to check list of admin users (*superuser* only)
* ```/p4 promote USERNAME``` to promote users to admin (*superuser* only)
* ```/p4 demote USERNAME``` to demote admin to user (*superuser* only)
* Set ```webhookURL``` in webhook.py to send notifications everytime a change is pushed
* Put ```startup.bat``` in Startup folder to automatically start server on system reboot (failsafe)

## Built With

* James Ives' [perforce-commit-discord-bot](https://github.com/JamesIves/perforce-commit-discord-bot)
* Python 3.7.2
* GitHub

## Authors

* **Cisc0-gif** - *Main Contributor/Author*: fergo310@yahoo.com

## License

This project is licensed under the GPLv3 License - see LICENSE file for details


## Acknowledgments

All credits are given to the authors and contributors to tools used in this software
