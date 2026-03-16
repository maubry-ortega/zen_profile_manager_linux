# Zen Profile Manager - Architecture Overview

This project is a GTK-based profile manager for the Zen Browser, designed with a focus on minimalism, UX, and modularity.

## Core Flow

1.  **Entry Point**: `main.py` initializes the GTK application and handles the main event loop.
2.  **UI Layer (`zen_manager/ui.py`)**: Defines the main window and orchestrates the layout.
    - **Components (`zen_manager/components.py`)**: Reusable widgets like the `ProfileCard`.
    - **Dialogs (`zen_manager/dialogs.py`)**: Modal windows for profile creation and customization.
    - **Styling (`zen_manager/style.css`)**: Modern dark theme with custom classes.
3.  **Controller Layer (`zen_manager/controller.py`)**: Bridges the UI and the system logic.
    - Handles browser execution, version checking, and update scripts.
4.  **Profile Logic (`zen_manager/profiles.py`)**: Manages the filesystem interactions for profile directories and metadata.

## Data Management
- **Profiles**: Stored in `~/.zen/profiles/` (configurable).
- **Metadata**: Each profile has a `zen_manager_meta.json` file inside its directory to store custom images and settings.

## Execution Model
- **Non-blocking**: Browser updates and launches run in background threads or processes to keep the UI responsive.
- **Polling**: A timer in the UI checks every 2 seconds for lock files to indicate which profiles are running.
