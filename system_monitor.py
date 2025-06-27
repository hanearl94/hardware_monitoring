import platform
import getpass
import subprocess
import psutil
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_cpu_usage():
    return psutil.cpu_percent(interval=1, percpu=True)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.total, mem.used, mem.available, mem.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.total, disk.used, disk.free, disk.percent

def get_network_usage():
    net = psutil.net_io_counters()
    return net.bytes_sent, net.bytes_recv

def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def get_system_info():
    username = getpass.getuser()
    os_version = platform.platform()
    model_number = "Unknown"

    if platform.system() == "Darwin":  # macOS
        try:
            output = subprocess.check_output(["system_profiler", "SPHardwareDataType"]).decode()
            model_number = output.strip()
        except Exception as e:
            model_number = f"Error: {e}"
    elif platform.system() == "Windows":
        try:
            output = subprocess.check_output(["wmic", "csproduct", "get", "name"]).decode().split('\n')
            model_number = output[1].strip()
        except Exception as e:
            model_number = f"Error: {e}"

    return username, os_version, model_number

def display_system_info():
    username, os_version, model_number = get_system_info()
    print("=== System Information ===")
    print(f"User: {username}")
    print(f"OS Version: {os_version}")
    print("Model Info:\n")
    print(model_number)
    print("\n")

def monitor_resources():
    clear_screen()
    print("=== System Resource Monitor ===\n")

    cpu = get_cpu_usage()
    print("CPU Usage per Core:")
    for i, usage in enumerate(cpu):
        print(f"  Core {i}: {usage}%")

    total, used, available, percent = get_memory_usage()
    print(f"\nMemory Usage: {percent}%")
    print(f"  Total: {format_bytes(total)}")
    print(f"  Used: {format_bytes(used)}")
    print(f"  Available: {format_bytes(available)}")

    d_total, d_used, d_free, d_percent = get_disk_usage()
    print(f"\nDisk Usage: {d_percent}%")
    print(f"  Total: {format_bytes(d_total)}")
    print(f"  Used: {format_bytes(d_used)}")
    print(f"  Free: {format_bytes(d_free)}")

    sent, recv = get_network_usage()
    print(f"\nNetwork I/O:")
    print(f"  Sent: {format_bytes(sent)}")
    print(f"  Received: {format_bytes(recv)}")

def main():
    clear_screen()
    display_system_info()

    choice = input("Do you want to run the system monitor continuously? (y/n): ").strip().lower()
    if choice == 'y':
        try:
            while True:
                monitor_resources()
                time.sleep(3)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
    else:
        monitor_resources()
        print("\nMonitoring complete. Exiting...")

if __name__ == "__main__":
    main()
