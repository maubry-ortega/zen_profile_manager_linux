# VolleyDevByMaubry [6/∞] - Núcleo del sistema
# "La estabilidad del sistema es el silencio de la armonía técnica."

import os

def is_running(profile_path):
    # Zen/Firefox use these lock files on Linux
    lock_files = [
        os.path.join(profile_path, "lock"),
        os.path.join(profile_path, "parent.lock"),
        os.path.join(profile_path, ".parentlock")
    ]
    for lock in lock_files:
        if os.path.exists(lock):
            return True
    return False

def remove_locks(profile_path):
    import glob
    for lock_file in glob.glob(os.path.join(profile_path, "lock")) + \
                    glob.glob(os.path.join(profile_path, "parent.lock")) + \
                    glob.glob(os.path.join(profile_path, ".parentlock")):
        try:
            os.remove(lock_file)
        except FileNotFoundError:
            pass
