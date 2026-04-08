# AI Programming Tool - Environment Setup Guide

## Prerequisites

- **Python 3.8 or higher** (required)
- **pip** (Python package manager)
- **Qt5 libraries** (installed automatically via PyQt5)

## Quick Start

### Option 1: Automated Setup (Recommended)

#### Linux/macOS
```bash
chmod +x setup_environment.sh
./setup_environment.sh
```

#### Windows
```cmd
setup_environment.bat
```

### Option 2: Manual Setup

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate virtual environment:**
   
   **Linux/macOS:**
   ```bash
   source venv/bin/activate
   ```
   
   **Windows:**
   ```cmd
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python ai_programming_tool.py
   ```

## Platform-Specific Instructions

### Ubuntu/Debian Linux

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv python3-pyqt5

# Then follow manual setup steps above
```

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and PyQt5
brew install python pyqt

# Then follow manual setup steps above
```

### Windows

1. Download and install Python 3.8+ from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Open Command Prompt and follow manual setup steps

## Running the Application

After setup is complete:

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Run the application
python ai_programming_tool.py
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Space` | Generate AI code suggestion |
| `Ctrl+Enter` | Accept AI suggestion |
| `Esc` | Reject AI suggestion |
| `Ctrl+N` | New file |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save file |
| `Ctrl+Q` | Quit application |

## Troubleshooting

### Common Issues

**1. PyQt5 import error:**
```bash
# Reinstall PyQt5
pip uninstall PyQt5
pip install PyQt5==5.15.9
```

**2. Display issues on Linux:**
```bash
# Install Qt5 platform plugins
sudo apt-get install -y qt5-qpa-plugins
```

**3. Permission errors on macOS/Linux:**
```bash
# Make scripts executable
chmod +x setup_environment.sh
```

**4. Virtual environment activation fails:**
- Ensure you're in the correct directory
- Check that `venv` folder exists
- Try recreating the virtual environment

## Uninstallation

To remove the virtual environment and all dependencies:

```bash
# Deactivate if active
deactivate

# Remove virtual environment folder
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

## Development Mode

For developers who want to contribute:

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest pytest-qt

# Run tests
pytest
```

## Additional Resources

- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Qt for Python](https://doc.qt.io/qtforpython/)
- [Pygments Documentation](https://pygments.org/docs/)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the application logs in the terminal output
3. Verify your Python version meets requirements (3.8+)
