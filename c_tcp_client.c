#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <unistd.h>
#include <errno.h>
#define PORT 12345

typedef enum msg_type
{
  TYPE_A = 1,
  TYPE_B = 2,
  TYPE_C = 3,
  TYPE_D = 4,
  TYPE_E = 5,
} msg_type;

typedef struct msg_body
{
  msg_type t;
  char body[10];
} msg_body;

int main()
{

  int i = 0;
  for(i = 0; i < 1000; i ++)
  {
    int sockfd;
    struct sockaddr_in servaddr;

    // create socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    bzero(&servaddr, sizeof(servaddr));

    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    servaddr.sin_port = htons(PORT);
    // connect the client socket to server socket
    int rc = connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr));
    if (rc == -1)
    {
      printf("[Client_C]connection with the server failed errno=%s\n", strerror(errno));
      exit(0);
    }
    else
    {
      printf("[Client_C]connected to the server sockfd=%d\n", sockfd);
    }

    msg_body msg = {0};
    msg.t = (i % 5) + 1;
    write(sockfd, &msg, sizeof(msg));
    bzero(&msg, sizeof(msg));
    read(sockfd, &msg, sizeof(msg));
    printf("[Client_C] reply from server: type: %d body: %s\n", msg.t, msg.body);

    // close the socket
    close(sockfd);
  }

}
