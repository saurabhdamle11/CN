#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */

int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }

//declaration of structure objects
struct addrinfo hint;
struct addrinfo *result, *address; 

//declaring required variables
  char* host = argv[1];
  char* port = argv[2];
  char buff[8192];
  int retval;
  void* raw_addr;//to store the returned raw address out of which the IP address will be extracted using inet_ntop

//initialising variable in addrinfor struct to values stated
  memset(&hint, 0, sizeof(hint));
  hint.ai_family=PF_UNSPEC;
  hint.ai_socktype=SOCK_STREAM;
  hint.ai_protocol=IPPROTO_TCP;
  hint.ai_flags=AI_PASSIVE;
  
// returning raw result from getaddrinfo function(generally returns 0 if everything is fine)
  retval=getaddrinfo(host, port, &hint, &result);
  
//if the returned value is not 0 the program automatically sends an error message and terminates
  if(retval!=0)
  {
    fprintf(stderr, "error: %s\n", gai_strerror(retval));
    exit(EXIT_FAILURE);
  }

//loop defined to get the ip addr value stroed in ai_addr, structure is traversed using ai_next
  address=result;

  while(address!=NULL)
  {
    //IPv4 address printing
    if (address->ai_family==AF_INET) 
    {
      struct sockaddr_in* tmp=(struct sockaddr_in*)address->ai_addr;
      raw_addr=&(tmp->sin_addr);

      if(inet_ntop(AF_INET, raw_addr, buff, 8192)!=NULL)
      printf("IPv4 %s\n", buff);

      else
      exit(EXIT_FAILURE);
    }

    //IPv6 address printing
    else 
    {
      struct sockaddr_in6* tmp=(struct sockaddr_in6*)address->ai_addr;
      raw_addr=&(tmp->sin6_addr);
      
      if(inet_ntop(AF_INET6, raw_addr, buff, 8192)!=NULL)
      printf("IPv6 %s\n", buff);

      else
      exit(EXIT_FAILURE);
    }

    address=address->ai_next;
  }

  return 0;
}