# VolleyDevByMaubry [13/∞] - Utilidad de registro
# "Recordar es la base para entender el presente y prever el futuro."

import time

def log(message, level="INFO"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def error(message):
    log(message, level="ERROR")
