# VolleyDevByMaubry [19/∞] - Núcleo de respaldo
# "Preservar el pasado es asegurar la continuidad del futuro."

import os
import shutil
import zipfile
from .profiles import get_profile_dir

def create_backup(profile_name, dest_path):
    profile_path = os.path.join(get_profile_dir(), profile_name)
    if not os.path.exists(profile_path):
        return False, "El perfil no existe."
    
    try:
        # Si dest_path es una carpeta, poner el nombre del zip por defecto
        if os.path.isdir(dest_path):
            dest_path = os.path.join(dest_path, f"{profile_name}_backup.zip")
            
        with zipfile.ZipFile(dest_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(profile_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, profile_path)
                    zipf.write(file_path, arcname)
        return True, dest_path
    except Exception as e:
        return False, str(e)

def import_profile(zip_path, new_profile_name):
    target_path = os.path.join(get_profile_dir(), new_profile_name)
    if os.path.exists(target_path):
        return False, "Ya existe un perfil con ese nombre."
    
    try:
        os.makedirs(target_path, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(target_path)
        return True, target_path
    except Exception as e:
        # Limpiar si falla
        if os.path.exists(target_path):
            shutil.rmtree(target_path)
        return False, str(e)
