# VolleyDevByMaubry [5/∞] - Núcleo del navegador
# "Navegar es descubrir, y descubrir es ampliar la realidad."

import subprocess
import os

def launch(binary, profile_path):
    cmd = [
        binary,
        "--no-remote",
        "--new-instance",
        "--profile", profile_path
    ]
    return subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def get_version(binary):
    try:
        result = subprocess.run([binary, "--version"], capture_output=True, text=True, check=True)
        return result.stdout.strip().replace("Mozilla Zen ", "")
    except Exception:
        return "Desconocida"
