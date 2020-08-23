# requires toolchain as defined in https://hackaday.io/project/160006/instructions
# udev step requires mapping to /dev/esp0
P=main
CC=xtensa-lx106-elf-gcc
LDLIBS=-nostdlib -Wl,-Map=output.map -Wl,--start-group -lc -lhal -lpp -llwip -lphy -lnet80211 -lwpa -lmain -Wl,--end-group -lgcc
CFLAGS= -I. -mlongcalls
LDFLAGS=-Teagle.app.v6.ld

all: $(P)

$(P)-0x00000.bin: $(P)
	esptool.py elf2image $^

$(P): $(P).o

$(P).o: $(P).c

flash: $(P)-0x00000.bin
	esptool.py --port /dev/esp0 write_flash 0 $(P)-0x00000.bin 0x10000 $(P)-0x10000.bin

clean:
	rm -f $(P) $(P).o $(P)-0x00000.bin $(P)-0x10000.bin
