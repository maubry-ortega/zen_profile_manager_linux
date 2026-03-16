# VolleyDevByMaubry [7/∞] - Servicio de perfiles
# "El servicio es el puente que conecta la intención con la acción."

import os
import time
from ..core import profiles, browser, system, backup
from ..config import ZEN_BINARY

def launch_profile(name):
    path = os.path.join(profiles.get_profile_dir(), name)
    profiles.create_profile(name)
    system.remove_locks(path)
    
    # Actualizar estadísticas de inicio
    meta = profiles.get_metadata(name)
    meta["last_used"] = int(time.time())
    profiles.save_metadata(name, meta)
    
    return browser.launch(ZEN_BINARY, path)

def is_active(name):
    path = os.path.join(profiles.get_profile_dir(), name)
    active = system.is_running(path)
    
    # Si está activo, sumar tiempo de uso (aproximado por el polling)
    if active:
        from ..constants import POLLING_INTERVAL_SECONDS
        meta = profiles.get_metadata(name)
        meta["usage_seconds"] = meta.get("usage_seconds", 0) + POLLING_INTERVAL_SECONDS
        profiles.save_metadata(name, meta)
        
    return active

def backup_profile(name, dest_folder):
    return backup.create_backup(name, dest_folder)

def export_profile(name, zip_path):
    return backup.create_backup(name, zip_path)

def import_from_zip(zip_path, new_name):
    return backup.import_profile(zip_path, new_name)

def get_stats(name):
    meta = profiles.get_metadata(name)
    return {
        "last_used": meta.get("last_used", 0),
        "usage_seconds": meta.get("usage_seconds", 0)
    }
