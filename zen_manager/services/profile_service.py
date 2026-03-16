# VolleyDevByMaubry [7/∞] - Servicio de perfiles
# "El servicio es el puente que conecta la intención con la acción."

import os
from ..core import profiles, browser, system
from ..config import ZEN_BINARY

def launch_profile(name):
    path = os.path.join(profiles.get_profile_dir(), name)
    
    # Asegurar que el directorio existe
    profiles.create_profile(name)
    
    # Limpiar bloqueos previos
    system.remove_locks(path)
    
    # Lanzar
    return browser.launch(ZEN_BINARY, path)

def is_active(name):
    path = os.path.join(profiles.get_profile_dir(), name)
    return system.is_running(path)
