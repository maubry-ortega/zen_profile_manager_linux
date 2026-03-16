# VolleyDevByMaubry [5/∞] - Controlador de acciones
# "Entre el clic del usuario y el navegador, el controlador es quien toma la decisión."

import subprocess
import shutil
import os
import glob
from .config import ZEN_BINARY, PROFILE_DIR

def launch_browser(profile_name):
    # Ruta absoluta para evitar conflictos con el wrapper
    path = os.path.abspath(os.path.join(PROFILE_DIR, profile_name))
    
    # Crear el directorio del perfil si no existe
    try:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        
        # Eliminar cualquier archivo de bloqueo residual
        for lock_file in glob.glob(os.path.join(path, "lock")) + glob.glob(os.path.join(path, "parent.lock")):
            try:
                os.remove(lock_file)
            except FileNotFoundError:
                pass
        
        # Verificar permisos de escritura
        test_file = os.path.join(path, "test_write")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        
        print(f"Lanzando Zen con perfil en: {path}")
        
        # Lanzar el navegador con formato explícito
        cmd = [
            ZEN_BINARY,
            "--no-remote",
            "--new-instance",
            "--profile", path
        ]

        print(f"Ejecutando comando: {' '.join(cmd)}")
        
        # Ejecutar sin esperar a que termine, para que la instancia siga abierta
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except PermissionError:
        raise Exception(f"No se tienen permisos para escribir en {path}")
    except Exception as e:
        raise Exception(f"Error al lanzar el navegador: {str(e)}")

def get_browser_version():
    try:
        result = subprocess.run([ZEN_BINARY, "--version"], capture_output=True, text=True, check=True)
        return result.stdout.strip().replace("Mozilla Zen ", "")
    except Exception:
        return "Desconocida"

def update_browser():
    from .config import ZEN_INSTALL_SCRIPT
    import threading
    
    def run_update():
        try:
            print("Iniciando actualización de Zen Browser...")
            # Usar curl para descargar y pipear a bash (método oficial)
            cmd = f"curl -fsSL {ZEN_INSTALL_SCRIPT} | bash"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                print("Actualización completada con éxito.")
            else:
                print(f"Error en la actualización: {stderr}")
        except Exception as e:
            print(f"Error al ejecutar script de actualización: {str(e)}")

    # Ejecutar en un hilo separado para no bloquear la UI
    thread = threading.Thread(target=run_update)
    thread.start()
    return thread

def is_profile_running(profile_name):
    path = os.path.join(PROFILE_DIR, profile_name)
    # Firefox/Zen use 'lock' on Linux (and parent.lock)
    lock_files = [os.path.join(path, "lock"), os.path.join(path, "parent.lock")]
    for lock in lock_files:
        if os.path.exists(lock):
            return True
    return False
