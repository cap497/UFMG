# Compiler name
CC = clang

# Compiler flags
CFLAGS = -Wall -pthread

# Executable name
TARGET = ex1

# Default rule
all: $(TARGET)

# Rule to compile the program
$(TARGET): ex1.c
	$(CC) $(CFLAGS) -o $(TARGET) ex1.c

# Rule to clean compiled files
clean:
	rm -f $(TARGET)
	rm -f *.o

# Rule to run the program
run: $(TARGET)
	./$(TARGET) < t.in | sort -n > t.out