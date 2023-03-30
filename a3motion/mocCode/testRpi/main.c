#include <stdio.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <i2c/smbus.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <ctype.h>
//#include <conio.h>
void display_byte(uint8_t b) {
    for (int i = 0; i < 8; ++i)
    {
        if (b & 1 << (7 - i))
            printf("1");
        else
            printf("0");
    }
}
uint8_t input_byte() {
    char *p, s[100];
    long n;

    while (fgets(s, sizeof(s), stdin)) {
        n = strtol(s, &p, 10);
        if (p != s && *p == '\n' ) {
            break;
        }
        if (n > 255)
            return 255;
    }
    return n;
}
uint32_t input_u32() {
    char *p, s[100];
    long n;

    while (fgets(s, sizeof(s), stdin)) {
        n = strtol(s, &p, 10);
        if (p != s && *p == '\n' ) {
            break;
        }
    }
    return n;
}

int i2c_open(int *file, int adapter_nr) {
    char filename[20];
    snprintf(filename, 19, "/dev/i2c-%d", adapter_nr);
    *file = open(filename, O_RDWR);
    printf("opening device /dev/i2c-%d\n", adapter_nr);
    if (*file < 0) {
        printf("error opening %d \n", adapter_nr);
        /* ERROR HANDLING; you can check errno to see what went wrong */
        return 0;
    }
    printf("success\n");
    return 1;

}

int i2c_start(int file, uint8_t addr) {
    printf("opening address %d\n", addr);
    if (ioctl(file, I2C_SLAVE, addr) < 0)
    {
        printf("Failed to acquire bus access and/or talk to slave.\n");

        return -1;
    }
    printf("success\n");
    return 1;
}

int i2c_write(int file, uint8_t *buf, uint8_t n_buf) {
    //printf("writing %d bytes\n", n_buf);
    if (write(file, buf, n_buf) != n_buf) {
        printf("Failed to write\n");
        exit(1);
    }

    //printf("success\n");
    return 1;
}
void delay_millis(long milis) {
    for (long i = 0; i < milis; ++i)
    {
        usleep(930);
    }
}
int i2c_read(int file, uint8_t *buf, uint8_t n_buf) {
    printf("reading %d bytes\n", n_buf);
    int8_t test = read(file, buf, n_buf);
    if (test != n_buf) {
        printf("Failed to read. Read %d bytes\n", test);
        exit(1);
    }
    printf("success\n");
    return 1;
}
int i2c_read_silent(int file, uint8_t *buf, uint8_t n_buf) {
    //printf("reading %d bytes\n", n_buf);
    int8_t test = read(file, buf, n_buf);
    if (test != n_buf) {
        printf("Failed to read. Read %d bytes\n", test);
        exit(1);
    }
    //printf("success\n");
    return 1;
}
uint8_t buf_read[16];
uint8_t buf_read_n = 0;
uint8_t buf_write[16];
uint8_t buf_write_n;
void delay(int number_of_seconds)
{
    // Converting time into milli_seconds
    long milli_seconds = 100 * number_of_seconds;

    // Storing start time
    clock_t start_time = clock();

    // looping till required time is not achieved
    while (clock() < start_time + milli_seconds)
        ;
}

void repeat_display() {
    uint8_t tm_cnt = 0;
    printf("start\n");
    while (1) {
        printf("%d", tm_cnt++);
        fflush(stdout);
        delay(1000);
        printf("\33[2K\r");
    }

}


char getchar_no_enter() {
    int c;
    /* use system call to make terminal send all keystrokes directly to stdin */
    system ("/bin/stty raw");
    c = getchar();
    /* use system call to set terminal behaviour to more normal behaviour */
    printf("\n");
    system ("/bin/stty cooked");
    return c;
}
void create_button_command(uint8_t r, uint8_t g, uint8_t b, uint8_t *out) {
    if (r < 64 && g < 64 && b < 16) {
        out[1] = r << 2;
        out[1] |= g >> 4;
        out[0] = g << 4;
        out[0] |= b;
    }
}
uint8_t create_button_command_header(uint8_t **buts, uint8_t n) {
    uint8_t ret = 0b01010000;
    for (int i = 0; i < n; ++i)
    {
        ret |= (1 << buts[i][0]);
    }
    return ret;
}
void create_command_all(uint8_t r, uint8_t g, uint8_t b, uint8_t *commands) {
    commands[0] = 0b01011111;
    uint8_t buts[4][3] = {0};
    for (int i = 0; i < 4; ++i)
        create_button_command(r, g, b, &buts[i][1]);
    for (int i = 0; i < 4; ++i)
    {
        commands[(i * 2) + 2] = buts[i][1];
        commands[(i * 2) + 1] = buts[i][2];
    }
}
int main() {
    int file;
    int mod_id = 1;
    int dev_id = 1;
    uint8_t chk = 0;
    uint8_t is_first_start = 1;
    printf("A3 Audio Moc Test\n\n");
    while (1) {
        chk = i2c_open(&file, dev_id);
        if (chk)
            break;
        printf("try another dev id! 0,1 or 2 are common\n");
        dev_id = input_byte();
    }
    printf("\n\n");

    printf("Module id is %d\n", mod_id);
    printf("Change it? y/n   (Q quit)\n");
    char ans = getchar_no_enter();
    fflush(stdin);
    if (tolower(ans) == 'q')
        return 0;
    if (ans == 'y') {
        mod_id = input_byte();
    }
    i2c_start(file, mod_id);

    while (1) {
        printf("\nPress:\nL   for led test\nS   for sensor test\nE   for encoder setup(not working)\n");
        printf("M   to change module id (not working))\nC   to change id\nQ   to exit\n\n");
        ans = getchar_no_enter();
        ans = tolower(ans);
        switch (ans) {
        case 'l': {
            uint8_t commands[9] = {0};
            uint8_t first = 1;
            uint8_t time_s=10;
            for (int i = 0; i < 10; ++i)
            {
                printf("LED test %d seconds",time_s-i);
                fflush(stdout);
                create_command_all(61, 0, 0, commands);
                i2c_write(file, commands, 9);
                delay_millis(333);
                create_command_all(0, 61, 0, commands);
                i2c_write(file, commands, 9);
                delay_millis(333);
                create_command_all(0, 0, 15, commands);
                i2c_write(file, commands, 9);
                delay_millis(333);
                first = 0;

                printf("\33[2K\r");
                
            }
        }
        printf("\n\n\n");
        break;

        case 's':{
            printf("reading\n");
            printf("How long in s(0 indef)\n");
            uint32_t time_s=input_u32();
            uint32_t cnt1=0;
            uint32_t cnt2=0;
            if(time_s==0)
                time_s= (uint32_t)(-1);
            buf_read_n = 6;//input_byte();
            uint8_t br[6];
            int enc = 0;
            char load,b0,b1,b2,b3;
            uint16_t adc0,adc1;
            uint8_t cnt = 0;
            printf("B0 B1 B2 B3    ADC0   ADC1    ENC\n");
            while (cnt2!=time_s) {
                if (i2c_read_silent(file, br, buf_read_n) == 1) {
                    enc += (int8_t)br[5];
                    load = (cnt++ & 1) ? 'O' : '|';
                    adc0 = ((uint16_t)br[1] | br[2] << 8);
                    adc1 = ((uint16_t)br[3] | br[4] << 8);
                    b0 = (br[0] & 1 << 0) ? 'X' : 'O';
                    b1 = (br[0] & 1 << 1) ? 'X' : 'O';
                    b2 = (br[0] & 1 << 2) ? 'X' : 'O';
                    b3 = (br[0] & 1 << 3) ? 'X' : 'O';
                    
                    printf("%c  %c  %c  %c %6d %6d   %6d  %8c", b0, b1, b2, b3, adc0, adc1, enc, load);
                    fflush(stdout);
                    delay_millis(100);
                    printf("\33[2K\r");

                }
                cnt1++;
                if((cnt1%10)==0)
                    cnt2++;
            }
            printf("%c  %c  %c  %c %6d %6d   %6d  %8c", b0, b1, b2, b3, adc0, adc1, enc, load);
        }
            break;
        case 'e':
            break;
        case 'c':
            printf("Module id is %d\n", mod_id);
            mod_id = input_byte();
            printf("Change it to  %d and start!\n", mod_id);
            i2c_start(file, mod_id);
            break;
        case 'q':
            exit(0);
        }
    }

    return 0;
}
