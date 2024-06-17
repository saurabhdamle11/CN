import os
import signal
import socket
import threading
from _thread import *


def threaded(conn, cnt, s):

    exit_s=False

    while True:

        msg=conn.recv(256)
        msg=msg.decode().replace("\n", "")

        if msg=="hello":
            conn.sendall("world\n".encode())

        elif msg=="goodbye":
            conn.sendall("farewell\n".encode())
            conn.close()
            cnt-=1
            break
                
        elif msg=="exit":
            conn.sendall("ok\n".encode())
            exit_s=True
            break

        else:
            msg=msg+"\n"
            conn.sendall(msg.encode())

    if exit_s:
        conn.close()
        s.shutdown(socket.SHUT_RDWR)
    


def chat_server(iface:str, port:int, use_udp:bool) -> None:
    
    
    print("Hello, I am a server")

    if use_udp is True: 
            
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:  
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            host, port1=socket.getaddrinfo(iface, port)[0][4]

            s.bind((host, port1))
            while True:

                msg=s.recvfrom(256)
                msg0=msg[0].decode().replace("\n", "")
                print(f"got message from ('{msg[1][0]}', {port1})")
                if msg0=="hello":
                    s.sendto("world\n".encode(), msg[1])

                elif msg0=="goodbye":
                    s.sendto("farewell\n".encode(), msg[1])
                            
                elif msg0=="exit":
                    s.sendto("ok\n".encode(), msg[1])
                    s.close()
                    return

                else:
                    msg0=msg0+"\n"
                    conn.sendto(msg0.encode(), msg[1])

    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            cnt=0

            host, port1=socket.getaddrinfo(iface, port)[0][4]

            s.bind((host, port1))
            while True:
                s.listen()
               
                try:
                    conn, addr=s.accept()
                    cnt+=1
                    print(f"\nconnection {cnt} from ('{addr[0]}', {port1})")
                    print(f"got message from ('{addr[0]}', {port1})")
                    start_new_thread(threaded, (conn, cnt, s))

                except:
                    s.close()
                    break
                    

def chat_client(host:str, port:int, use_udp:bool) -> None:

    print("Hello, I am a client")

    if use_udp is True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host, port1=socket.getaddrinfo(host, port)[0][4]
            while True:
                msg=input()
                s.sendto(str.encode(msg), (host, port1))
                msg1=s.recv(256).decode().replace("\n", "")
                print(f"{msg1}")
                if msg=="goodbye" or msg=="exit":
                    s.close()
                    return

    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host, port1=socket.getaddrinfo(host, port)[0][4]
            s.connect((host, port1))
            while True:
                try:
                    msg=input()
                    s.sendall(msg.encode())
                    msg1=s.recv(256).decode().replace("\n", "")
                    print(f"{msg1}")
                    if msg=="goodbye" or msg=="exit":
                        s.close()
                        return

                except KeyboardInterrupt:
                    s.close()
                    break
            