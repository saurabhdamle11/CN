#include <stdio.h>
#include <string.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);

int main(int argc, char* argv[])
{
  if(argc!=3) 
  {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  //Declaring required variables
  int sock=connect_smtp("lunar.open.sice.indiana.edu", 25), size;
  char* rcpt = argv[1];
  char* filepath = argv[2];
  char msg[200]="", res[8192]="", str[4096]="",ch;

  //Declaring file pointer
  FILE *file;
  file=fopen(filepath, "r");

  //Checking size of file to ensure that it isn't beyond 4096 bytes
  fseek(file, 0L, SEEK_END);
  size=ftell(file);
  fseek(file, 0L, SEEK_SET);

  //If file is larger than 4096 bytes then the program exits
  if(size>4096)
  {
    printf("Size too large, enter file with size less than 4096 bytes");
    return 1;
  }

  //Fetching data from text file, character by character
  ch=fgetc(file);
  while(ch!=EOF)
  {
    strcat(str,&ch);
    ch=fgetc(file);
  }

  //Commands to send a test email

  //HELO Command
  send_smtp(sock, "HELO mkanitka@silo.luddy.indiana.edu\n", res, 8192);
  printf("Response token: %s", res);

  //Sender's email address
  strcat(msg,"MAIL FROM:<");
  strcat(msg, rcpt);
  strcat(msg, ">\n");
  send_smtp(sock, msg, res, 8192);
  printf("Response token: %s", res);

  //Making the string blank to bypass nested command error
  strcpy(msg, "");

  //Recipient's email address
  strcat(msg,"RCPT TO:<");
  strcat(msg, rcpt);
  strcat(msg, ">\n");
  send_smtp(sock, msg, res, 8192);
  printf("Response token: %s", res);

  send_smtp(sock, "DATA\n", res, 8192);
  printf("Response token: %s", res);

  //Email content passed to send_smtp
  strcat(str, "\r\n.\r\n");
  send_smtp(sock, str, res, 8192);
  printf("Response token: %s", res);
  
  //Quitting
  send_smtp(sock, "QUIT\n", res, 8192);
  printf("Response token: %s", res);

  return 0;
}