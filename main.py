# Flask-based real-time Web DNS Switcher (Windows only)
from flask import Flask, render_template, request, redirect, url_for, flash
import subprocess
import os
from dns_provider import dns_list

app = Flask(__name__, template_folder='')
app.secret_key = "supersecretkey"

# ------------------------- DNS Actions ----------------------------

def get_network_interfaces():
    interfaces = []
    try:
        output = subprocess.check_output("netsh interface show interface", shell=True, text=True)
        for line in output.splitlines():
            if "Connected" in line or "enabled" in line.lower():
                parts = line.split()
                if parts:
                    interfaces.append(parts[-1])
    except Exception as e:
        print("Interface error:", e)
    return interfaces

def set_dns(dns1, dns2):
    try:
        interfaces = get_network_interfaces()
        for iface in interfaces:
            subprocess.call(f'netsh interface ip set dns name="{iface}" source=static addr={dns1}', shell=True)
            subprocess.call(f'netsh interface ip add dns name="{iface}" addr={dns2} index=2', shell=True)
        return True
    except Exception as e:
        print("DNS switch error:", e)
        return False

def reset_dns():
    try:
        interfaces = get_network_interfaces()
        for iface in interfaces:
            subprocess.call(f'netsh interface ip set dns name="{iface}" source=dhcp', shell=True)
        return True
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
    success = set_dns(dns1, dns2)
    if success:
        flash(f"Successfully applied DNS: {dns1}, {dns2}", "success")
    else:
        flash("Failed to apply DNS. Run server as Administrator.", "danger")
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    success = reset_dns()
    if success:
        flash("DNS reset to automatic (DHCP)", "info")
    else:
        flash("Failed to reset DNS.", "danger")
    return redirect(url_for("index"))

@app.route("/refresh-dns")
def refresh_dns():
    current_dns = get_current_dns()
    return {"dns": current_dns}

# ------------------------- Run ----------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)
