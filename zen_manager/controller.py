# VolleyDevByMaubry [5/∞] - Controlador de acciones
# "Entre el clic del usuario y el navegador, el controlador es quien toma la decisión."

import subprocess
import shutil
import os
import glob
from .config import ZEN_BINARY, ZEN_FLATPAK_ID, PROFILE_DIR

def launch_browser(profile_name):
    path = os.path.join(PROFILE_DIR, profile_name)
    
    # Crear el directorio del perfil si no existe
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        
        # Eliminar cualquier archivo de bloqueo residual
        for lock_file in glob.glob(os.path.join(path, "lock")) + glob.glob(os.path.join(path, "parent.lock")):
            os.remove(lock_file)
        
        # Verificar permisos de escritura
        test_file = os.path.join(path, "test_write")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        
        print(f"Lanzando Zen con perfil en: {path}")
        
        # Lanzar el navegador con formato explícito
        cmd = [
            ZEN_BINARY, "run", ZEN_FLATPAK_ID,
            f"--user-data-dir={path}",
            "--no-first-run",
            "--no-remote",
            "--new-instance",
            "--profile", path  # Parámetro adicional para forzar el perfil
        ]
        print(f"Ejecutando comando: {' '.join(cmd)}")
        
        # Capturar salida para depuración
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=5)
        if stderr:
            print(f"Error de Flatpak: {stderr}")
        if stdout:
            print(f"Salida de Flatpak: {stdout}")
            
    except PermissionError:
        raise Exception(f"No se tienen permisos para escribir en {path}")
    except subprocess.TimeoutExpired:
        print("El proceso de Flatpak no respondió en 5 segundos, pero puede estar ejecutándose.")
    except Exception as e:
        raise Exception(f"Error al lanzar el navegador: {str(e)}")