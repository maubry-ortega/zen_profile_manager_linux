# VolleyDevByMaubry [8/∞] - Servicio de actualizaciones
# "Evolucionar es la única constante en el flujo del tiempo digital."

import subprocess
import threading
from ..core import browser
from ..constants import ZEN_INSTALL_SCRIPT
from ..config import ZEN_BINARY

def run_update_async(callback=None):
    def run_update():
        try:
            print("Iniciando actualización de Zen Browser...")
            cmd = f"curl -fsSL {ZEN_INSTALL_SCRIPT} | bash"
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                print("Actualización completada con éxito.")
                if callback: callback(True)
            else:
                print(f"Error en la actualización: {stderr}")
                if callback: callback(False)
        except Exception as e:
            print(f"Error al ejecutar script de actualización: {str(e)}")
            if callback: callback(False)

    thread = threading.Thread(target=run_update)
    thread.start()
    return thread

def check_version():
    return browser.get_version(ZEN_BINARY)
