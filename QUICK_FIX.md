# Quick Fix: "import cv2 could not be resolved"

## ✅ Packages ARE Installed!

The packages are installed in your virtual environment. This is just an IDE configuration issue.

## Fast Fix (30 seconds)

**Step 1:** Press `Cmd+Shift+P` (or `Ctrl+Shift+P`)

**Step 2:** Type: `Python: Select Interpreter`

**Step 3:** Select: `./backend/venv/bin/python` 
   - OR the full path: `/Users/fionaluo/AI-Companion/backend/venv/bin/python`

**Step 4:** The import errors should disappear immediately!

## Alternative: Reload VS Code

1. Press `Cmd+Shift+P`
2. Type: `Developer: Reload Window`
3. Press Enter

VS Code should automatically detect the venv Python now.

## Verify It Worked

After selecting the interpreter:
- ✅ Look at bottom-right corner - should show Python version with "(venv)"
- ✅ Import errors should disappear
- ✅ Hover over `import cv2` - should show the package path
- ✅ Code completion should work for `cv2.*`

## If Still Not Working

Check bottom-right corner of VS Code:
- If it shows "Python 3.13.1" but NO "(venv)" label, click it and select the venv interpreter
- If it shows a different Python version, click it and select the venv interpreter

That's it! The import errors should be gone now. 🎉
