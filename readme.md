# 🛡 Public DNS Switcher (Flask Web App)

A Windows-only real-time web application built using **Flask** to change system DNS settings to popular public DNS providers like Google, Cloudflare, Quad9, etc.

> 🚨 Requires Administrator privileges to modify DNS settings on Windows.

---

## 🌐 Features

- List of public DNS providers with descriptions
- Apply selected DNS with one click
- Reset DNS to automatic (DHCP)
- View current DNS settings
- Live DNS refresh without reloading the page
- Friendly web interface using Bootstrap

---

## 📦 Requirements

- Python 3.8+
- Windows OS (only)
- Administrator access

### 🔧 Python Libraries
```bash
pip install flask
```

---

## 🚀 How to Run

### ⚡ Method 1: Run manually as Admin

1. Open `CMD` or `PowerShell` **as Administrator**
2. Navigate to the folder containing the project:
   ```bash
   cd path\to\project
   ```
3. Run the app:
   ```bash
   python main.py
   ```
4. Open your browser at: [http://localhost:5000](http://localhost:5000)

---

### ⚡ Method 2: Auto-admin `.bat` Launcher

Create a file `run_as_admin.bat`:
```bat
@echo off
powershell -Command "Start-Process python 'main.py' -Verb RunAs"
```
Then **right-click → Run as administrator**

---

## 📁 File Structure
```
📦dns-switcher
├── main.py                 # Flask app
├── dns_provider.py         # List of DNS providers
├── index.html              # Frontend template (Bootstrap)
├── run_as_admin.bat        # Optional launcher
├── README.md               # Project info
```

---

## 🔒 Admin Detection

If the app is not run as administrator, it will show a clear red alert:
```
❌ Please run this server as Administrator to apply/reset DNS settings.
```

---

## 📬 To-Do / Next Features
- Package as `.exe` with auto-elevation using `pyinstaller`
- System tray interface
- Dark mode UI
- Platform-independent version (Linux, macOS)

---

## 🙌 Credits
Built by Om using Python + Flask + Bootstrap 💻

