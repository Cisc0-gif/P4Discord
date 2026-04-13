#! /usr/bin/env python
# -*- coding:utf-8 -*-

import discord
from discord.ext import commands
import asyncio
import logging
import os
import subprocess
import time
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

# ================= CONFIG =================
TOKEN = ""
WEBHOOK_URL = ""
superuser = "" #SUPERUSER Discord ID HERE (Get from Messages output!)

CHECK_INTERVAL = 30
PROJECT_PATH = "... //PROJECTNAME/main/"
P4_PASSWORD = ""

# ================= INTENTS =================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# ================= LOGGING =================
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s'))
logger.addHandler(handler)

def logwrite(msg):
    with open('MESSAGES.log', 'a+') as f:
        f.write(msg + '\n')

def format_user(user):
    if hasattr(user, "discriminator") and user.discriminator != "0":
        return f"{user.name}#{user.discriminator} (ID: {user.id})"
    if hasattr(user, "global_name") and user.global_name:
        return f"{user.global_name} (ID: {user.id})"
    return f"{user.name} (ID: {user.id})"

# ================= PERFORCE =================
class PerforceMonitor:
    def __init__(self):
        self.latest_change = ''

    def run_p4(self, args):
        env = os.environ.copy()
        env["P4PASSWD"] = P4_PASSWORD
        proc = subprocess.Popen(
            ["p4"] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        out, err = proc.communicate()
        if err:
            print("P4 STDERR:", err.decode(errors="ignore"))
        return out.decode(errors="ignore").strip()

    def ensure_login(self):
        out = self.run_p4(["login", "-s"])
        if "ticket expires" in out.lower():
            return True
        # Session expired, attempt re-login
        env = os.environ.copy()
        env["P4PASSWD"] = P4_PASSWORD
        proc = subprocess.Popen(
            ["p4", "login"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        out, err = proc.communicate(input=P4_PASSWORD.encode())
        return proc.returncode == 0

    def check_p4(self):
        try:
            if not self.ensure_login():
                print("P4 login failed, skipping changelist check")
                return ''
            # Get latest change
            output = self.run_p4(["changes", "-m", "1"])
            if not output:
                return ''
            parts = output.split()
            if len(parts) < 2:
                return ''
            change_num = parts[1]
            result = self.run_p4(["describe", "-s", change_num])
            result = result.replace(PROJECT_PATH, "")
            
            # Remove "Affected files" section
            if "Affected files" in result:
                result = result.split("Affected files")[0]
            
            return result.strip()
        except Exception as e:
            print("P4 exception:", e)
            return ''

    def get_new_change(self, output):
        if output and output != self.latest_change and '*pending*' not in output:
            self.latest_change = output
            return output
        return ''

    def send_to_discord(self, payload):
        webhook = DiscordWebhook(url=WEBHOOK_URL)
        embed = DiscordEmbed(
            title='Perforce Update',
            description=f'`{payload[:1900]}`',
            color=0xc8702a #,timestamp=datetime.now().astimezone().isoformat()
        )
        webhook.add_embed(embed)
        webhook.execute()

p4 = PerforceMonitor()

# ================= UTIL =================
def server_status():
    try:
        proc = subprocess.Popen(["p4", "info"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        out, _ = proc.communicate()
        return bool(out)
    except:
        return False

def is_admin(user_id):
    if not os.path.exists("admins.txt"):
        return False
    with open("admins.txt", "r") as f:
        admins = f.read()
    return str(user_id) in admins or str(user_id) == superuser

def is_superuser(user_id):
    return str(user_id) == superuser

# ================= BACKGROUND LOOPS =================
async def perforce_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        output = p4.check_p4()
        if output:
            payload = p4.get_new_change(output)
            if payload:
                print(f"New changelist detected @ {datetime.now()}")
                p4.send_to_discord(payload)
            else:
                print(f"Checked Perforce @ {datetime.now()} (no new changelist)")
        else:
            print(f"Checked Perforce @ {datetime.now()} (no output)")
        await asyncio.sleep(CHECK_INTERVAL)

async def heartbeat_loop():
    await bot.wait_until_ready()
    while not bot.is_closed():
        msg = "Heartbeat @ " + time.ctime()
        print(msg)
        logwrite(msg)
        await asyncio.sleep(3600)

# ================= EVENTS =================
@bot.event
async def on_ready():
    print("Logged in as:", bot.user)
    if os.path.exists("game_presence.txt") and os.path.getsize("game_presence.txt") > 0:
        with open("game_presence.txt", "r") as f:
            game = f.read()
    else:
        game = "DEFAULT PRESENCE"
        with open("game_presence.txt", "w") as f:
            f.write(game)

    await bot.change_presence(activity=discord.Game(game))

    # 🔥 SEND INITIAL CHANGE
    print("Fetching initial changelist...")
    output = p4.check_p4()
    if output:
        p4.latest_change = output
        p4.send_to_discord(output)
        print("Initial changelist sent")
    else:
        print("No initial changelist found")

    bot.loop.create_task(perforce_loop())
    bot.loop.create_task(heartbeat_loop())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    user_tag = format_user(message.author)
    print(user_tag, "said:", message.content, "-- Time:", time.ctime())
    logwrite(f"{user_tag} said: {message.content} -- Time: {time.ctime()}")
    await bot.process_commands(message)

# ================= COMMANDS =================
@bot.command()
async def ping(ctx):
    """Checks Perforce server status"""
    await ctx.send("Perforce Server: ONLINE" if server_status() else "Perforce Server: OFFLINE")

@bot.command()
async def stop(ctx):
    """Returns p4 admin stop"""
    if not is_admin(ctx.author.id):
        await ctx.send("ERROR: Admins only")
        return
    if server_status():
        os.system("p4 admin stop")
        await ctx.send("Perforce Server stopped...")
    else:
        await ctx.send("ERROR: Server already offline")

@bot.command()
async def restart(ctx):
    """Runs p4 admin restart"""
    if not is_admin(ctx.author.id):
        await ctx.send("ERROR: Admins only")
        return
    if server_status():
        os.system("p4 admin restart")
        await ctx.send("Perforce Server restarted...")
    else:
        await ctx.send("ERROR: Server offline")

@bot.command()
async def latest(ctx):
    """Returns latest changelist to webhook"""
    if not server_status():
        await ctx.send("Perforce Server: OFFLINE")
        return
    await ctx.send("Fetching latest changelist...")
    output = p4.check_p4()
    if not output:
        await ctx.send("No changelist found.")
        return
    print("Manual fetch @", datetime.now())
    p4.send_to_discord(output)
    await ctx.send("Latest changelist sent to webhook.")

@bot.command()
async def presence(ctx, *, game: str):
    """STRING - sets the App Activity"""
    if not is_superuser(ctx.author.id):
        await ctx.send("ERROR: Superuser only")
        return
    with open("game_presence.txt", "w") as f:
        f.write(game)
    await bot.change_presence(activity=discord.Game(game))
    await ctx.send(f"Presence updated to: {game}")

@bot.command()
async def session(ctx):
    """Checks Perforce login session"""
    await ctx.send("Checking Perforce login...")

    try:
        out = p4.run_p4(["login", "-s"])

        if "ticket expires" in out.lower():
            await ctx.send("✅ Perforce login is ACTIVE")
            return

        await ctx.send("⚠️ Session expired, attempting re-login...")

        env = os.environ.copy()
        env["P4PASSWD"] = P4_PASSWORD
        proc = subprocess.Popen(
            ["p4", "login"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )
        out, err = proc.communicate(input=P4_PASSWORD.encode())
        out = out.decode(errors="ignore")
        err = err.decode(errors="ignore")

        if "logged in" in out.lower() or proc.returncode == 0:
            await ctx.send("✅ Login successful")
        else:
            await ctx.send(f"❌ Login failed: {err or out}")

    except Exception as e:
        await ctx.send(f"❌ Error checking login: {e}")

# ================= RUN =================
bot.run(TOKEN)