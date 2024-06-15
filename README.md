# P4Discord - A Perforce Manager for Discord!

P4Discord is a Discord app that allows you to manage your locally-hosted Perforce server from discord! Using James Ives [Perforce Commit Discord Bot](https://github.com/JamesIves/perforce-commit-discord-bot), and my own [Discord-Bot-Template](https://github.com/Cisc0-gif/Discord-Bot-Template), I created this bot as a wrapper for p4v, p4d, and p4broker so that you can manage perforce without having to connect to your server with SSH or Remote Desktop software.

## Setup

1. On your server machine, clone this repo onto your C: drive (```/p4 checkdrive``` checks if your storage drive is connected or not, so you should run this bot off an internal drive to prevent failure)
2. Use ```pip install -r requirements.txt``` to install necessary packages (Reliably tested with Python 3.7.2, anything past that is untested and may have dependency issues!)
3. Then use ```python bot.py```. A second window should open, displaying the webhook.py console, and your main window should display a live chat log.

## Features

* ```/p4 start``` to start Helix Core Server + Helix Core Broker (*superuser* and *admin* users only)
* ```/p4 stop``` to stop Helix Core Server (*superuser* and *admin* users only)
* ```/p4 status``` to check if server is running
* ```/p4 checkdrive``` to check if server storage drive is connected
* ```/p4 users``` to get list of members in server
* ```/p4 admins``` to check list of admin users (*superuser* only)
* ```/p4 promote USERNAME``` to promote users to admin (*superuser* only)
* ```/p4 demote USERNAME``` to demote admin to user (*superuser* only)
* Set ```webhookURL``` in webhook.py to send notifications everytime a change is pushed

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
