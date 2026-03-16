import os
import json
from .config import PROFILE_DIR

def get_metadata(name):
    path = os.path.join(PROFILE_DIR, name, "zen_manager_meta.json")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_metadata(name, data):
    path = os.path.join(PROFILE_DIR, name)
    if not os.path.exists(path):
        os.makedirs(path)
    meta_path = os.path.join(path, "zen_manager_meta.json")
    with open(meta_path, "w") as f:
        json.dump(data, f)

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