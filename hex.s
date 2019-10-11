#=========================================================================
# Decimal to Hex calculator
#=========================================================================
# Print a number in hexadecimal, digit by digit.
# 
# Inf2C Computer Systems
# 
# Paul Jackson
#  8 Oct 2013
# 
# Based on program written by Aris Efthymiou, in turn derived from
# program from U. of Manchester for the ARM ISA
#
# MIPS comments show how code corresponds to an equivalent C program.
# C comments within MIPS comments are used to add further details on
# the operation of the MIPS code and the use of registers.
        
        #==================================================================
        # DATA SEGMENT
        #==================================================================
        .data
        #------------------------------------------------------------------
        # Constant strings for output messages
        #------------------------------------------------------------------

prompt1:        .asciiz  "Enter decimal number: "
outmsg:         .asciiz  "\nThe number in hex is: "
newline:        .asciiz  "\n"
        
        #------------------------------------------------------------------
        # Global variables in memory
        #------------------------------------------------------------------
        # None for this program.  Registers used instead.
        
        #==================================================================
        # TEXT SEGMENT  
        #==================================================================
        .text

        #------------------------------------------------------------------
        # Registers allocated for global variables
        #------------------------------------------------------------------
        # int input_num  // $s0
        # int loop_count // $s1

        #------------------------------------------------------------------
        # GET_HEX_CHAR function
        #------------------------------------------------------------------
        # Take an integer in range 0 .. 15.  Return the corresponding
	# ASCII character

                               # int get_hex_char(int i)
                               # i in $a0
get_hex_char:
                               # {
                               #    if (i < 10) 

        slti $t0, $a0, 10      #    // $t0 = i < 10
        beq  $t0, $0,  over10  #    // goto over10 if ! (i < 10)
                               #   {
                               #       return '0' + i;
        add  $v0, $a0, 48      #       // $v0 = $a0 + 48, ASCII for '0' is 48
        jr $ra                 #       // return $v0
                               #    }
over10:                        #    else {
                               #       return 'a' + (i - 10);
        add $v0, $a0, 87       #       // $v0 = $a0 + 87, ASCII for 'a' is 97
        jr $ra                 #       // return $v0
                               #    }
                               # }
  
  
        #------------------------------------------------------------------
        # MAIN code block
        #------------------------------------------------------------------

        .globl main           # Declare main label to be globally visible.
                              # Needed for correct operation with MARS
main:
        
        li   $v0, 4           # print_string("Enter decimal number: ");
        la   $a0, prompt1
        syscall

        li   $v0, 5           # input_num = read_int();
        syscall
        move $s0, $v0  


        li   $v0, 4           # print_string("\nThe number in hex is: ");
        la   $a0, outmsg
        syscall

        li   $s1, 8           # loop_count = 8; 

loop:   beqz $s1, main_end    # while (loop_count != 0)
                              # {
       
                              #    int left_nibble; // Use $t0 
        srl  $t0, $s0, 28     #    left_nibble = input_num >>(logical) 28;

                              #    int hex_char;    // Use $t1
        move $a0, $t0         #    hex_char = get_hex_char(left_nibble);
        jal  get_hex_char  
        move $t1, $v0      

print:  li   $v0, 11          #    print_char(hex_char);
        move $a0, $t1      
        syscall            

        sll  $s0, $s0, 4      #    input_num = input_num << 4;
        addi $s1, $s1, -1     #    loop_count-- ;
        j loop                # }

main_end:      
        li   $v0, 4           # print_string("\n");
        la   $a0, newline
        syscall

        li   $v0, 10          # exit()
        syscall

        #----------------------------------------------------------------
        # END OF CODE
        #----------------------------------------------------------------
