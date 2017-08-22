#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <net/if.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/ioctl.h>
#include <sys/stat.h>
#include <netinet/in.h>

#include <time.h>
#include <netdb.h>
#include <arpa/inet.h>

#define SECONDS_1900_1970    0x83aa7e80

char time_str[10] = {0};

typedef struct 
{
	unsigned li   : 2;       // Only two bits. Leap indicator.
	unsigned vn   : 3;       // Only three bits. Version number of the protocol.
	unsigned mode : 3;       // Only three bits. Mode. Client will pick mode 3 for client.

	uint8_t stratum;         // Eight bits. Stratum level of the local clock.
	uint8_t poll;            // Eight bits. Maximum interval between successive messages.
	uint8_t precision;       // Eight bits. Precision of the local clock.

	uint32_t rootDelay;      // 32 bits. Total round trip delay time.
	uint32_t rootDispersion; // 32 bits. Max error aloud from primary clock source.
	uint32_t refId;          // 32 bits. Reference clock identifier.

	uint32_t refTm_s;        // 32 bits. Reference time-stamp seconds.
	uint32_t refTm_f;        // 32 bits. Reference time-stamp fraction of a second.

	uint32_t origTm_s;       // 32 bits. Originate time-stamp seconds.
	uint32_t origTm_f;       // 32 bits. Originate time-stamp fraction of a second.

	uint32_t rxTm_s;         // 32 bits. Received time-stamp seconds.
	uint32_t rxTm_f;         // 32 bits. Received time-stamp fraction of a second.

	uint32_t txTm_s;         // 32 bits and the most important field the client cares about. Transmit time-stamp seconds.
	uint32_t txTm_f;         // 32 bits. Transmit time-stamp fraction of a second.
} ntp_packet;                 // Total: 384 bits or 48 bytes.

static int time_get(const char *pNTPhost)
{
        int sockfd;
        int res, counter = 0;
        char *pServerIP;
        struct in_addr in;
        struct hostent *host;
        struct sockaddr_in addr;
        struct timeval timeout = {3, 0};
        unsigned long ultime = 0, ulTime_net = 0;
        //char hostname1[] = "time.nist.gov";//"time-b.nist.gov";//"time-a.nist.gov";//"time.windows.com";//"time-nw.nist.gov";//"time.nist.gov";
        char *pHostName = pNTPhost;

GETHOST:
        if((host = gethostbyname(pHostName)) != NULL) {
                memcpy(&in.s_addr,host->h_addr,4);
                pServerIP = inet_ntoa(in);
                printf("the ip of [%s] is :%s\n", pHostName, pServerIP);
        } else {
                printf("cannot get the ip of the domain:%s\n",pHostName);
                counter++;
                if(counter > 1) {
                        printf("cannot get ip of time_server\n");
                        return -1;
                }
                sleep(1);
                goto GETHOST;
        }

	ntp_packet packet = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	memset( &packet, 0, sizeof( ntp_packet ) );

        sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
        if (sockfd  < 0) {
                perror("socket creat");
                return -1;
        }

        res = setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, (char *)&timeout, sizeof(struct timeval));
        if (res  < 0) {
                perror("socket setsockopt");
                return -1;
        }

        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_port = htons(123);
        addr.sin_addr.s_addr = inet_addr(pServerIP);

        counter = 0;
CONNECT:
        res = connect(sockfd, (struct sockaddr *)&addr, sizeof(addr));
        if (res  < 0) {
                perror("socket connect");
                counter++;
                if(counter > 1) {
                        printf("socket connetc failed\n");
                        return -1;
                }
                sleep(1);
                goto CONNECT;
        }

	*( ( char * ) &packet + 0 ) = 0x1b; // Represents 27 in base 10 or 00011011 in base 2.

	res = write( sockfd, ( char* ) &packet, sizeof( ntp_packet ) );
	
	if ( res < 0 ) 
		perror( "ERROR writing to socket" );

        counter = 0;
RECV:
        res = read(sockfd, ( char* ) &packet, sizeof( ntp_packet ) );
        if (res  < 0) {
                perror("socket recv");
                counter++;
                if(counter > 1) {
                        printf("socket recv failed\n");
                        return -1;
                }
                sleep(1);
                goto RECV;
        }
	ultime = ntohl( packet.txTm_s ); // Time-stamp seconds.
        ultime -= SECONDS_1900_1970;
        //ultime += SECONDS_OF_8HOURS;
        if(ultime > 2000000000) {
                printf("time error reget\n");
                close(sockfd);
                sleep(1);
                goto GETHOST;
        }
        printf("current time %lu, %s", ultime, ctime((time_t *)&ultime));
        sprintf(time_str, "%ld", ultime);
        close(sockfd);

        return 0;
}


int main(int argc, char **argv)
{
	time_get("ntp1.aliyun.com");
	//time_get("ntp2.aliyun.com");
	//time_get("ntp3.aliyun.com");
	//time_get("ntp4.aliyun.com");
	//time_get("ntp5.aliyun.com");
	//time_get("ntp6.aliyun.com");
	//time_get("ntp7.aliyun.com");
	time_get("time.nist.gov");
	time_get("time-a.nist.gov");
	time_get("time-b.nist.gov");
	return 0;
}
