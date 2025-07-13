# Flask-based real-time Web DNS Switcher (Windows only)
from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import threading
import time
import sys
import os
from dns_provider import dns_list
import webbrowser

app = Flask(__name__, template_folder='')
app.secret_key = "supersecretkey"

# ------------------------- DNS Actions ----------------------------

def get_network_interfaces():
    interfaces = []
    try:
        output = subprocess.check_output("netsh interface show interface", shell=True, text=True)
        lines = output.splitlines()
        for line in lines:
            if line.strip().startswith("Enabled") or "Connected" in line:
                parts = line.strip().split()
                if len(parts) >= 4:
                    # Interface name starts after the 3rd token (Admin, State, Type)
                    iface = " ".join(parts[3:])
                    interfaces.append(iface.strip('"'))
    except Exception as e:
        print("Interface error:", e)
    return interfaces


def set_dns(dns1, dns2):
    try:
        interfaces = get_network_interfaces()
        for iface in interfaces:
            subprocess.check_call(f'netsh interface ip set dns name="{iface}" source=static addr={dns1}', shell=True)
            subprocess.check_call(f'netsh interface ip add dns name="{iface}" addr={dns2} index=2', shell=True)
        return True
    except subprocess.CalledProcessError as e:
        if "elevation" in str(e).lower():
            raise PermissionError("Admin rights required.")
        print("DNS switch error:", e)
        return False
    except Exception as e:
        print("DNS switch error:", e)
        return False

def reset_dns():
    try:
        interfaces = get_network_interfaces()
        for iface in interfaces:
            subprocess.check_call(f'netsh interface ip set dns name="{iface}" source=dhcp', shell=True)
        return True
    except subprocess.CalledProcessError as e:
        if "elevation" in str(e).lower():
            raise PermissionError("Admin rights required.")
        print("Reset error:", e)
        return False
    except Exception as e:
        print("Reset error:", e)
        return False

def get_current_dns():
    try:
        output = subprocess.check_output("ipconfig /all", shell=True, text=True)
        lines = output.splitlines()
        dns_servers = []
        capture = False

        for line in lines:
            if "DNS Servers" in line:
                capture = True
                dns_servers.append(line.strip())
            elif capture:
                if line.startswith("   ") or line.startswith("\t"):
                    dns_servers.append(line.strip())
                else:
                    capture = False
        return dns_servers
    except Exception as e:
        print("DNS read error:", e)
        return []

# ------------------------- Routes ----------------------------

@app.route("/")
def index():
    current_dns = get_current_dns()
    return render_template("index.html", dns_list=dns_list, current_dns=current_dns)

@app.route("/apply", methods=["POST"])
def apply_dns():
    dns1 = request.form.get("dns1")
    dns2 = request.form.get("dns2")
    try:
        success = set_dns(dns1, dns2)
        if success:
            flash(f"Successfully applied DNS: {dns1}, {dns2}", "success")
        else:
            flash("Failed to apply DNS. Unknown error.", "danger")
    except PermissionError:
        flash("❌ Please run this server as Administrator to apply DNS settings.", "danger")
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    try:
        success = reset_dns()
        if success:
            flash("DNS reset to automatic (DHCP)", "info")
        else:
            flash("Failed to reset DNS.", "danger")
    except PermissionError:
        flash("❌ Please run this server as Administrator to reset DNS.", "danger")
    return redirect(url_for("index"))

@app.route("/refresh-dns")
def refresh_dns():
    current_dns = get_current_dns()
    return {"dns": current_dns}

@app.route("/quit")
def quit_server():
    def shutdown():
        try:
            print("[INFO] Resetting DNS before shutdown...")
            reset_dns()
        except Exception as e:
            print("[ERROR] Failed to reset DNS on quit:", e)
        time.sleep(1.5)  # Let the response render
        os._exit(0)      # Kill the server and terminal

    threading.Thread(target=shutdown).start()
    return "👋 Resetting DNS and shutting down the server. You may close the browser and terminal."



# ------------------------- Run ----------------------------

if __name__ == "__main__":
    webbrowser.open("http://localhost:5000")
    app.run(debug=True, port=5000)