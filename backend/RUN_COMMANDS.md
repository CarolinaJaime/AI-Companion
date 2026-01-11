# How to Run - Exact Commands

## The Problem

If you see: `source: no such file or directory: venv/bin/activate`

It means you're **not in the correct directory**. Here are the exact commands to run:

## Solution: Use Full Path or Navigate First

### Option 1: Navigate to the backend directory first (Recommended)

```bash
cd /Users/fionaluo/AI-Companion/backend
source venv/bin/activate
python main.py
```

### Option 2: Use absolute path to activate

```bash
source /Users/fionaluo/AI-Companion/backend/venv/bin/activate
cd /Users/fionaluo/AI-Companion/backend
python main.py
```

### Option 3: Use the run script (Easiest)

```bash
cd /Users/fionaluo/AI-Companion/backend
./run.sh
```

Or with full path:
```bash
bash /Users/fionaluo/AI-Companion/backend/run.sh
```

### Option 4: Run directly with venv Python (No activation needed)

```bash
cd /Users/fionaluo/AI-Companion/backend
venv/bin/python main.py
```

## Check Your Current Directory

First, check where you are:
```bash
pwd
```

You should see: `/Users/fionaluo/AI-Companion/backend`

If you see something else, navigate there first:
```bash
cd /Users/fionaluo/AI-Companion/backend
```

## Verify Virtual Environment Exists

Check if venv exists:
```bash
ls -la /Users/fionaluo/AI-Companion/backend/venv/bin/activate
```

This should show the activate file. If it doesn't exist, you need to install dependencies first.

## Complete Step-by-Step

```bash
# 1. Navigate to backend directory
cd /Users/fionaluo/AI-Companion/backend

# 2. Verify you're in the right place
pwd
# Should show: /Users/fionaluo/AI-Companion/backend

# 3. Check venv exists
ls venv/bin/activate
# Should show: venv/bin/activate

# 4. Activate virtual environment
source venv/bin/activate

# 5. You should see (venv) in your prompt now
# Your prompt should look like: (venv) username@hostname backend %

# 6. Run the application
python main.py
```

## Quick One-Liner

If you want to run it from anywhere without activation:

```bash
/Users/fionaluo/AI-Companion/backend/venv/bin/python /Users/fionaluo/AI-Companion/backend/main.py
```

## Troubleshooting

### "No such file or directory: venv/bin/activate"
- **Fix:** Make sure you're in `/Users/fionaluo/AI-Companion/backend` directory
- **Check:** Run `pwd` to see your current directory
- **Solution:** `cd /Users/fionaluo/AI-Companion/backend` first

### "venv/bin/activate: No such file or directory"
- **Fix:** The virtual environment might not be created
- **Solution:** Run `python3 -m venv venv` in the backend directory

### "command not found: python"
- **Fix:** You're not using the virtual environment's Python
- **Solution:** Make sure you activated venv: `source venv/bin/activate`
- **Check:** Run `which python` - should show `.../backend/venv/bin/python`

## Copy-Paste Ready Command

For the quickest start, copy and paste this:

```bash
cd /Users/fionaluo/AI-Companion/backend && source venv/bin/activate && python main.py
```

This will:
1. Navigate to the correct directory
2. Activate the virtual environment
3. Run the application
