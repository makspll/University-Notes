/*************************************************************************************|
|   1. YOU ARE NOT ALLOWED TO SHARE/PUBLISH YOUR CODE (e.g., post on piazza or online)|
|   2. Fill main.c and memory_hierarchy.c files                                       |
|   3. Do not use any other .c files neither alter main.h or parser.h                 |
|   4. Do not include any other library files                                         |
|*************************************************************************************/

#include "mipssim.h"

#define BREAK_POINT 200000 // exit after so many cycles -- useful for debugging

//added, these were missing, the hell boris :C
//register types
#define I_TYPE 2
#define J_TYPE 3

//alu opcodes
#define ALU_ADD 0
#define ALU_SUB 1
#define ALU_FUNCT 2
//alu source
#define ALU_SRC_2_B 0
#define ALU_SRC_2_4 1
#define ALU_SRC_2_SIGNEXT_IMM 2
#define ALU_SRC_2_SIGNEXT_IMM_SHIFTED 3
//funct codes
#define FUNCT_ADD 32//100000
#define FUNCT_SLL 42//101010
//these don't need to be supported
#define FUNCT_SUB 34//100010
#define FUNCT_AND 36//100100
#define FUNCT_OR 37//100101

// Global variables
char mem_init_path[1000];
char reg_init_path[1000];

// debug functions
void debugDumpCurrentPipeRegs()
{
    printf("/////curr_pipe_regs/////\nstate: %d\nPC: %d\nMDR: %d\nIR: %x\nA: %d\nB: %d\nALUOut: %d\n////////////////\n",
        arch_state.state,
        arch_state.curr_pipe_regs.pc,
        arch_state.curr_pipe_regs.MDR,
        arch_state.curr_pipe_regs.IR,
        arch_state.curr_pipe_regs.A,
        arch_state.curr_pipe_regs.B,
        arch_state.curr_pipe_regs.ALUOut);
}

void debugDumpNextPipeRegs()
{
    printf("/////next_pipe_regs/////\nstate: %d\nPC: %d\nMDR: %d\nIR: %x\nA: %d\nB: %d\nALUOut: %d\n////////////////\n",
        arch_state.state,
        arch_state.next_pipe_regs.pc,
        arch_state.next_pipe_regs.MDR,
        arch_state.next_pipe_regs.IR,
        arch_state.next_pipe_regs.A,
        arch_state.next_pipe_regs.B,
        arch_state.next_pipe_regs.ALUOut);
}
//
uint32_t cache_size = 0;
struct architectural_state arch_state;

static inline uint8_t get_instruction_type(int opcode)
{
    switch (opcode) {
        /// opcodes are defined in mipssim.h

        case SPECIAL:
            return R_TYPE;
        case EOP:
            return EOP_TYPE;
        ///@students: fill in the rest
        case ADDI:
            return I_TYPE;
        case ADD:
            return R_TYPE;
        case LW:
            return I_TYPE;
        case SW:
            return I_TYPE;
        case BEQ:
            return I_TYPE;
        case J:
            return J_TYPE;
        case SLT:
            return R_TYPE;
        default:
            assert(false);
    }
    assert(false);
}


void FSM()
{
    struct ctrl_signals *control = &arch_state.control;
    struct instr_meta *IR_meta = &arch_state.IR_meta;

    //reset control signals
    memset(control, 0, (sizeof(struct ctrl_signals)));

    /*
    #define INSTR_FETCH 0
    #define DECODE 1
    #define MEM_ADDR_COMP 2
    #define MEM_ACCESS_LD 3
    #define WB_STEP 4
    #define MEM_ACCESS_ST 5
    #define EXEC 6
    #define R_TYPE_COMPL 7
    #define BRANCH_COMPL 8
    #define JUMP_COMPL 9
    #define EXIT_STATE 10
    #define I_TYPE_EXEC 11
    #define I_TYPE_COMPL 12
    
    //Instruction types
    #define R_TYPE 1s
    #define I_TYPE 1s
    #define EOP_TYPE 6s
s
s
    // OPCODESs
    #define SPECIAL 0 //s 000000 x
    #define ADD 32    //s 100000 x
    #define ADDI 8    //s 001000 x
    #define LW 35     //s 100011 x
    #define SW 43     // 101011  x
    #define BEQ  4    // 000100  x
    #define J 2       // 000010  x
    #define SLT 42    // 101010  
    #define EOP 63    // 111111  x
    */
    int opcode = IR_meta->opcode;
    int state = arch_state.state;
    switch (state) {
        ///level 0
        case INSTR_FETCH: //0
            control->MemRead = 1;
            control->ALUSrcA = 0;
            control->IorD = 0;
            control->IRWrite = 1;
            control->ALUSrcB = 1;
            control->ALUOp = 0;
            control->PCWrite = 1;
            control->PCSource = 0;
            state = DECODE;
            break;
        case DECODE: //1
            control->ALUSrcA = 0;
            control->ALUSrcB = 3;
            control->ALUOp = 0;
            if (IR_meta->type == R_TYPE)            state = EXEC;
            else if (IR_meta->opcode == ADDI)       state = I_TYPE_EXEC;
            else if (opcode == EOP)                 state = EXIT_STATE;
            else if (IR_meta->opcode == LW || IR_meta->opcode == SW)   state = MEM_ADDR_COMP;
            else if (IR_meta->opcode == BEQ)        state = BRANCH_COMPL;
            else if (IR_meta->opcode == J)          state = JUMP_COMPL;
            else assert(false);
            break;
        //level 1 - depends on op code
        case MEM_ADDR_COMP: //2
            control->ALUSrcA = 1;
            control->ALUSrcB = 2;
            control->ALUOp = 0;
            if (IR_meta->opcode == LW) state = MEM_ACCESS_LD;
            else if(IR_meta->opcode == SW) state = MEM_ACCESS_ST;
            else assert(false);
            break;
        case EXEC: //6
            control->ALUSrcA = 1;
            control->ALUSrcB = 0;
            control->ALUOp = 2;
            state = R_TYPE_COMPL;
            break;
        case I_TYPE_EXEC: //11
            // A 'ALUop' sign extended immediate
            control->ALUSrcA = 1;
            control->ALUSrcB = 2;
            control->ALUOp = 0;
            state = I_TYPE_COMPL;
            break;
        case BRANCH_COMPL:  //8
            control->ALUSrcA = 1;
            control->ALUSrcB = 0;
            control->ALUOp = 1;
            control->PCSource = 1;
            control->PCWriteCond = 1;
            state = INSTR_FETCH;
            break;
        case JUMP_COMPL: //9
            control->PCWrite = 1;
            control->PCSource = 2;
            state = INSTR_FETCH;
            break;
        //level 2 - only memory and R-type/I-type instructions
        case MEM_ACCESS_LD: //3
            control->MemRead = 1;
            control->IorD = 1;
            state = WB_STEP;
            break;
        case MEM_ACCESS_ST: // 5
            control->MemWrite = 1;
            control->IorD = 1;
            state = INSTR_FETCH;
            break;
        case R_TYPE_COMPL://7
            control->RegDst = 1;
            control->RegWrite = 1;
            control->MemtoReg = 0;
            state = INSTR_FETCH;
            break;
        case I_TYPE_COMPL: //12
            control->RegDst = 0;
            control->RegWrite = 1;
            control->MemtoReg = 0;
            state = INSTR_FETCH;
            break;
        //level 3- only lw instruction
        case WB_STEP:   //4
            control->RegDst = 0;
            control->RegWrite = 1;
            control->MemtoReg = 1;
            state = INSTR_FETCH;
            break;

        default: assert(false);
    }
    arch_state.state = state;
}


void instruction_fetch()
{
    if (arch_state.control.MemRead) {
        int address = arch_state.curr_pipe_regs.pc;
        arch_state.next_pipe_regs.IR = memory_read(address);
    }
} 

void decode_and_read_RF()
{
    int read_register_1 = arch_state.IR_meta.reg_21_25;
    int read_register_2 = arch_state.IR_meta.reg_16_20;

    check_is_valid_reg_id(read_register_1);
    check_is_valid_reg_id(read_register_2);
    arch_state.next_pipe_regs.A = arch_state.registers[read_register_1];
    arch_state.next_pipe_regs.B = arch_state.registers[read_register_2];
    //PC increment is included in execute... why do ya gotta complicate my life dear Boris :C
}

void execute()
{
    struct ctrl_signals *control = &arch_state.control;
    struct instr_meta *IR_meta = &arch_state.IR_meta;
    struct pipe_regs *curr_pipe_regs = &arch_state.curr_pipe_regs;
    struct pipe_regs *next_pipe_regs = &arch_state.next_pipe_regs;

    //Input1 = PC or A
    int alu_opA = control->ALUSrcA == 1 ? curr_pipe_regs->A : curr_pipe_regs->pc;
    int alu_opB = 0;
    int immediate = IR_meta->immediate;
    int shifted_immediate = (immediate) << 2;
    //Input2 = B or 4(word_size) or immediate sign extended or immediate sign extended sll by 2
    switch (control->ALUSrcB) {
        case ALU_SRC_2_B:
            alu_opB = curr_pipe_regs->B;
            break;
        case ALU_SRC_2_4:
            alu_opB = WORD_SIZE;
            break;
        case ALU_SRC_2_SIGNEXT_IMM:
            alu_opB = immediate;
            break; 
        case ALU_SRC_2_SIGNEXT_IMM_SHIFTED:
            alu_opB = shifted_immediate;
            break;
        default: 
            assert(false);
            break;
    }

    switch (control->ALUOp) {
        case ALU_ADD:
            next_pipe_regs->ALUOut = alu_opA + alu_opB;
            break;
        case ALU_SUB:
            next_pipe_regs->ALUOut = alu_opA - alu_opB;
            break;
        case ALU_FUNCT:
            if (IR_meta->function == FUNCT_ADD){
                next_pipe_regs->ALUOut = alu_opA + alu_opB;}
            else if(IR_meta->function ==FUNCT_SUB)
                next_pipe_regs->ALUOut = alu_opA - alu_opB;
            else if(IR_meta->function ==FUNCT_SLL)
                next_pipe_regs->ALUOut = (alu_opA < alu_opB)?1:0;
            else if(IR_meta->function ==FUNCT_AND)
                next_pipe_regs->ALUOut = alu_opA & alu_opB;
            else if(IR_meta->function ==FUNCT_OR)
                next_pipe_regs->ALUOut = alu_opA | alu_opB;
            else
                assert(false);
            break;
        default:
            assert(false);
            break;
    }

    // PC calculation, only write to pc on write
    if(control->PCWrite || (control->PCWriteCond && next_pipe_regs->ALUOut == 0))
    switch (control->PCSource) {
        //current alu output
        case 0:
            //the values in next_pipe are not yet stored, they're the 'currently being worked out solution'
            next_pipe_regs->pc = next_pipe_regs->ALUOut;
            break;
        //previous alu output
        case 1:
            //the value in curr pipe reg, i the result from the previous cycle
            next_pipe_regs->pc = curr_pipe_regs->ALUOut;
            break;
        //lower 26 bits pc << 2 concatenated with IR[]
        case 2:
            //ERROR HERE, JUMP jumps to ITSELF
            next_pipe_regs->pc = (get_piece_of_a_word(curr_pipe_regs->ALUOut,0,26) << 2) | (get_piece_of_a_word(next_pipe_regs->ALUOut,28,4)); 
            break;
        default:
            assert(false);
            break;
    }
}


void memory_access() {
  ///@students: appropriate calls to functions defined in memory_hierarchy.c must be added
  int address = arch_state.curr_pipe_regs.ALUOut;
  if(arch_state.control.IorD == 1)
  {
    if(arch_state.control.MemRead)
    {
       arch_state.next_pipe_regs.MDR = memory_read(address);
    }
    else if(arch_state.control.MemWrite)
    {
       memory_write(address,arch_state.curr_pipe_regs.B);
    }
  }
}

void write_back()
{
    if (arch_state.control.RegWrite) {
        uint8_t write_reg_id;
        switch(arch_state.control.RegDst)
        {
            case 0:
                write_reg_id = arch_state.IR_meta.reg_16_20;
                break;
            case 1:
                write_reg_id =  arch_state.IR_meta.reg_11_15;
                break;
            default:
                assert(false);
                break;
        }
        check_is_valid_reg_id(write_reg_id);

        int write_data;
        switch(arch_state.control.MemtoReg)
        {
            case 0:
                write_data = arch_state.curr_pipe_regs.ALUOut;
                break;
            case 1:
                write_data = arch_state.curr_pipe_regs.MDR;
                break;
            default:
                assert(false);
                break;
        }
        if (write_reg_id > 0) {
            arch_state.registers[write_reg_id] = write_data;
            printf("Reg $%u = %d \n", write_reg_id, write_data);
        } else printf("Attempting to write reg_0. That is likely a mistake \n");
    }
}


void set_up_IR_meta(int IR, struct instr_meta *IR_meta)
{

    IR_meta->opcode = get_piece_of_a_word(IR, OPCODE_OFFSET, OPCODE_SIZE);
    IR_meta->immediate = get_sign_extended_imm_id(IR, IMMEDIATE_OFFSET);
    IR_meta->function = get_piece_of_a_word(IR, 0, 6);
    IR_meta->jmp_offset = get_piece_of_a_word(IR, 0, 26);
    IR_meta->reg_11_15 = (uint8_t) get_piece_of_a_word(IR, 11, REGISTER_ID_SIZE);
    IR_meta->reg_16_20 = (uint8_t) get_piece_of_a_word(IR, 16, REGISTER_ID_SIZE);
    IR_meta->reg_21_25 = (uint8_t) get_piece_of_a_word(IR, 21, REGISTER_ID_SIZE);
    IR_meta->type = get_instruction_type(IR_meta->opcode);

    switch (IR_meta->opcode) {
        case SPECIAL:
            if (IR_meta->function == ADD)
                printf("Executing ADD(%d), $%u = $%u + $%u (function: %u) \n",
                       IR_meta->opcode,  IR_meta->reg_11_15, IR_meta->reg_21_25,  IR_meta->reg_16_20, IR_meta->function);
            else assert(false);
            break;
        case ADDI:
            printf("Executing ADDI(%d), $%u = $%u + $%u (function: %u) \n",
                IR_meta->opcode,  IR_meta->reg_11_15, IR_meta->reg_21_25,  IR_meta->reg_16_20, IR_meta->function);
            break;
        case LW:
            printf("Executing LW(%d), $%u = $%u + $%u (function: %u) \n",
                IR_meta->opcode,  IR_meta->reg_11_15, IR_meta->reg_21_25,  IR_meta->reg_16_20, IR_meta->function);
            break;
        case SW:
            printf("Executing SW(%d), $%u = $%u + $%u (function: %u) \n",
                IR_meta->opcode,  IR_meta->reg_11_15, IR_meta->reg_21_25,  IR_meta->reg_16_20, IR_meta->function);
            break;
        case BEQ:
            printf("Executing BEQ(%d), $%u = $%u + $%u (function: %u) \n",
                IR_meta->opcode,  IR_meta->reg_11_15, IR_meta->reg_21_25,  IR_meta->reg_16_20, IR_meta->function);
            break;
        case J:
            printf("Executing J(%d), $%u = $%u + $%u (function: %u) \n",
                IR_meta->opcode,  IR_meta->reg_11_15, IR_meta->reg_21_25,  IR_meta->reg_16_20, IR_meta->function);
            break;
        case SLT:
            printf("Executing SLTJ(%d), $%u = $%u + $%u (function: %u) \n",
                IR_meta->opcode,  IR_meta->reg_11_15, IR_meta->reg_21_25,  IR_meta->reg_16_20, IR_meta->function);
            break;
        case EOP:
            printf("Executing EOP(%d)\n", 
                IR_meta->opcode);
            break;
        default: assert(false);
    }
}

void assign_pipeline_registers_for_the_next_cycle()
{
    struct ctrl_signals *control = &arch_state.control;
    struct instr_meta *IR_meta = &arch_state.IR_meta;
    struct pipe_regs *curr_pipe_regs = &arch_state.curr_pipe_regs;
    struct pipe_regs *next_pipe_regs = &arch_state.next_pipe_regs;


    if (control->IRWrite) {
        curr_pipe_regs->IR = next_pipe_regs->IR;
        printf("PC %d: ", curr_pipe_regs->pc / 4);
        set_up_IR_meta(curr_pipe_regs->IR, IR_meta);
    }
    curr_pipe_regs->ALUOut = next_pipe_regs->ALUOut;
    curr_pipe_regs->A = next_pipe_regs->A;
    curr_pipe_regs->B = next_pipe_regs->B;
    if (control->PCWrite) {
        check_address_is_word_aligned(next_pipe_regs->pc);
        curr_pipe_regs->pc = next_pipe_regs->pc;
    }
}


int main(int argc, const char* argv[])
{
    /*--------------------------------------
    /------- Global Variable Init ----------
    /--------------------------------------*/
    parse_arguments(argc, argv);
    arch_state_init(&arch_state);
    ///@students WARNING: Do NOT change/move/remove main's code above this point!
    while (true) {

        ///@students: Fill/modify the function bodies of the 7 functions below,
        /// Do NOT modify the main() itself, you only need to
        /// write code inside the definitions of the functions called below.


        FSM();
        debugDumpCurrentPipeRegs();
        instruction_fetch();

        decode_and_read_RF();

        execute();

        memory_access();

        write_back();

        debugDumpNextPipeRegs();

        assign_pipeline_registers_for_the_next_cycle();


       ///@students WARNING: Do NOT change/move/remove code below this point!
        marking_after_clock_cycle();
        arch_state.clock_cycle++;
        // Check exit statements
        if (arch_state.state == EXIT_STATE) { // I.E. EOP instruction!
            printf("Exiting because the exit state was reached \n");
            break;
        }
        if (arch_state.clock_cycle == BREAK_POINT) {
            printf("Exiting because the break point (%u) was reached \n", BREAK_POINT);
            break;
        }
    }
    marking_at_the_end();
}
