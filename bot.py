#! /usr/bin/env python
# -*- coding:utf-8 -*-
#
# @name   : P4Discord - Perforce x Discord Monitor
# @url    : https://github.com/Cisc0-gif
# @author : Cisc0-gif

import discord
import asyncio
import logging
import random
import sys
import os
import subprocess
import time
from datetime import datetime

# Go To https://discordapp.com/developers/applications/ and start a new application for Token
# **Enable MEMBER and MESSAGE intents**

#Get member intent to read users in server
intents = discord.Intents.default()
intents.members = True

client = discord.Client(command_prefix='/', description='Basic Commands', intents=intents)
TOKEN = ''
superuser = "" #superuser to manage admins and server

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

def client_run():
  os.system("start python webhook.py") #start webhook as side process with bot
  client.loop.create_task(background_loop())
  client.run(TOKEN)

def logwrite(msg): #writes chatlog to MESSAGES.log
  with open('MESSAGES.log', 'a+') as f:
    f.write(msg + '\n')
  f.close()

async def background_loop():
  await client.wait_until_ready()
  while not client.is_closed:
    print("Booted Up @ " + time.ctime())
    logwrite("Booted Up @ " + time.ctime())
    await asyncio.sleep(3600)  #Bootup Message

@client.event
async def on_ready():
  print('--------------------------------------------------------------------------------------')
  print('Server Connect Link:')
  print('https://discordapp.com/api/oauth2/authorize?scope=bot&client_id=' + str(client.user.id))
  print('--------------------------------------------------------------------------------------')
  print('Logged in as:')
  print(client.user.name)
  print("or")
  print(client.user)
  print("UID:")
  print(client.user.id)
  print('---------------------------------------------')
  print("LIVE CHAT LOG - See MESSAGES.log For History")
  print("---------------------------------------------")
  await client.change_presence(activity=discord.Game("PROJECT NAME"), status=discord.Status.online)

@client.event
async def on_message(message):
  if message.author == client.user:
    return #ignore what bot says in server so no message loop
  channel = message.channel
  print(message.author, "said:", message.content, "-- Time:", time.ctime()) #reports to discord.log and live chat
  logwrite(str(message.author) + " said: " + str(message.content) + "-- Time: " + time.ctime())

  def get_members():
      guild = message.guild
      if guild:
        members = guild.members
        member_names = [member.name for member in members]
        return member_names

  #check if user has admin privileges
  async def check_admin():
    try:
      f = open("admins.txt","r")
      if f.mode == 'r':
        contents = f.read()
    finally:
      f.close()
    if str(message.author) not in contents and superuser not in str(message.author):
      await channel.send(":ERROR: Only promoted users can run this command")
      raise asyncio.CancelledError()
    else:
      pass

  #check if user has superuser privileges
  async def check_superuser():
    if superuser not in str(message.author):
      await channel.send(":ERROR: Only " + superuser + " can run this command")
      raise asyncio.CancelledError()
    else:
      pass

  #start perforce server + broker
  if message.content == "/p4 start":
    await check_admin()
    os.system("start /b p4d")
    os.system("start /b D:\HelixCoreBroker\p4broker.exe") #FILE PATH TO P4BROKER HERE (OR REMOVE IF NO SSL)
    await channel.send("Perforce Server starting...")
    await channel.send("Helix Core Broker starting...")

  #stop perforce server
  elif message.content == "/p4 stop":
    await check_admin()
    os.system("p4 admin stop")
    await channel.send("Perforce Server stopped...")

  #get server status
  elif message.content == "/p4 status":
    proc = subprocess.Popen(["p4", "info"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
    (out, err) = proc.communicate()
    if str(out) == "b''":
      await channel.send("Perforce Server: offline")
    else:
      await channel.send("Perforce Server: online")

  #check if storage drive connected
  elif message.content == "/p4 checkdrive":
    result = subprocess.check_output(["wmic", "logicaldisk", "get", "name"])
    if b'D:' in result:
      await channel.send("D: drive connected")
    else:
      await channel.send("D: drive not connected")

  #promote user to admin
  elif "/p4 promote" in message.content:
    await check_superuser()
    cmd = message.content.split()
    user = str(cmd[len(cmd)-1])
    member_names = get_members()
    if user in member_names:
        with open("admins.txt", "r") as f:
          admins = f.read()
        if user not in admins: #check if user in admins
            try:
              f = open("admins.txt", "a")
              if f.mode == "a":
                f.write(user + '\n')
                await channel.send(user + " was promoted to admin")
            finally:
              f.close()
        else:
            await channel.send(user + " is already an admin")
    else:
        await channel.send(user + " is not in this server")

  #demote admin to user
  elif "/p4 demote" in message.content:
    await check_superuser()
    cmd = message.content.split()
    user = str(cmd[len(cmd)-1])
    with open("admins.txt", "r") as f:
      admins = f.read()
    if user in admins: #check if user in admins
        try:
            with open("admins.txt", "r") as f:
                lines = f.readlines()
        
            lines = [line for line in lines if line.strip() != user.strip()]

            with open("admins.txt", "w") as f:
                f.writelines(lines)

            await channel.send(user + " was demoted")

        finally:
            f.close()
    else:
        await channel.send(user + " not found in admins")
      
  #view all users in server
  elif message.content == "/p4 users":
    await check_superuser()
    member_names = get_members()
    await channel.send('\n'.join(member_names))

  #view all admins
  elif message.content == "/p4 admins":
    await check_superuser()
    if os.path.getsize("admins.txt") > 0:
        try:
          f = open("admins.txt","r")
          if f.mode == 'r':
            contents = f.read()
            await channel.send(contents)
        finally:
          f.close()
    else:
        await channel.send(":ERROR: No admins found.")

  elif message.content == "/p4 help":
    if superuser in str(message.author): #only send superuser commands to superuser
      await message.author.send("========P4Discord *Superuser* Commands========\n/p4 promote            Promote user to admin\n/p4 demote              Demote admin to user\n/p4 users                  Get list of all members in server\n/p4 admins               Get list of all admin users")
    await channel.send("========P4Discord Commands========\n/p4 start                 Start Helix Core Server + Broker\n/p4 stop                  Stop Helix Core Server\n/p4 status               Get server status\n/p4 checkdrive      Get status of storage drive\n/p4 help                   Display this menu")

  elif "/p4" in message.content:
    await channel.send(":ERROR: Unknown command. Use '/p4 help' to view commands")

client_run()