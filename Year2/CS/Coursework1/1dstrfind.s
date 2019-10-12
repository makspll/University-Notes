
#=========================================================================
# 1D String Finder 
#=========================================================================
# Finds the [first] matching word from dictionary in the grid
# 
# Inf2C Computer Systems
# 
# Siavash Katebzadeh
# 8 Oct 2019
# 
#
#=========================================================================
# DATA SEGMENT
#=========================================================================
.data
#-------------------------------------------------------------------------
# Constant strings
#-------------------------------------------------------------------------

grid_file_name:         .asciiz  "1dgrid.txt"
dictionary_file_name:   .asciiz  "dictionary.txt"
newline:                .asciiz  "\n"

#-------------------------------------------------------------------------
# Global variables in memory
#-------------------------------------------------------------------------
# 
grid:                   .space 33       # Maximun size of 1D grid_file + NULL
.align 4                                # The next field will be aligned
dictionary:             .space 11001    # Maximum number of words in dictionary *
                                        # ( maximum size of each word + \n) + NULL
MAX_DIM_SIZE:		 .word 32       # maximum size of each dimension
MAX_DICTIONARY_WORDS:    .word 1000     # maximum number of words in dictionary file
MAX_WORD_SIZE:           .word 10	# maximum size of each word in the dictionary

.align 2
dictionary_idx:		 .space 4000    # starting index of each word in the dictionary, 1000 words x 4 bytes per int
dict_num_words:          .word 0        # number of words in the dictionary
#=========================================================================
# TEXT SEGMENT  
#=========================================================================
.text

#-------------------------------------------------------------------------
# MAIN code block
#-------------------------------------------------------------------------

.globl main                     # Declare main label to be globally visible.
                                # Needed for correct operation with MARS
main:
#-------------------------------------------------------------------------
# Reading file block. DO NOT MODIFY THIS BLOCK
#-------------------------------------------------------------------------

# opening file for reading

        li   $v0, 13                    # system call for open file
        la   $a0, grid_file_name        # grid file name
        li   $a1, 0                     # flag for reading
        li   $a2, 0                     # mode is ignored
        syscall                         # open a file
        
        move $s0, $v0                   # save the file descriptor 

        # reading from file just opened

        move $t0, $0                    # idx = 0

READ_LOOP:                              # do {
        li   $v0, 14                    # system call for reading from file
        move $a0, $s0                   # file descriptor
                                        # grid[idx] = c_input
        la   $a1, grid($t0)             # address of buffer from which to read
        li   $a2,  1                    # read 1 char
        syscall                         # c_input = fgetc(grid_file);
        blez $v0, END_LOOP              # if(feof(grid_file)) { break }
        lb   $t1, grid($t0)          
        addi $v0, $0, 10                # newline \n
        beq  $t1, $v0, END_LOOP         # if(c_input == '\n')
        addi $t0, $t0, 1                # idx += 1
        j    READ_LOOP 
END_LOOP:
        sb   $0,  grid($t0)            # grid[idx] = '\0'

        # Close the file 

        li   $v0, 16                    # system call for close file
        move $a0, $s0                   # file descriptor to close
        syscall                         # fclose(grid_file)


        # opening file for reading

        li   $v0, 13                    # system call for open file
        la   $a0, dictionary_file_name  # input file name
        li   $a1, 0                     # flag for reading
        li   $a2, 0                     # mode is ignored
        syscall                         # fopen(dictionary_file, "r")
        
        move $s0, $v0                   # save the file descriptor 

        # reading from  file just opened

        move $t0, $0                    # idx = 0

READ_LOOP2:                             # do {
        li   $v0, 14                    # system call for reading from file
        move $a0, $s0                   # file descriptor
                                        # dictionary[idx] = c_input
        la   $a1, dictionary($t0)       # address of buffer from which to read
        li   $a2,  1                    # read 1 char
        syscall                         # c_input = fgetc(dictionary_file);
        blez $v0, END_LOOP2             # if(feof(dictionary_file)) { break }
        lb   $t1, dictionary($t0)                             
        beq  $t1, $0,  END_LOOP2        # if(c_input == '\0')
        addi $t0, $t0, 1                # idx += 1
        j    READ_LOOP2
END_LOOP2:
        sb   $0,  dictionary($t0)       # dictionary[idx] = '\0'

        # Close the file 

        li   $v0, 16                    # system call for close file
        move $a0, $s0                   # file descriptor to close
        syscall                         # fclose(dictionary_file)
#------------------------------------------------------------------
# End of reading file block.
#------------------------------------------------------------------
#------------------------------------------------------------------
# main functionality of the program
#------------------------------------------------------------------
	#storing the starting index of each word in the dictionary
	addiu $t0,$zero,0 		# idx = 0
	
	addiu $t4, $zero,0 		# dict_idx = 0				
	addiu $t5, $zero,0 		# start_idx = 0
	
STORE_LOOP:				# do {
	la $t1, dictionary              # &dictionary -> t1
	addu $t1,$t1,$t0               # &dictionary[idx] -> t1
	lb $t3, 0($t1)			# c_input = dictionary[idx]
	
	beqz $t3, END_STORE_LOOP	# if(c_input == '\0') {break;}
	bne $t3,10 NOT_WORD_BOUNDARY    # if(c_input == '\n') {
	
	la $t6, dictionary_idx          # &dictionary_idx -> t6
	sll $t7, $t4, 2			# since int, we multiply index by 4 -> t7
	addu $t6, $t6,$t7		# &dictionary_idx[dict_idx] ->t6
	sw $t5, ($t6)			# dictionary_idx[dict_idx] = start_idx;
	
	addiu $t4,$t4, 1			#dict_idx += 1
	addu $t5,$t0,1			#start_idx = idx + 1
	
NOT_WORD_BOUNDARY:
	addiu $t0,$t0,1			# idx += 1;
	
	j STORE_LOOP			# while (1)
	
END_STORE_LOOP:
	sw $t4, dict_num_words		# dict_num_words = dict_idx;
	
	#test print_word
	#la $a1,dictionary #dictionary -> a1
	#addiu $a1,$a1,4
	#jal print_word

	#test contain
	#la $a1, dictionary
	#addiu $a1, $a1, 27 #choose "not" from dict
	#la $a2, grid
	#addiu $a2,$a2,28  #choose n position in grid
	#jal contain

	jal strfind
		
	j main_end

#-----------------------------------------------------------------
# helper functions
#-----------------------------------------------------------------

#desc: print the given \n terminated word
#in  : $a1 = &word (non-aligned)
#out : none
#used: $a0 = *word, $v0 = syscall code
print_word:
					 # while( 
	lb $a0,0($a1)                    # dereference a1: *word -> a0 
	beq $a0,10,print_word_exit       # (*word != '\n' &&
	beq $a0,$zero, print_word_exit   # *word != '\0')
					 
					 # print_char(*word)
	addiu $v0,$zero,11               # v0 <- 11 syscall print code for char
	syscall				 # a0 already contains char to print: *word
	
	addiu $a1,$a1,1                  # word++
	
	j print_word			 # complete the while loop
	
print_word_exit:
	
	jr $ra                           #return 0



#desc: given a string and a word (\n terminated) returns 1 if word is contained in string
#in  : #a1 = $word (dictionary word start idx) 
       #a2 = $string (grid start idx)
#out : #v0 = (bool)
#used: #t1 = *string, $t0 = *word
contain:				# while(1) {
	lb $t1,($a2)			# *string
	lb $t0,($a1)			# *word
	bne $t1,$t0,contain_exit	# if(*string != *word)
	
	addiu $a2,$a2,1			#string++
	addiu $a1,$a1,1			#word++
	
	j contain
	
contain_exit:                           
	seq $v0,$t0,10			#*word == '\n' | if end of word v0 is 1
	jr $ra				#return (*word == '\n')

#desc: strfind for 1d grid
#in  :  
#out : I/O
#used: 
strfind:
	addiu $t1, $zero, 0		#int grid_idx = 0 -> t1
STRFIND_LOOP:	

	la $t2, grid			# t2 = &grid[0]
	addu $t2, $t2, $t1		# t2 = &grid[grid_idx]
	lb $t2, 0($t2)			# t2 = grid[grid_idx]
	beqz $t2, STRFIND_LOOP_EXIT	# while (grid[grid_idx] != '\0')
	
	addiu $t0, $zero, 0 		#int idx = 0 -> t0
STRFIND_LOOP2:
	lw $t3, dict_num_words          #t3 = dict_num_words
	slt $t3, $t0, $t3		#for(idx = 0; idx < dict_num_words; idx ++) t3 -> 1 if idx < dict_num_words
	beqz $t3, STRFIND_LOOP2_EXIT	#skip word if idx >= dict_num_words , otherwise
	
	la $a1, dictionary_idx
	sll $t3, $t0, 2			#get offset in words -> t3
	addu $a1, $a1, $t3		
	lw $a1, 0($a1)			# a1 = dictionary_idx[idx] == starting index for current word
	
	la $a2, dictionary		# a2 = &dictionary[0]
	addu $a1, $a1, $a2		# a1 <-  dictionary + dictionary_idx[idx] e.g. position in memory of first letter of current word
	
	la $a2, grid			# a2 <- &grid[0]
	addu $a2, $a2, $t1		# a2 <- grid + grid_idx
	#save variables before call
	addiu $sp, $sp, -21
	sw $ra, 17($sp)
	sw $t1,13($sp)
	sw $t0,9($sp)
	sw $a1,5($sp)
	sw $a2,1($sp)
	sb $t2,0($sp)
	
	#test if the word is in the string at current position
	jal contain			# contain(grid + grid_idx, word) | v0 = bool
	
	lw $ra, 17($sp)
	lw $t1,13($sp)
	lw $t0,9($sp)
	lw $a1,5($sp)
	lw $a2,1($sp)
	lb $t2,0($sp)
	addiu $sp, $sp, 21
	
	addiu $t0, $t0, 1		#idx++
	
	beqz $v0, STRFIND_LOOP2		# if (contain(grid + grid_idx, word)) {
	
	addiu $a0, $t1, 0		# print_int(grid_idx)
	addu $v0, $zero, 1 		# syscall call code
	syscall
	
	addiu $a0, $zero, 32		# print_char(' ')
	addu $v0, $zero, 11 		# syscall call code
	syscall
	
	#a1 = &word
	addiu $sp, $sp, -4
	sw $ra, 0($sp)
	
	jal print_word 
	
	lw $ra, 0($sp)
	addiu $sp, $sp, 4
	
	addiu $a0, $t1, 0		# print_char('\n')
	addu $v0, $zero, 10 		# syscall call code
	syscall
	
	jr $ra
	
	

	
STRFIND_LOOP2_EXIT:

	addiu $t1, $t1, 1		# grid_idx++
	
	j STRFIND_LOOP
	
STRFIND_LOOP_EXIT:
	
	addiu $a0, $zero, -1		# print_int(-1)
	addu $v0, $zero, 1 		# syscall call code
	syscall
	
	addiu $a0, $t1, 0		# print_char('\n')
	addu $v0, $zero, 10 		# syscall call code
	syscall
	
	jr $ra

#------------------------------------------------------------------
# Exit, DO NOT MODIFY THIS BLOCK
#------------------------------------------------------------------
main_end:      
        li   $v0, 10          # exit()
        syscall

#----------------------------------------------------------------
# END OF CODE
#----------------------------------------------------------------
