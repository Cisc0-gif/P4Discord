# P4Discord - A Remote Perforce Client for Discord!

Hosting your own Perforce server locally? P4Discord is a bot that allows you to manage your server from Discord! Get live updates on Submits, restart your server, and add your own commands for more!

Using James Ives [Perforce Commit Discord Bot](https://github.com/JamesIves/perforce-commit-discord-bot), and my own [Discord-Bot-Template](https://github.com/Cisc0-gif/Discord-Bot-Template), I created this bot as a wrapper for p4v and p4d so you can manage a local server without having to use remote software.

## Features
* More secure than RDP connections
* Sends Submit reports to Discord Channels in realtime using Webhooks (Workspace, Time of Submission, Changelist #, Affected Files, etc)
* Remotely Start, Stop, check the Status of your Perforce server
* Features an Admin List, to allow other users to control the server

## Setup

1. On your server machine, clone this repo.
2. Run ```Setup.bat``` to run setup installer (it'll prompt for your P4Root directory, Bot Token, Webhook URL from the channel you'd like to post Submits to, and your P4 Admin Password to allow access for live Submit checks)

## Recommendations
* *Highly recommend going into your server's BiOS settings and enabling Power On After Power Loss to automatically reboot in-case of outages!*
* [Tailscale](https://tailscale.com) is a VPN service that bridges server and workspace machines into a virtual network—as if each machine was on the same LAN—making it way easier to connect remotely. (Free plan is up to 3 users!)

## Default Commandlist

* ```/help``` Returns this commandlist
* ```/latest``` Posts latest changelist to webhook channel
* ```/ping``` Returns Perforce server status
* ```/presence STRING``` Sets the Bot's App Activity in Discord
* ```/restart``` Runs p4 admin restart
* ```/session``` Checks Perforce login session (for webhook functionality)
* ```/stop``` Runs p4 admin stop

## Built With

* James Ives' [perforce-commit-discord-bot](https://github.com/JamesIves/perforce-commit-discord-bot)
* Python 3.7.2
* GitHub
* Claude

## Authors

* **Cisc0-gif** - *Main Contributor/Author*: fergo310@yahoo.com

## License

This project is licensed under the GPLv3 License - see LICENSE file for details


## Acknowledgments

All credits are given to the authors and contributors to tools used in this software
