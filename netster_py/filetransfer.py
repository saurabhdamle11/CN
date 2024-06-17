import socket
from typing import BinaryIO


def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:

    print("Hello, I am a server")

    if use_udp is True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host, port=socket.getaddrinfo(iface, port)[0][4]
            
            s.bind((host, port))
            opfile=open(fp.name, "wb")
            msg=s.recv(256)
        
            while msg:
                opfile.write(msg)
                msg=s.recv(256)
                
            opfile.close()
            s.close()  
         
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host, port=socket.getaddrinfo(iface, port)[0][4]  

            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            opfile=open(fp.name, "wb")
            msg=conn.recv(256)
        
            while msg:
                opfile.write(msg)
                msg=conn.recv(256)
                
            opfile.close()
            conn.close()
            s.close()  
        

def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:

    print("Hello, I am a client")

    if use_udp is True:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            host, port=socket.getaddrinfo(host, port)[0][4]
            file=open(fp.name, "rb")
            fdata=file.read(256)
            while fdata:
                s.sendto(fdata, (host, port))
                fdata=file.read(256)
            s.sendto("".encode(), (host, port))
            file.close()
            s.close()
         
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            host, port=socket.getaddrinfo(host, port)[0][4]
            s.connect((host, port))
            file=open(fp.name, "rb")
            fdata=file.read(256)
            while fdata:
                s.send(fdata)
                fdata=file.read(256)
            s.send("".encode())
            file.close()
            s.close()
