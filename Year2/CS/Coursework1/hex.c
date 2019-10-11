// =========================================================================
// Decimal to Hex calculator
// =========================================================================
// C version of MIPS code

// Inf2C Computer Systems

// Paul Jackson
// 8 Oct 2013

// Code assumes sizeof(int) == 4.


//---------------------------------------------------------------------------
// C definitions for SPIM system calls
//---------------------------------------------------------------------------
#include <stdio.h>

int read_char() { return getchar(); }
int read_int()
{
    int i;
    scanf("%i", &i);
    return i;
}
void read_string(char* s, int size) { fgets(s, size, stdin); }

void print_char(int c)     { putchar(c); }   
void print_int(int i)      { printf("%i", i); }
void print_string(char* s) { printf("%s", s); }

//---------------------------------------------------------------------------
// Global variables
//---------------------------------------------------------------------------

int input_num;
int loop_count;

//---------------------------------------------------------------------------
// GET_HEX_CHAR function
//---------------------------------------------------------------------------
// Take an integer in range 0 .. 15.  Return the corresponding ASCII character.

int get_hex_char(int i)
{
    if (i < 10) 
        return '0' + i;
    else 
        return 'a' + (i - 10);
}
//---------------------------------------------------------------------------
// MAIN function
//---------------------------------------------------------------------------

int main (void)
{
    // Read in number to print in hex
    print_string("Enter decimal number: ");
    input_num = read_int();

    print_string("\nThe number in hex is: "); 

    // Loop 8 times, once for each hex digit. 
    loop_count = 8; 
    while (loop_count != 0) {


        // Get the leftmost nibble (4 bits) of input_num.
        // The >> operation on an int var is arithmetic shift right. 
        // We use the bitwise and to get the effect of a logical shift right.

        int left_nibble = (input_num >> 28) & 0xf; 

        // Compute the hex character corresponding to the leftmost nibble.
        int hex_char = get_hex_char(left_nibble);

        // Output the hex character.
        print_char(hex_char);
        
        // Make the next nibble of input_num the leftmost one
        input_num = input_num << 4;  
        loop_count--;
    }

    print_string("\n");
    return 0;
}
