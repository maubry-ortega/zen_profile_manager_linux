# Zen Profile Manager

Zen Profile Manager es una aplicación para gestionar perfiles de configuración en entornos Linux de manera sencilla y eficiente. Permite crear, modificar, activar y eliminar perfiles personalizados para adaptar tu entorno de trabajo rápidamente según tus necesidades.

## Características principales
- Gestión de múltiples perfiles de configuración.
- Interfaz gráfica intuitiva y fácil de usar.
- Permite alternar entre perfiles con un solo clic.
- Ideal para usuarios que requieren diferentes entornos de trabajo (desarrollo, oficina, gaming, etc.).

## Instalación y uso en Linux

1. **Clona o descarga este repositorio en tu equipo.**

2. **Copia el archivo de escritorio para integrarlo en tu sistema:**

```sh
cp /home/maubry/Desktop/zen_profile_manager/zen-profile-manager.desktop ~/.local/share/applications/
```

3. **Actualiza la base de datos de aplicaciones:**

```sh
update-desktop-database ~/.local/share/applications/
```

4. **Busca "Zen Profile Manager" en tu menú de aplicaciones y ejecútalo.**

## Requisitos
- Python 3.8 o superior
- Las dependencias listadas en `requirements.txt` (puedes instalarlas con `pip install -r requirements.txt`)

## Ejecución manual

Si prefieres ejecutar la aplicación desde la terminal:

```sh
python3 main.py
```

## Autor
Desarrollado con pasión por **VolleyDevByMaubry**.

¡Disfruta de una gestión de perfiles más zen y eficiente!
