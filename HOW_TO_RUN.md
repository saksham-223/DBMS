# 🚀 How to Run Event Management System in VS Code

## 📋 Prerequisites

### 1. Install Python
```bash
# Check if Python is installed
python --version
# or
python3 --version

# Should show: Python 3.8 or higher
```

**If not installed:**
- Download from: https://www.python.org/downloads/
- Install Python 3.8 or higher

---

### 2. Install VS Code
- Download from: https://code.visualstudio.com/
- Install Python extension in VS Code

---

## 🔧 Setup Steps (First Time Only)

### Step 1: Open Project in VS Code

**Option A: From VS Code**
```
1. Open VS Code
2. File → Open Folder
3. Navigate to: /Users/samarthchoudhary/Downloads/DBMS
4. Click "Open"
```

**Option B: From Terminal**
```bash
cd /Users/samarthchoudhary/Downloads/DBMS
code .
```

---

### Step 2: Create Virtual Environment

**Open VS Code Terminal:**
- Menu: Terminal → New Terminal
- Or press: `` Ctrl + ` `` (backtick)

**Run these commands:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in terminal prompt
```

---

### Step 3: Install Dependencies

```bash
# Make sure venv is activated (you see (venv) in prompt)
pip install -r requirements.txt
```

**Expected output:**
```
Installing collected packages: Flask, Flask-SQLAlchemy, python-dotenv, requests
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1...
```

---

### Step 4: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file if needed
code .env
```

**Your .env should contain:**
```env
SECRET_KEY=your-secret-key-here
SQLALCHEMY_DATABASE_URI=sqlite:///instance/event_management.db
```

---

### Step 5: Setup Database

```bash
# Create database and tables
python setup_database_sqlite.py
```

**Expected output:**
```
Database setup complete!
Default admin user created:
Username: admin
Email: admin@gmail.com
Password: admin123
```

---

## ▶️ Running the Application

### Method 1: Using Terminal (Recommended)

```bash
# Make sure you're in project folder
cd /Users/samarthchoudhary/Downloads/DBMS

# Activate virtual environment (if not already active)
source venv/bin/activate    # Mac/Linux
# or
venv\Scripts\activate       # Windows

# Run Flask application
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
```

---

### Method 2: Using VS Code Run Button

**Setup launch.json:**

1. Click **Run and Debug** icon (left sidebar)
2. Click **"create a launch.json file"**
3. Select **"Python"**
4. Select **"Python File"**

**Or manually create `.vscode/launch.json`:**
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "1"
            },
            "args": [
                "run",
                "--port=5001"
            ],
            "jinja": true,
            "autoReload": {
                "enable": true
            }
        }
    ]
}
```

**Then:**
1. Press **F5** or click **Start Debugging** (green play button)
2. Application will start on http://localhost:5001

---

### Method 3: Using VS Code Tasks

**Create `.vscode/tasks.json`:**
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Flask App",
            "type": "shell",
            "command": "${workspaceFolder}/venv/bin/python",
            "args": ["app.py"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        }
    ]
}
```

**Then:**
1. Terminal → Run Task
2. Select **"Run Flask App"**

---

## 🌐 Accessing the Application

### Once Server is Running:

**Open Browser and go to:**
```
http://localhost:5001
```

**Or:**
```
http://127.0.0.1:5001
```

### VS Code Shortcuts:
- **Ctrl + Click** on the URL in terminal
- Or click the **"Open in Browser"** popup

---

## 🔑 Login Credentials

### Default Admin Account
```
Username: admin
Email:    admin@gmail.com
Password: admin123
```

---

## 🛠️ VS Code Extensions (Recommended)

### Essential Extensions:

1. **Python** (Microsoft)
   - Syntax highlighting
   - Debugging support
   - IntelliSense

2. **Pylance** (Microsoft)
   - Advanced Python language support
   - Type checking

3. **SQLite** (alexcvzz)
   - View database contents
   - Run SQL queries

4. **HTML CSS Support** (ecmel)
   - HTML/CSS autocomplete
   - Class/ID suggestions

5. **Jinja** (wholroyd)
   - Jinja2 template syntax highlighting
   - Autocomplete for templates

### Install Extensions:
```
1. Click Extensions icon (left sidebar)
2. Search for extension name
3. Click "Install"
```

---

## 📂 VS Code Workspace Settings

**Create `.vscode/settings.json`:**
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "autopep8",
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "files.associations": {
        "*.html": "jinja-html"
    },
    "emmet.includeLanguages": {
        "jinja-html": "html"
    }
}
```

---

## 🐛 Debugging in VS Code

### Set Breakpoints:
1. Click left of line number (red dot appears)
2. Press **F5** to start debugging
3. Code will pause at breakpoint

### Debug Actions:
- **F5** - Continue
- **F10** - Step Over
- **F11** - Step Into
- **Shift+F11** - Step Out
- **Shift+F5** - Stop

### View Variables:
- **Variables** panel shows current values
- **Watch** panel for custom expressions
- **Call Stack** shows function calls

---

## 📁 Project Structure in VS Code

```
DBMS/
├── 📄 app.py                    ← Main Flask application
├── 📄 models.py                 ← Database models
├── 📄 config.py                 ← Configuration
├── 📄 requirements.txt          ← Dependencies
├── 📄 .env                      ← Environment variables
├── 📄 setup_database_sqlite.py  ← Database setup
│
├── 📁 templates/                ← HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── auth/
│   ├── events/
│   ├── guests/
│   └── bookings/
│
├── 📁 instance/                 ← Database folder
│   └── event_management.db
│
└── 📁 venv/                     ← Virtual environment
```

---

## 🔄 Common Workflows

### Starting Your Work Session:

```bash
# 1. Open project in VS Code
cd /Users/samarthchoudhary/Downloads/DBMS
code .

# 2. Open terminal in VS Code (Ctrl + `)

# 3. Activate virtual environment
source venv/bin/activate    # Mac/Linux
# or
venv\Scripts\activate       # Windows

# 4. Run application
python app.py

# 5. Open browser
# http://localhost:5001
```

---

### Making Changes:

```bash
# 1. Edit your files in VS Code

# 2. Save changes (Ctrl + S)

# 3. Server auto-reloads (if debug mode on)
#    Or restart manually (Ctrl + C, then python app.py)

# 4. Refresh browser to see changes
```

---

### Stopping the Server:

```bash
# In terminal where server is running:
# Press Ctrl + C

# Deactivate virtual environment:
deactivate
```

---

## ⚡ Quick Commands

### Terminal Commands:

```bash
# Activate venv
source venv/bin/activate         # Mac/Linux
venv\Scripts\activate            # Windows

# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Run application
python app.py

# Setup database
python setup_database_sqlite.py

# Deactivate venv
deactivate
```

---

## 🎨 VS Code Keyboard Shortcuts

### Essential Shortcuts:

```
Ctrl + `          - Open/Close Terminal
Ctrl + B          - Toggle Sidebar
Ctrl + P          - Quick File Open
Ctrl + Shift + P  - Command Palette
Ctrl + /          - Toggle Comment
Ctrl + F          - Find in File
Ctrl + Shift + F  - Find in All Files
F5                - Start Debugging
Ctrl + C          - Stop Server
Ctrl + S          - Save File
Alt + ↑/↓         - Move Line Up/Down
Shift + Alt + ↓   - Duplicate Line
```

---

## 🔍 Viewing Database in VS Code

### Using SQLite Extension:

1. **Install SQLite Extension**
   ```
   Extensions → Search "SQLite" → Install
   ```

2. **Open Database**
   ```
   Right-click instance/event_management.db
   → Open Database
   ```

3. **View Tables**
   ```
   SQLite Explorer panel (left sidebar)
   → Expand database
   → Click table to view data
   ```

4. **Run Queries**
   ```
   Right-click database
   → New Query
   → Write SQL
   → Run (Ctrl + Shift + Q)
   ```

---

## 📊 Monitoring Logs

### View Flask Logs in Terminal:

```
127.0.0.1 - - [15/Oct/2025 02:16:23] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [15/Oct/2025 02:16:24] "GET /events HTTP/1.1" 200 -
```

**What they mean:**
- IP address
- Timestamp
- HTTP method + URL
- Status code (200 = success)

---

## 🚨 Troubleshooting

### Issue 1: "python: command not found"
```bash
# Use python3 instead
python3 --version
python3 app.py
```

### Issue 2: "No module named flask"
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 3: "Port 5001 already in use"
```bash
# Find and kill process using port 5001
# Mac/Linux:
lsof -ti:5001 | xargs kill

# Windows:
netstat -ano | findstr :5001
taskkill /PID [PID_NUMBER] /F

# Or change port in app.py:
# app.run(debug=True, port=5002)
```

### Issue 4: "Template not found"
```bash
# Make sure you're in project root
cd /Users/samarthchoudhary/Downloads/DBMS

# Run from correct directory
python app.py
```

### Issue 5: Virtual environment not activating
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📝 Development Tips

### 1. Auto-Reload (Debug Mode)
```python
# In app.py (last line):
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```
- Changes auto-reload
- Better error messages
- Interactive debugger

### 2. Multiple Terminal Windows
```
Terminal → Split Terminal
```
- One for server
- One for commands

### 3. Quick File Navigation
```
Ctrl + P → Type filename → Enter
```

### 4. Format Code
```
Right-click → Format Document
Or: Shift + Alt + F
```

### 5. Git Integration
```
Source Control icon (left sidebar)
- View changes
- Commit changes
- Push to GitHub
```

---

## 🎯 Complete Workflow Example

### First Time Setup:
```bash
# 1. Open VS Code
code /Users/samarthchoudhary/Downloads/DBMS

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Setup database
python setup_database_sqlite.py

# 6. Run application
python app.py

# 7. Open browser
# http://localhost:5001

# 8. Login with admin/admin123
```

### Daily Development:
```bash
# 1. Open VS Code
code /Users/samarthchoudhary/Downloads/DBMS

# 2. Activate venv
source venv/bin/activate

# 3. Run app
python app.py

# 4. Start coding!
```

---

## ✅ Checklist

**Before Running:**
- [ ] Python 3.8+ installed
- [ ] VS Code installed
- [ ] Project folder opened in VS Code
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Database setup completed

**To Run:**
- [ ] Terminal opened in VS Code
- [ ] Virtual environment activated
- [ ] `python app.py` executed
- [ ] Server running on port 5001
- [ ] Browser opened to localhost:5001

**Development:**
- [ ] Extensions installed (Python, Jinja)
- [ ] launch.json configured (optional)
- [ ] Debug mode enabled
- [ ] Git initialized (optional)

---

## 🎊 You're Ready!

Your Event Management System should now be running in VS Code!

**Access at:** http://localhost:5001

**Login:** admin / admin123

**Happy Coding!** 🚀

---

## 📞 Need Help?

### Check These Files:
- `README.md` - Project overview
- `SYSTEM_ARCHITECTURE.md` - System details
- `requirements.txt` - Dependencies list

### Common Commands Reference:
```bash
# Activate venv
source venv/bin/activate

# Run app
python app.py

# Install package
pip install package-name

# Stop server
Ctrl + C
```

### VS Code Settings:
```
File → Preferences → Settings
Or: Ctrl + ,
```

---

**Everything you need to run and develop your project in VS Code!** ✨
