# Quick Start Guide

## ✅ Installation Complete!

All packages have been installed successfully in the virtual environment.

## Running the Application

### Quick Start (3 Steps)

1. **Activate virtual environment:**
   ```bash
   cd backend
   source venv/bin/activate
   ```

2. **Grant camera permissions** (macOS only):
   - System Preferences > Security & Privacy > Privacy > Camera
   - Enable access for Terminal

3. **Run the application:**
   ```bash
   python main.py
   ```

Or use the run script:
```bash
cd backend
./run.sh
```

## Fixing "python: command not found" Error

On macOS, Python 3 is typically installed as `python3`, not `python`. Here are the solutions:

### Solution 1: Configure Code Runner (VS Code Extension)

I've created a `.vscode/settings.json` file that configures Code Runner to use `python3`. 

**After creating this file, you may need to:**
1. Reload VS Code window: `Cmd+Shift+P` → "Reload Window"
2. Or restart VS Code

### Solution 2: Use Terminal Directly

Instead of using Code Runner, run from terminal:

```bash
cd backend
python3 main.py
```

### Solution 3: Use the Run Script

I've created a convenient run script:

```bash
cd backend
./run.sh
```

Or:

```bash
bash backend/run.sh
```

### Solution 4: Create a python alias (Optional)

If you want `python` to work, you can create an alias in your shell config:

```bash
# Add to ~/.zshrc (or ~/.bash_profile on older macOS)
alias python=python3
alias pip=pip3
```

Then reload your shell:
```bash
source ~/.zshrc
```

## Running the Focus Tracker

Once the Python issue is fixed:

1. **Install dependencies** (if not already done):
   ```bash
   cd backend
   python3 -m pip install -r requirements.txt
   ```

2. **Test camera**:
   ```bash
   python3 test_camera.py
   ```

3. **Run the application**:
   ```bash
   python3 main.py
   ```

## Troubleshooting

### Code Runner still uses `python`?

1. Check that `.vscode/settings.json` exists in your workspace root
2. Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"
3. Try running the file again with Code Runner (right-click → "Run Code" or use the play button)

### Still having issues?

Run from terminal - it's the most reliable method:
```bash
cd /Users/fionaluo/AI-Companion/backend
python3 main.py
```
