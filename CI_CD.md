# CI/CD Guide for Zen Profile Manager

To distribute this application across Linux, Windows, and macOS, we recommend using GitHub Actions with `PyInstaller`.

## GitHub Actions Workflow (.github/workflows/build.yml)

```yaml
name: Build Cross-Platform Bundles

on: [push, pull_request]

jobs:
  build:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pyinstaller
          
      - name: Build with PyInstaller
        run: |
          # Linux/Mac
          pyinstaller --onefile --windowed --name zen-manager main.py
          # Windows
          # pyinstaller --onefile --noconsole --name zen-manager main.py
          
      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: zen-manager-${{ matrix.os }}
          path: dist/*
```

## Platform-Specific Requirements

### Linux
- Ensure `python3-gi`, `python3-gi-cairo`, and `gir1.2-gtk-3.0` are installed on the target machine.
- For the bundle, you may need to include the GTK libraries or use an AppImage/Flatpak approach for better portability.

### Windows / macOS
- **PyGObject** on non-Linux systems requires the **gvsbuild** or standard GTK binaries.
- On macOS, you might need to bundle the `GObject Introspection` data.

## Continuous Integration (CI)
- **Linting**: Add `flake8` or `ruff` to the workflow.
- **Tests**: Add `pytest` for controller and profile logic validation.
