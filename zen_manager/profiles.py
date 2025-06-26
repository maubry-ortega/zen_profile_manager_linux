# VolleyDevByMaubry [4/∞] - Lógica de perfiles
# "Administrar identidades es orquestar múltiples realidades."

import os
from .config import PROFILE_DIR

def list_profiles():
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    return sorted([d for d in os.listdir(PROFILE_DIR) if os.path.isdir(os.path.join(PROFILE_DIR, d))])

def create_profile(name):
    path = os.path.join(PROFILE_DIR, name)
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

def delete_profile(name):
    path = os.path.join(PROFILE_DIR, name)
    if os.path.exists(path):
        import shutil
        shutil.rmtree(path)
        return True
    return False

def rename_profile(old, new):
    old_path = os.path.join(PROFILE_DIR, old)
    new_path = os.path.join(PROFILE_DIR, new)
    if os.path.exists(old_path) and not os.path.exists(new_path):
        os.rename(old_path, new_path)
        return True
    return False