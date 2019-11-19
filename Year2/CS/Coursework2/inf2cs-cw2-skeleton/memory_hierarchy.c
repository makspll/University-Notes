/*************************************************************************************|
|   1. YOU ARE NOT ALLOWED TO SHARE/PUBLISH YOUR CODE (e.g., post on piazza or online)|
|   2. Fill main.c and memory_hierarchy.c files                                       |
|   3. Do not use any other .c files neither alter main.h or parser.h                 |
|   4. Do not include any other library files                                         |
|*************************************************************************************/
#include "mipssim.h"

/// @students: declare cache-related structures and variables here


void memory_state_init(struct architectural_state* arch_state_ptr) {
    arch_state_ptr->memory = (uint32_t *) malloc(sizeof(uint32_t) * MEMORY_WORD_NUM);
    memset(arch_state_ptr->memory, 0, sizeof(uint32_t) * MEMORY_WORD_NUM);
    if(cache_size == 0){
        // CACHE DISABLED
        memory_stats_init(arch_state_ptr, 0); // WARNING: we initialize for no cache 0
    }else {
        // CACHE ENABLED
        assert(0); /// @students: Remove assert(0); and initialize cache

        /// @students: memory_stats_init(arch_state_ptr, X); <-- fill # of tag bits for cache 'X' correctly
    }
}


// returns data on memory[address / 4]
int memory_read(int address){
    arch_state.mem_stats.lw_total++;
    check_address_is_word_aligned(address);

    if(cache_size == 0){
        // CACHE DISABLED
        return (int) arch_state.memory[address / 4];
    }else{
        // CACHE ENABLED
        assert(0); /// @students: Remove assert(0); and implement Memory hierarchy w/ cache

        /// @students: your implementation must properly increment: arch_state_ptr->mem_stats.lw_cache_hits
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
    }else{
        // CACHE ENABLED
        assert(0); /// @students: Remove assert(0); and implement Memory hierarchy w/ cache

        /// @students: your implementation must properly increment: arch_state_ptr->mem_stats.sw_cache_hits
    }
}
