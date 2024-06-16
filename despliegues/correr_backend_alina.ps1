# Open Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
# Wait for Docker Desktop to start. Adjust the sleep time as necessary.
Start-Sleep -Seconds 30
# Execute the Python script
& python "C:\alina\despliegues\levantar.py" angela
# Prevent the PowerShell script from closing automatically
Read-Host -Prompt "Press Enter to exit"