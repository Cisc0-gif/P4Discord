import os
import subprocess
import time
from datetime import datetime
from discord_webhooks import DiscordWebhooks

webhookURL = ""

class PerforceLogger():
    def __init__(self, webhook_url):
      """ Initializes a 30 second timer used to check if commits have been made.  """
      self.webhook_url = webhook_url
      self.global_store = {
        'latest_change': ''
      }
      self.serverOn = False

    def check_p4(self):
      """ Runs the p4 changes command to get the latest commits from the server. """
      proc = subprocess.Popen(["p4", "changes", "-t", "-m", "1", "-l"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
      (out, err) = proc.communicate()
      blit = out.decode('ISO-8859-1')
      if blit != "":
        self.serverOn = True
        change_num = str(blit.split()[1])
        p4_changes = subprocess.Popen('p4 describe -s ' + change_num, stdout=subprocess.PIPE, shell=True)
        formatp4c = p4_changes.stdout.read().decode('ISO-8859-1').replace("... //PROJECTNAME/main/", "") #FORMAT p4 describe OUPUT
        return formatp4c
      else:
        self.serverOn = False
        print("Waiting for Helix Core Server to start...")

    def check_for_changes(self, output):
      """ Figures out if the latest p4 change is new or should be thrown out. """
      if output != self.global_store['latest_change']:
        self.global_store['latest_change'] = output

        if '*pending*' in output: 
          return ''

        else:
          return output

      else: 
        return ''

    def post_changes(self):
      """ Posts the changes to the Discord server via a webhook. """
      output = self.check_p4()
      if self.serverOn == True:
        payload = self.check_for_changes(output)

        if payload != '':
          print(payload, datetime.now());
          message = DiscordWebhooks(self.webhook_url)
          message.set_content(color=0xc8702a, description='`%s`' % (payload))
          message.set_author(name='Perforce')
          #message.set_footer(text='https://github.com/JamesIves/perforce-commit-discord-bot', ts=True)
          message.send()
        else:
          return

      else:
        return

if __name__ == "__main__":
  """ Initializes the application loop that checks Perforce for changes. """
  DISCORD_WEBHOOK_URL = webhookURL #os.environ.get('DISCORD_WEBHOOK_URL')
  logger = PerforceLogger(DISCORD_WEBHOOK_URL)
  timer = time.time()
  print("===========Starting application loop...===========");

  while True:
    logger.post_changes()
    time.sleep(30.0 - ((time.time() - timer) % 30.0))