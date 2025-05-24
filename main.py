import csv
import socket
from datetime import datetime, timedelta
from colorama import init, Fore, Style
import os

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

init(autoreset=True)

def check_ssh(ip_port, timeout=3):
    try:
        ip, port = ip_port.split(':')
        with socket.create_connection((ip, int(port)), timeout=timeout):
            return "Online"
    except (socket.timeout, socket.error, ValueError):
        return "Offline"

def get_warranty_info(warranty_flag, reg_date_str):
    if str(warranty_flag).strip() != "1":
        return Fore.YELLOW + "No Warranty"
    try:
        reg_date = datetime.strptime(reg_date_str.strip(), "%d/%m/%Y")
        warranty_end = reg_date + timedelta(days=10)
        days_left = (warranty_end - datetime.now()).days
        if days_left >= 0:
            return Fore.GREEN + f"Valid ({days_left}d left)"
        else:
            return Fore.RED + f"Expired ({abs(days_left)}d ago)"
    except Exception:
        return Fore.MAGENTA + "Unknown"

def get_expiry_info(reg_date_str):
    try:
        reg_date = datetime.strptime(reg_date_str.strip(), "%d/%m/%Y")
        expiry_date = reg_date + timedelta(days=28)
        days_left = (expiry_date - datetime.now()).days
        return expiry_date.strftime("%Y-%m-%d"), days_left
    except Exception:
        return "Unknown", None

def color_text(text, color):
    return f"{color}{text}{Style.RESET_ALL}"

def check_vps_status(csv_file):
    print(
        f"{Style.BRIGHT + Fore.WHITE}{'Client':<18}"
        f"{Fore.CYAN}{'IP Address':<22}"
        f"{Fore.BLUE}{'Spec':<6}"
        f"{Fore.MAGENTA}{'Status':<8}"
        f"{Fore.GREEN}{'Warranty':<25}"
        f"{Fore.YELLOW}{'Expiry Date':<15}"
        f"{Fore.RED}{'Days Left':<15}"
        f"{Fore.LIGHTBLACK_EX}{'Checked At'}"
    )
    print(Style.RESET_ALL + "-" * 140)

    with open(csv_file, newline='') as infile:
        reader = csv.DictReader(infile, skipinitialspace=True)
        for row in reader:
            if not row["client"].strip():
                continue

            status = check_ssh(row["ip"])
            warranty_status = get_warranty_info(row.get("warranty", "0"), row.get("reg_date", ""))
            expiry_date, days_left = get_expiry_info(row.get("reg_date", ""))
            checked_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            client = f"{Fore.WHITE}{row['client'].strip():<18}"
            ip = f"{Fore.CYAN}{row['ip']:<22}"
            spec = f"{Fore.BLUE}{row['spec']:<6}"
            status_colored = (Fore.GREEN if status == "Online" else Fore.RED) + f"{status:<8}"
            expiry_colored = f"{Fore.YELLOW}{(expiry_date or 'N/A'):<15}"

            if days_left is None:
                days_left_plain = "Unknown"
                days_left_str = color_text(days_left_plain.ljust(15), Fore.MAGENTA)
            elif days_left >= 0:
                days_left_plain = f"{days_left} days left"
                days_left_str = color_text(days_left_plain.ljust(15), Fore.GREEN)
            else:
                days_left_plain = f"Expired ({abs(days_left)}d ago)"
                days_left_str = color_text(days_left_plain.ljust(15), Fore.RED)

            checked_at_str = checked_at

            print(f"{client}{ip}{spec}{status_colored}{warranty_status:<25}{expiry_colored}{days_left_str}{Fore.LIGHTBLACK_EX}{checked_at_str}")

if __name__ == "__main__":
    while True:
        clear_terminal()
        check_vps_status("data.csv")
        answer = input("\nDo you want to check again? (y/n): ").strip().lower()
        if answer not in ('y', 'yes'):
            print("Exiting...")
            break
