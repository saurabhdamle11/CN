#include <stdio.h>
#include <string.h>

void send_http(char* host, char* msg, char* resp, size_t len);

int main(int argc, char* argv[]) 
{
  if (argc != 4) 
  {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }

  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];
  char msg[50]="", res[8192]="";

  strcat(msg, verb);
  strcat(msg, " ");
  strcat(msg, path);
  strcat(msg, " HTTP/1.1\r\nHost:");
  strcat(msg, host);
  strcat(msg, " \r\n\r\n");

  send_http(host, msg, res, 8192);
  printf("%s", res);

  return 0;
}
