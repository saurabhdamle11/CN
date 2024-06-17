from typing import BinaryIO
import socket

def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    print("Hello, I am a server")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host, port=socket.getaddrinfo(iface, port)[0][4]
            s.bind((host, port))
            opfile=open(fp.name, "wb")
            lpktnum=0
            
            while True:
                msg, addr=s.recvfrom(512)
                if not msg:
                    break
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
                print("packet received: ", pktnum, lpktnum)
                if pktnum==lpktnum :
                    opfile.write(msg[j+2:])
                    lpktnum+=1
                    s.sendto("T".encode(), addr)
                else:
                    s.sendto("F".encode(), addr)
                # msg, addr=s.recvfrom(512)
            opfile.close()
            s.close() 

def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    print("Hello, I am a client")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            host, port=socket.getaddrinfo(host, port)[0][4]
            s.settimeout(0.1)
            
            lst=[]
            n=2 # Window size

            file=open(fp.name, "rb")
            fdata=file.read(256)
            while fdata:
                lst.append(fdata)
                fdata=file.read(256)

            pkt=0
            length=len(lst)
            breakFlag = False
            while pkt<length:
                ack=0
                i=str(pkt)
                k=str(len(lst[pkt]))
                for j in range(n):
                    if pkt > len(lst)-1:
                        breakFlag = True
                        break
                    s.sendto(str(pkt).encode()+"__".encode()+k.encode()+"--".encode()+lst[pkt], (host, port))
                    print("packet no sent: ", pkt)
                    pkt+=1
                for j in range(n):
                    try:
                        res, addr=s.recvfrom(512)
                        if res.decode()=="T":
                            ack+=1
                    except socket.timeout:
                        print("timeout")
                        if ack!=n and pkt>0:
                            pkt-=n
                            continue
                        elif breakFlag:
                            break
                if breakFlag:
                    break
                
            for i in range(10):
                s.sendto("".encode(), (host, port))
            file.close()
            s.close()
