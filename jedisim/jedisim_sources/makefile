CC=gcc
CFLAGS=-O3 -Wall
LIBS=-I/usr/local/include -I/usr/include -lm -lcfitsio -lfftw3f
EXE_PATH=../executables
SRC_PATH=.

# execute program and clean it
default: jedi
	echo " compilation finished ... "




jedi : jedicatalog jeditransform jedidistort jedipaste jediconvolve jedirescale jedinoise jediaverage jedicolor

jedicatalog :
	gcc -Wall -O3 $(SRC_PATH)/jedicatalog.c -o $(EXE_PATH)/jedicatalog $(LIBS) -lm -lcfitsio -lfftw3f

jeditransform :
	$(CC) $(CFLAGS) $(SRC_PATH)/jeditransform.c -o $(EXE_PATH)/jeditransform $(LIBS)

jedidistort :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedidistort.c -o $(EXE_PATH)/jedidistort $(LIBS)

jedipaste :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedipaste.c -o $(EXE_PATH)/jedipaste $(LIBS)

jediconvolve :
	$(CC) $(CFLAGS) $(SRC_PATH)/jediconvolve.c -o $(EXE_PATH)/jediconvolve $(LIBS) -lfftw3f

jedirescale :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedirescale.c -o $(EXE_PATH)/jedirescale $(LIBS)

jedinoise :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedinoise.c -o $(EXE_PATH)/jedinoise $(LIBS)

jediaverage :
	$(CC) $(CFLAGS) $(SRC_PATH)/jediaverage.c -o $(EXE_PATH)/jediaverage $(LIBS)

jedicolor :
	$(CC) $(CFLAGS) $(SRC_PATH)/jedicolor.c -o $(EXE_PATH)/jedicolor $(LIBS)


# Utility targets
.PHONY: clean

clean:
	rm -rf $(EXE_PATH)/*.dSYM
