@echo off
setlocal EnableDelayedExpansion
color 0A
title P4Discord Installer

echo.
echo  ============================================================
echo.  _____  _  _   _____  _                       _        ___    ___  
echo. |  __ \| || | |  __ \(_)                     | |      |__ \  / _ \ 
echo. | |__) | || |_| |  | |_ ___  ___ ___  _ __ __| | __   __ ) || | | |
echo. |  ___/|__   _| |  | | / __|/ __/ _ \| '__/ _` | \ \ / // / | | | |
echo. | |       | | | |__| | \__ \ (_| (_) | | | (_| |  \ V // /_ | |_| |
echo. |_|       |_| |_____/|_|___/\___\___/|_|  \__,_|   \_/|____(_)___/ 
echo.
echo          Discord Bot Installer  --  by P4Discord
echo  ============================================================
echo.
echo  Welcome! This installer will configure your P4Discord bot.
echo  Please follow the prompts carefully.
echo.
pause

:: ─────────────────────────────────────────────
:: STEP 1 — Install Python dependencies
:: ─────────────────────────────────────────────
echo.
echo  [1/6] Installing Python dependencies from requirements.txt...
echo  ────────────────────────────────────────────────────────────
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo.
    echo  [ERROR] pip install failed. Make sure Python and pip are
    echo          installed and requirements.txt is in this directory.
    pause
    exit /b 1
)
echo.
echo  [OK] Dependencies installed successfully.
echo.

:: ─────────────────────────────────────────────
:: STEP 2 — Ask for P4Root directory
:: ─────────────────────────────────────────────
echo.
echo  [2/6] Perforce Root Directory
echo  ────────────────────────────────────────────────────────────
echo  Enter the full path to your P4ROOT directory.
echo  Example: C:\Perforce\depot
echo.
set /p P4ROOT="  P4Root path: "

if "!P4ROOT!"=="" (
    echo.
    echo  [ERROR] P4Root path cannot be empty.
    pause
    exit /b 1
)

echo.
echo  [OK] P4Root set to: !P4ROOT!
echo.

:: ─────────────────────────────────────────────
:: STEP 3 — Ask for Discord Bot Token
:: ─────────────────────────────────────────────
echo.
echo  [3/6] Discord Bot Token
echo  ────────────────────────────────────────────────────────────
echo  Enter your Discord Bot Token.
echo  (Found at: https://discord.com/developers/applications)
echo.
set /p BOT_TOKEN="  Bot Token: "

if "!BOT_TOKEN!"=="" (
    echo.
    echo  [ERROR] Bot token cannot be empty.
    pause
    exit /b 1
)
echo.
echo  [OK] Bot token recorded.
echo.

:: ─────────────────────────────────────────────
:: STEP 4 — Ask for Discord Channel Webhook URL
:: ─────────────────────────────────────────────
echo.
echo  [4/8] Discord Channel Webhook URL
echo  ────────────────────────────────────────────────────────────
echo  Enter your Discord channel webhook URL.
echo  (Found in: Channel Settings ^> Integrations ^> Webhooks)
echo.
set /p WEBHOOK_URL="  Webhook URL: "

if "!WEBHOOK_URL!"=="" (
    echo.
    echo  [ERROR] Webhook URL cannot be empty.
    pause
    exit /b 1
)
echo.
echo  [OK] Webhook URL recorded.
echo.

:: ─────────────────────────────────────────────
:: STEP 5 — Ask for Superuser Discord ID
:: ─────────────────────────────────────────────
echo.
echo  [5/8] Superuser Discord ID
echo  ────────────────────────────────────────────────────────────
echo  The Superuser is the Discord account with full control over
echo  the bot. This ID unlocks all bot commands including /presence,
echo  /stop, /restart, and admin management.
echo.
echo  HOW TO FIND YOUR DISCORD ID:
echo.
echo  Option 1 - From the bot console (recommended first-time):
echo    1. Skip this step for now by pressing Enter.
echo    2. Finish setup, then run bot.py.
echo    3. Send ANY message in your Discord server.
echo    4. The console will print something like:
echo         YourName (ID: 123456789012345678) said: hello
echo    5. Re-run this installer and paste that number here.
echo.
echo  Option 2 - From Discord directly:
echo    1. Open Discord Settings ^> Advanced ^> Enable Developer Mode.
echo    2. Right-click your own profile picture anywhere in Discord.
echo    3. Click "Copy User ID" and paste it below.
echo.
set /p SUPERUSER_ID="  Superuser Discord ID: "

if "!SUPERUSER_ID!"=="" (
    echo.
    echo  [WARNING] No Superuser ID entered. Bot commands will be
    echo            restricted until this is set. Re-run the installer
    echo            once you have your ID.
    echo.
) else (
    echo.
    echo  [OK] Superuser ID recorded.
    echo.
)

:: ─────────────────────────────────────────────
:: STEP 6 — Ask for Perforce Admin Password
:: ─────────────────────────────────────────────
echo.
echo  [6/8] Perforce Admin Password
echo  ────────────────────────────────────────────────────────────
echo  Enter your Perforce admin account password.
echo  This is required for live Submit update notifications.
echo.
set /p P4_PASSWORD="  Perforce Password: "

if "!P4_PASSWORD!"=="" (
    echo.
    echo  [ERROR] Perforce password cannot be empty.
    pause
    exit /b 1
)
echo.
echo  [OK] Perforce password recorded.
echo.

:: ─────────────────────────────────────────────
:: STEP 7 — Write bot.py with all credentials
:: ─────────────────────────────────────────────
echo.
echo  [7/8] Writing configuration to bot.py...
echo  ────────────────────────────────────────────────────────────

if not exist "bot.py" (
    echo.
    echo  [ERROR] bot.py not found in the current directory.
    echo          Make sure you are running this installer from
    echo          the P4Discord root folder.
    pause
    exit /b 1
)

:: Use PowerShell regex to target the exact variable assignment lines in bot.py
powershell -Command "(Get-Content 'bot.py') -replace '^TOKEN = \".*\"', 'TOKEN = \"!BOT_TOKEN!\"' | Set-Content 'bot.py'"
powershell -Command "(Get-Content 'bot.py') -replace '^WEBHOOK_URL = \".*\"', 'WEBHOOK_URL = \"!WEBHOOK_URL!\"' | Set-Content 'bot.py'"
powershell -Command "(Get-Content 'bot.py') -replace '^P4_PASSWORD = \".*\"', 'P4_PASSWORD = \"!P4_PASSWORD!\"' | Set-Content 'bot.py'"
powershell -Command "(Get-Content 'bot.py') -replace '^superuser = \".*\"', 'superuser = \"!SUPERUSER_ID!\"' | Set-Content 'bot.py'"

echo  [OK] bot.py updated with your credentials.
echo.

:: ─────────────────────────────────────────────
:: STEP 8 — Write and deploy startup.bat
:: ─────────────────────────────────────────────
echo.
echo  [8/8] Creating startup.bat and deploying to Startup folder...
echo  ────────────────────────────────────────────────────────────

set "STARTUP_BAT=%~dp0startup.bat"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

(
    echo :: PUT THIS FILE IN STARTUP FOLDER IN CASE SERVER RESTARTS
    echo :: CTRL + R -^> "shell:startup" TO OPEN STARTUP FOLDER
    echo @echo off
    echo cd !P4ROOT!
    echo python bot.py
) > "!STARTUP_BAT!"

copy /Y "!STARTUP_BAT!" "!STARTUP_FOLDER!\startup.bat" >nul
if %ERRORLEVEL% neq 0 (
    echo.
    echo  [WARNING] Could not copy startup.bat to the Startup folder.
    echo            You may need to run this installer as Administrator.
    echo            Manual path: !STARTUP_FOLDER!
) else (
    echo  [OK] startup.bat deployed to Windows Startup folder.
)
echo.

:: ─────────────────────────────────────────────
:: Configure Perforce service to Automatic
:: ─────────────────────────────────────────────
echo  Configuring Perforce service to start Automatically...
sc config Perforce start= auto >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo  [WARNING] Could not configure Perforce service.
    echo            The service may not be installed, or you may need
    echo            to run this installer as Administrator.
) else (
    echo  [OK] Perforce service set to Automatic startup.
)
echo.

:: ─────────────────────────────────────────────
:: Done!
:: ─────────────────────────────────────────────
echo.
echo  ============================================================
echo   INSTALLATION COMPLETE
echo  ============================================================
echo.
echo   P4Discord has been configured and is ready to run.
echo.
echo   Summary:
echo     P4Root    : !P4ROOT!
echo     Bot Token : [saved to bot.py]
echo     Webhook   : [saved to bot.py]
echo     Superuser : !SUPERUSER_ID!
echo     P4 Pass   : [saved to bot.py]
echo     Autostart : %STARTUP_FOLDER%\startup.bat
echo     Service   : Perforce set to Automatic
echo.
echo   A SYSTEM RESTART is required for all changes to take effect.
echo.
echo  ============================================================
echo.
set /p RESTART_NOW="  Restart now? (Y/N): "
if /i "!RESTART_NOW!"=="Y" (
    echo.
    echo  Restarting in 5 seconds...
    shutdown /r /t 5
) else (
    echo.
    echo  Remember to restart manually for changes to take effect.
    echo.
    pause
)
endlocal