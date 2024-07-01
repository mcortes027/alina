import subprocess
import time
import config as cfg
import os 
import sys
import platform

"""
    This script is an environment selector which takes the environment to deploy in as a command-line argument.
    It assigns the necessary environment variables based on the selected environment and then runs docker-compose up -d command.
    After that, it waits for 20 seconds and then runs docker exec command to pull the latest version of 'llama3' image.
"""
try:
    entorno = sys.argv[1:][0] 
    print(f"Se ha detectado el entorno: {entorno}")
    variables_entorno = cfg.entornos[entorno]
    
    # Set environment variables using setx on Windows
    if platform.system() == 'Windows':
        subprocess.run(["setx", "VOLUMEN_CHROMADB", variables_entorno['volumen_chromadb']], check=True)
        subprocess.run(["setx", "VOLUMEN_OLLAMA", variables_entorno['volumen_ollama']], check=True)
        subprocess.run(["setx", "VOLUMEN_MYSQL", variables_entorno['volumen_mysql']], check=True)
        subprocess.run(["setx", "VOLUMEN_BACKUPS", variables_entorno['volumen_backups']], check=True)
        subprocess.run(["setx", "VOLUMEN_CODE", variables_entorno['volumen_code']], check=True)
        subprocess.run(["setx", "VOLUMEN_AUDIO", variables_entorno['volumen_audio']], check=True)
    else:
        os.environ['VOLUMEN_CHROMADB'] = variables_entorno['volumen_chromadb']
        os.environ['VOLUMEN_OLLAMA'] = variables_entorno['volumen_ollama']
        os.environ['VOLUMEN_MYSQL'] = variables_entorno['volumen_mysql']
        os.environ['VOLUMEN_BACKUPS'] = variables_entorno['volumen_backups']
        os.environ['VOLUMEN_CODE'] = variables_entorno['volumen_code']
        os.environ['VOLUMEN_AUDIO'] = variables_entorno['volumen_audio']

    print(f"Se han asignado las variables de entorno para el entorno: {entorno}")

except IndexError:
    print("Por favor recuerda pasar como argumento el nombre del entorno en el que estás desplegando")
    print("El entorno ha de estar definido en config.py")

# Run docker-compose up -d
if sys.argv[2:] != None:
    if "bajar" in sys.argv[2:]:
        print("Bajando contenedores")
        if platform.system() != 'Windows':
            subprocess.run(["docker-compose", "down"], check=True)
        else:
            subprocess.run(["docker", "compose", "down"], check=True)
        sys.exit(0)

if platform.system() != 'Windows':
    subprocess.run(["docker-compose", "up", "-d"], check=True)
else:
    subprocess.run(["docker", "compose", "up", "-d"], check=True)

# Wait for 5 seconds
time.sleep(20)

# Run docker exec
if platform.system() != 'Windows':
    subprocess.run(["docker", "exec", "-it","despliegues_ollama_1", "ollama", "pull", "llama3"], check=True)
else:
    subprocess.run(["docker", "exec", "-it","despliegues-ollama-1", "ollama", "pull", "llama3"], check=True)
