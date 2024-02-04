import os
import platform   # Access to underlying platform’s data
import socket     # Socket interface for network programming
import subprocess # Run shell commands from Python
import psutil     # Retrieve information on system utilization (CPU, memory, disks, network, sensors)
import speedtest  # Measure internet speedk
import json
import subprocess

# 1] All Installed software’s listtk
def installed_software():
    # Get a list of all installed software using Windows Management Instrumentation (WMI)
    installed_software = subprocess.check_output(['wmic', 'product', 'get', 'name']).decode('utf-8')
    return installed_software


# 2] Internet Speed  
def internet_speed():
    try:
        speed_result = subprocess.check_output(['speedtest', '--json']).decode('utf-8')
        speed_data = json.loads(speed_result)
        download_speed = speed_data['download'] / 10**6  #  # Convert download speed to Mbps
        upload_speed = speed_data['upload'] / 10**6  # Convert upload speed to Mbps
        return f"Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps"
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return "Internet Speed: Unable to retrieve speed information"

# 3] Screen resolvution  
def screen_resolution():
    # Get screen resolution using the 'screeninfo' library
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        return f"Screen Resolution: {monitors[0].width}x{monitors[0].height}"
    except ImportError:
        return "Screen Resolution: Library 'screeninfo' not installed"

# 4] CPU model  
def cpu_info():
    cpu_info = f"CPU Model: {platform.processor()}\n"
    cpu_info += f"Cores: {psutil.cpu_count(logical=False)}, Threads: {psutil.cpu_count(logical=True)}"
    return cpu_info

# 6]GPU model 
def gpu_info():
    # Get GPU information using the 'GPUtil' library
    try:
        import GPUtil
        gpu_info = GPUtil.getGPUs()
        if gpu_info:
            return f"GPU Model: {gpu_info[0].name}"
        else:
            return "No GPU found"
    except ImportError:
       return "GPU Model: Library 'GPUtil' not installed"

# 7] RAM Size ( In GB )
def ram_size():
    ram_size = psutil.virtual_memory().total / (1024**3)  # in GB
    return f"RAM Size: {ram_size:.2f} GB"

# 8] Screen size ( like, 15 inch, 21 inch)
def screen_size():
    # Get screen size in inches using the 'screeninfo' library
    try:
        from screeninfo import get_monitors
        monitors = get_monitors()
        if monitors:
            return f"Screen Size: {monitors[0].width} inch"
        else:
            return "Screen Size: Unknown"
    except ImportError:
        return "Screen Size: Library 'screeninfo' not installed"

# 9] Wifi/Ethernet mac address
def mac_address():
    # Get MAC address of WiFi or Ethernet interface
    for interface, snic in psutil.net_if_addrs().items():
        for addr in snic:
            if addr.family == socket.AF_LINK:
                return f"MAC Address: {addr.address}"
    return "MAC Address: Not Found"

# 10] Public IP address
def public_ip():
    # Get public IP address using an external service
    try:
        public_ip = socket.gethostbyname(socket.gethostname())
        return f"Public IP Address: {public_ip}"
    except socket.gaierror:
        return "Public IP Address: Not Found"

# 11] Windows version
def windows_version():
    windows_version = platform.platform()
    return f"Windows Version: {windows_version}"


if __name__ == "__main__":
    results = [
        installed_software(),
        internet_speed(),
        screen_resolution(),
        cpu_info(),
        gpu_info(),
        ram_size(),
        screen_size(),
        mac_address(),
        public_ip(),
        windows_version()
    ]

    for result in results:
        print(result)

    # Optionally, save results to a text file or display in a GUI