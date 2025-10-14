# Instructor Setup Guide

## Overview

This project template is configured to automatically set up Python virtual environments for students using VSCode. The setup mimics the IDX Firebase script functionality but works in any VSCode environment.

## What Was Added

### 1. `.vscode/settings.json`
Configures VSCode to:
- Use the correct Python interpreter from `.venv`
- Auto-activate the virtual environment in terminals
- Support multiple operating systems (macOS, Linux, Windows)

### 2. `.vscode/terminal-init.sh`
Bash/Zsh initialization script that:
- Sources the appropriate shell configuration
- Defines helpful aliases (`setup-venv`, `activate`)
- Automatically activates the virtual environment if it exists
- Shows helpful messages to students

### 3. `.vscode/terminal-init.ps1`
PowerShell initialization script for Windows users with the same functionality.

### 4. `setup.sh` (Optional)
A setup script that adds aliases to the user's shell configuration file (`.bashrc` or `.zshrc`).
This is optional since the VSCode terminal configuration handles everything automatically.

### 5. `.gitignore`
Properly configured to exclude:
- Virtual environments (`.venv/`)
- Python cache files (`__pycache__/`, `*.pyc`)
- IDE settings (except the ones we want to keep)
- OS-specific files (`.DS_Store`, `Thumbs.db`)

## How It Works

### For Students:

1. **Clone/Open the project** in VSCode
2. **Open a new terminal** - it will automatically detect if `.venv` exists
3. **If no virtual environment exists**, they'll see:
   ```
   💡 No virtual environment found. Run 'setup-venv' to create one!
   ```
4. **Run `setup-venv`** - this will:
   - Create the virtual environment
   - Activate it
   - Upgrade pip
   - Install all packages from `requirements.txt`
5. **All future terminals** will automatically activate the virtual environment!

### Commands Available in VSCode Terminals:

- `setup-venv` - Create virtual environment and install all requirements
- `activate` - Manually activate the virtual environment (if needed)

## Testing the Setup

To test if everything works:

```bash
# Open a new terminal in VSCode
# You should see one of these messages:
# ✅ "🐍 Virtual environment activated!" (if .venv exists)
# ✅ "💡 No virtual environment found. Run 'setup-venv' to create one!" (if no .venv)

# If no .venv exists, run:
setup-venv

# Test that packages are installed:
pip list

# Test running the code:
python main.py
```

## Cross-Platform Support

This setup works on:
- **macOS** (using zsh, the default since macOS Catalina)
- **Linux** (using bash)
- **Windows** (using PowerShell)

The VSCode settings automatically detect the OS and use the appropriate configuration.

## Troubleshooting

### Terminals don't auto-activate on macOS
- Make sure `.vscode/terminal-init.sh` has execute permissions:
  ```bash
  chmod +x .vscode/terminal-init.sh
  ```

### Commands not found (`setup-venv`, `activate`)
- Close all terminals and open a new one
- Check that `.vscode/terminal-init.sh` exists
- Verify VSCode settings are correct in `.vscode/settings.json`

### Windows PowerShell execution policy issues
Students might need to run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Differences from IDX Script

| Feature | IDX Script | This Setup |
|---------|-----------|------------|
| Auto-activation | ✅ | ✅ |
| Aliases available | ✅ | ✅ |
| Cross-platform | ❌ (Linux only) | ✅ (macOS/Linux/Windows) |
| Requires cloud IDE | ✅ | ❌ |
| Works offline | ❌ | ✅ |
| Git-friendly | ✅ | ✅ |

## Distributing to Students

When sharing this template:

1. **Push to GitHub/GitLab** with all the `.vscode` files included
2. Students simply **clone the repository**
3. Students **open in VSCode**
4. Students **open a terminal** and follow the instructions

That's it! No manual setup required.

## Updating Requirements

When you add new packages:

1. Update `requirements.txt`
2. Students run: `pip install -r requirements.txt`
   
Or they can delete `.venv` and run `setup-venv` again to start fresh.

## Notes

- The `.vscode` folder is included in git (via `.gitignore` exceptions) so students get the configuration automatically
- The `.venv` folder is excluded from git to keep repositories clean
- Students can use IDEs other than VSCode, but they'll need to manually create/activate the virtual environment

