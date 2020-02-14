Install pygame, don't use pip
```bash
sudo apt-get install python-pygame
```

Install pam header files for C
```bash
sudo apt-get install libpam0g-dev
```

Compiling the pam module
```bash
gcc -fPIC -fno-stack-protector -c src/mypam.c
sudo ld -x --shared -o /lib/security/mypam.so mypam.o
```
