from typing import BinaryIO
import socket

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    print("Hello, I am a server")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host, port=socket.getaddrinfo(iface, port)[0][4]
            
            s.bind((host, port))
            opfile=open(fp.name, "wb")
            msg, addr=s.recvfrom(512)
            lpktnum=0
            while msg:
                i=0
                try:
                    while msg[i:i+2].decode()!="__":
                        i+=1
                    j=i+2
                    while msg[j:j+2].decode()!="--":
                        j+=1
                except IndexError:
                    s.sendto("F".encode(), addr)

                pktnum=int(msg[:i].decode())
                length=int(msg[i+2:j].decode())
                if pktnum==lpktnum and length==len(msg[j+2:]):
                    opfile.write(msg[j+2:])
                    lpktnum+=1
                    s.sendto("T".encode(), addr)
                else:
                    s.sendto("F".encode(), addr)
                msg, addr=s.recvfrom(512)
                
            opfile.close()
            s.close() 

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    print("Hello, I am a client")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(0.025)
            lst=[]
            pkt=0
            host, port=socket.getaddrinfo(host, port)[0][4]
            file=open(fp.name, "rb")
            fdata=file.read(256)
            while fdata:
                lst.append(fdata)
                fdata=file.read(256)

            length=len(lst)

            while pkt<length:
                i=str(pkt)
                k=str(len(lst[pkt]))
                s.sendto(i.encode()+"__".encode()+k.encode()+"--".encode()+lst[pkt], (host, port))
                fdata=file.read(256)
                try:
                    res, addr=s.recvfrom(256)
                    if res.decode()=="T":
                        pkt+=1
                except socket.timeout:
                    s.sendto(i.encode()+"__".encode()+k.encode()+"--".encode()+lst[pkt], (host, port))
            for i in range(10):
                s.sendto("".encode(), (host, port))
            file.close()
            s.close()
    

