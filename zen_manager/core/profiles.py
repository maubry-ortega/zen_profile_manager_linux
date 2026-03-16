# VolleyDevByMaubry [4/∞] - Núcleo de perfiles
# "Administrar identidades es orquestar múltiples realidades."

import os
import json
import shutil
from ..constants import DEFAULT_PROFILE_DIR, META_FILENAME

def get_profile_dir():
    # En el futuro esto podría leerse de una config editable
    return DEFAULT_PROFILE_DIR

def get_metadata(name):
    path = os.path.join(get_profile_dir(), name, META_FILENAME)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_metadata(name, data):
    path = os.path.join(get_profile_dir(), name)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    meta_path = os.path.join(path, META_FILENAME)
    with open(meta_path, "w") as f:
        json.dump(data, f)

def list_profiles():
    base_dir = get_profile_dir()
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)
    
    # Listar carpetas que no empiecen por punto
    return [d for d in os.listdir(base_dir) 
            if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith(".")]

def create_profile(name):
    path = os.path.join(get_profile_dir(), name)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        return True
    return False

def delete_profile(name):
    path = os.path.join(get_profile_dir(), name)
    if os.path.exists(path):
        shutil.rmtree(path)
        return True
    return False
