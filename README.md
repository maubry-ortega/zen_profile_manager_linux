# 🧘‍♂️ Zen Profile Manager

Zen Profile Manager es una herramienta elegante y minimalista desarrollada en Python y GTK 3 diseñada para gestionar perfiles de **Zen Browser** de forma eficiente.

## ✨ Características
- **Interfaz "Zen"**: Diseño moderno inspirado en Tokyo Night, limpio y sin distracciones.
- **Vista en Cuadrícula**: Navega por tus perfiles de forma visual con iconos personalizados.
- **Personalización Total**: Asocia imágenes propias a cada perfil desde el gestor.
- **Indicador en Tiempo Real**: Visualiza instantáneamente qué perfiles están abiertos (borde verde brillante).
- **Actualización Integrada**: Actualiza Zen Browser a la última versión con un solo clic desde la cabecera.
- **Interacción Ágil**: Lanza perfiles con la tecla **Enter** para un flujo de trabajo rápido.

## 🚀 Instalación y Uso

### 1. Requisitos
- Python 3.10+
- GTK 3 (PyGObject)
- Curl (para actualizaciones automáticas)

### 2. Configuración
Clona el repositorio e instala las dependencias:
```bash
git clone https://github.com/maubry-ortega/zen_profile_manager_linux.git
cd zen_profile_manager_linux
pip install -r requirements.txt
```

### 3. Ejecución
```bash
python main.py
```

## 📂 Estructura del Proyecto
- `zen_manager/ui.py`: Ventana principal y lógica de la interfaz.
- `zen_manager/components.py`: Componentes visuales reutilizables (Tarjetas).
- `zen_manager/dialogs.py`: Ventanas modales para creación y edición.
- `zen_manager/controller.py`: Lógica de sistema y ejecución del navegador.
- `zen_manager/profiles.py`: Gestión de archivos y metadatos de perfiles.
- `zen_manager/style.css`: Estilos personalizados (CSS).

## 🛠️ Desarrollo y CI/CD
Consulta los archivos `ARCHITECTURE.md` para detalles técnicos y `CI_CD.md` para guías de despliegue multiplataforma.

## ✒️ Autor
Desarrollado con pasión por **VolleyDevByMaubry**.
*"Donde el orden nace del conocimiento compartido."*
