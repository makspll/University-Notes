/*************************************************************************************|
|   1. YOU ARE NOT ALLOWED TO SHARE/PUBLISH YOUR CODE (e.g., post on piazza or online)|
|   2. Fill main.c and memory_hierarchy.c files                                       |
|   3. Do not use any other .c files neither alter main.h or parser.h                 |
|   4. Do not include any other library files                                         |
|*************************************************************************************/
#include "mipssim.h"

/// @students: declare cache-related structures and variables here
//cache functions and structs
struct block
{
    int address;
    bool valid;
    int tag;
    int index;
    char* data; //byte addressible data, data[i] == MEM[Address + i]
    
};
struct block * cache;
int tag_bits;
int offset_bits;
int index_bits;


int get_offset(int address)
{
    int offset = get_piece_of_a_word(address,0,offset_bits);

}
int get_index(int address)
{
    int index = get_piece_of_a_word(address,offset_bits,index_bits);

}
int get_tag(int address)
{
    int tag = get_piece_of_a_word(address,32 - tag_bits,tag_bits);
}

void load_cache_block(int address)
{
    check_address_is_word_aligned(address);

    int offset = get_offset(address);
    int index = get_index(address);
    int tag = get_tag(address);

    struct block mapped_block = cache[index];

    mapped_block.tag = tag; //THIS DOESNT UPDATE RIGHT, TAG IS OFF
    mapped_block.index = index;
    mapped_block.address = address;
    mapped_block.valid = 1;
    printf("new tag: %d\n", mapped_block.tag);
    for(int w = 0; w < 4; w++)
    {
        int curr_word_address = (mapped_block.address & 0xfffffff0) + w*4;
        uint32_t curr_word = arch_state.memory[curr_word_address/4];
        for(int b = 0; b < 4; b++)
        {
            char portion_bits = get_piece_of_a_word((int)curr_word,(3-b)*8,8);
            printf("block: %d,i %d,%d, offset: %d :\n",index,w,b, (w*4)+b);
            print_binary_32bit_or_less_lsb(portion_bits,8);
            printf("\n");
            mapped_block.data[(w*4) + b] = portion_bits;
        }
    }



}

//reads the cache at given address
int read_cache(int address)
{
    int offset = get_offset(address);
    int index = get_index(address);
    return (int) cache[index].data[offset];
}

// end

void memory_state_init(struct architectural_state* arch_state_ptr) {
    arch_state_ptr->memory = (uint32_t *) malloc(sizeof(uint32_t) * MEMORY_WORD_NUM);
    memset(arch_state_ptr->memory, 0, sizeof(uint32_t) * MEMORY_WORD_NUM);
    if(cache_size == 0){
        // CACHE DISABLED
        memory_stats_init(arch_state_ptr, 0); // WARNING: we initialize for no cache 0
    }else {
        // CACHE ENABLED
        
        int words_in_block = 4;
        offset_bits = 4;
        int num_blocks = (float)cache_size / (float)16;
        index_bits = ceil(log2(num_blocks));
        tag_bits = 32- index_bits - offset_bits;
        memory_stats_init(arch_state_ptr,tag_bits);

        printf("offset bits: %d, index_bits %d, tag_bits: %d",offset_bits,index_bits,tag_bits);
        //initialize cache
        cache = malloc(num_blocks * sizeof(struct block));
        for(int i = 0; i < num_blocks;i++)
        {
            struct block block;
            block.valid = 0;
            block.data = malloc(sizeof(16)); //block size
            cache[i] = block;
        }
    }
}


// returns data on memory[addres            print_binary_32bs / 4]
int memory_read(int address){
    arch_state.mem_stats.lw_total++;
    check_address_is_word_aligned(address);
    if(cache_size == 0){
        // CACHE DISABLED
        return (int) arch_state.memory[address / 4];
    }else{
        printf("reading address:",address);
        print_binary_32bit_or_less_lsb(address,32);
        printf("\n");
        // CACHE ENABLED
        int offset = get_offset(address);
        int index = get_index(address);
        int tag = get_tag(address);

        struct block mapped_block = cache[index];
        //see if it's a miss of not
        printf("%d ==? %d\n",tag,mapped_block.tag);
        if(mapped_block.valid && tag == mapped_block.tag)
        {
            //hit
            printf("hit\n");
            arch_state.mem_stats.lw_cache_hits+=1;
        }
        else
        {
            //miss
            //load whole block from main memory
            printf("miss\n");
            load_cache_block(address);
            
        }

        //now we read the 4 bytes in cache and concatenate them
        

        printf("goal %d\n",arch_state.memory[address/4]);
        print_binary_32bit_or_less_lsb(arch_state.memory[address/4],32);
        printf("\n");
        int word = 0;
        for(int i = 0;i< 4;i++)
        {
            int mask = 0x000000ff << (24-(i*8));
            word = ((read_cache(address) << (24 - (i*8))) & mask) | word;
            printf("mask\n");
            print_binary_32bit_or_less_lsb(mask,32);
            printf("\n");
            print_binary_32bit_or_less_lsb(((read_cache(address) << (24 - (i*8))) & mask),32);
            printf("address: %d\n",address);
            address+= 1;
        }//ERROR HERE, first first byte turns to 1's]
        print_binary_32bit_or_less_lsb(word,32);
        printf("read: %d\n", word);
  
        return word;


    }
    return 0;
}



// writes data on memory[address / 4]
void memory_write(int address, int write_data){
    arch_state.mem_stats.sw_total++;
    check_address_is_word_aligned(address);

    if(cache_size == 0){
        // CACHE DISABLED
        arch_state.memory[address / 4] = (uint32_t) write_data;
    }
    else
    {
        int offset = get_offset(address);
        int index = get_index(address);
        int tag = get_tag(address);

        struct block mapped_block = cache[index];

        //write the value to the main memory
        arch_state.memory[address/4] = (uint32_t) write_data;

        //check if we have a hit
        if(mapped_block.valid && tag == mapped_block.tag)
        {
            arch_state.mem_stats.sw_cache_hits+=1;
        }
        else
        {
            mapped_block.address = address;
            mapped_block.index = index;
            mapped_block.tag = tag;
            mapped_block.valid = 1;
        }
        //write the value to the cache;
        load_cache_block(address);
    }
}
