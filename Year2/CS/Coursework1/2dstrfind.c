/***********************************************************************
* File       : <2dstrfind.c>
*
* Author     : <M.R. Siavash Katebzadeh>
*
* Description:
*
* Date       : 08/10/19
*
***********************************************************************/
// ==========================================================================
// 2D String Finder
// ==========================================================================
// Finds the matching words from dictionary in the 2D grid

// Inf2C-CS Coursework 1. Task 3-5
// PROVIDED file, to be used as a skeleton.

// Instructor: Boris Grot
// TA: Siavash Katebzadeh
// 08 Oct 2019

#include <stdio.h>

// maximum size of each dimension
#define MAX_DIM_SIZE 32
// maximum number of words in dictionary file
#define MAX_DICTIONARY_WORDS 1000
// maximum size of each word in the dictionary
#define MAX_WORD_SIZE 10

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
void output(char *string)  { print_string(string); }

// dictionary file name
const char dictionary_file_name[] = "dictionary.txt";
// grid file name
const char grid_file_name[] = "2dgrid.txt";
// content of grid file
char grid[(MAX_DIM_SIZE + 1 /* for \n */ ) * MAX_DIM_SIZE + 1 /* for \0 */ ];
// content of dictionary file 
char dictionary[MAX_DICTIONARY_WORDS * (MAX_WORD_SIZE + 1 /* for \n */ ) + 1 /* for \0 */ ];
///////////////////////////////////////////////////////////////////////////////
/////////////// Do not modify anything above
///////////////Put your global variables/functions here///////////////////////
// starting index of each word in the dictionary
int dictionary_idx[MAX_DICTIONARY_WORDS];
// number of words in the dictionary
int dict_num_words = 0;
// length of each row in the current grid with \n included
int grid_row_length = 0;
// the total number of characters including the \n in the grid
int grid_total_length = 0;
// function to print found word
void print_word(char *word)
{
  while(*word != '\n' && *word != '\0') {
    print_char(*word);
    word++;
  }
}

// function to see if the string contains the (\n terminated) word
int contain(char *string, char *word)
{
  while (1) {
    //check we're out of bounds to the right, wrap around
    if (*string == '\n')
    {
      string -= (grid_row_length - 1); // up and one right
    }
    if (*string != *word){
      return (*word == '\n');
    }
    
    string++;
    word++;
  }

  return 0;
}

// see if the vertical string contains the \n terminated word
int containV(char *string, char *word)
{
  while(1) {
    //check we're out of bounds down the bottom, wrap around if so
    if (string >= grid + grid_total_length)
    {
        string -= grid_total_length;
    }
    if (*string!= *word || *string == '\n' )
    {
        return (*word == '\n');
    }

    string += grid_row_length; // skip a row
    word++;
  }

  return 0;
}

int containD(char *string, char *word)
{
    //check for out of bounds both ways, wrap around PROBLEM HERE
    if(string >= grid + grid_total_length)
    {
        int idx = string - grid;
        string = grid + ((grid_row_length -(idx / grid_row_length))* grid_row_length);
    }
    if(*string == '\n')
    {
        int idx = string - grid;
        int rows = (grid_total_length / grid_row_length);
        string = grid + (rows - (idx % grid_row_length));
    }

    while(1) {
    if ( *string!= *word)
    {
        return (*word == '\n');
    }

    string += grid_row_length + 1; // skip a row and go right
    word++;
  }

  return 0;
}

// this functions finds all matches in the grid
void strfind()
{
  int idx = 0;
  int grid_idx = 0;
  char *word;
  char success = '\0';

  while (grid[grid_idx] != '\0') {
    for(idx = 0; idx < dict_num_words; idx ++) {
      word = dictionary + dictionary_idx[idx]; 
      if (contain(grid + grid_idx, word)) {
   
        print_int(grid_idx / grid_row_length); // y
        print_char(',');
        print_int(grid_idx % grid_row_length); // x
        print_char(' ');
        print_char('H');
        print_char(' ');
        print_word(word);
        print_char('\n');
        success = '1';
      }
      if(containV(grid + grid_idx, word))
      {
        print_int(grid_idx / grid_row_length); // y
        print_char(',');
        print_int(grid_idx % grid_row_length); // x
        print_char(' ');
        print_char('V');
        print_char(' ');
        print_word(word);
        print_char('\n');
        success = '1';
      }
      if(containD(grid + grid_idx, word))
      {
        print_int(grid_idx / grid_row_length); // y
        print_char(',');
        print_int(grid_idx % grid_row_length); // x
        print_char(' ');
        print_char('D');
        print_char(' ');
        print_word(word);
        print_char('\n');
        success = '1';
      }
    }

    grid_idx++;
  }
  if(!success)
  {
    print_string("-1\n");
  }
}

//---------------------------------------------------------------------------
// MAIN function
//---------------------------------------------------------------------------

int main (void)
{

  int dict_idx = 0;
  int start_idx = 0;

  /////////////Reading dictionary and grid files//////////////
  ///////////////Please DO NOT touch this part/////////////////
  int c_input;
  int idx = 0;


  // open grid file
  FILE *grid_file = fopen(grid_file_name, "r");
  // open dictionary file
  FILE *dictionary_file = fopen(dictionary_file_name, "r");

  // if opening the grid file failed
  if(grid_file == NULL){
    print_string("Error in opening grid file.\n");
    return -1;
  }

  // if opening the dictionary file failed
  if(dictionary_file == NULL){
    print_string("Error in opening dictionary file.\n");
    return -1;
  }
  // reading the grid file
  do {
    c_input = fgetc(grid_file);
    // indicates the the of file
    if(feof(grid_file)) {
      grid[idx] = '\0';
      break;
    }
    grid[idx] = c_input;
    idx += 1;

  } while (1);

  // closing the grid file
  fclose(grid_file);
  idx = 0;
   
  // reading the dictionary file
  do {
    c_input = fgetc(dictionary_file);
    // indicates the end of file
    if(feof(dictionary_file)) {
      dictionary[idx] = '\0';
      break;
    }
    dictionary[idx] = c_input;
    idx += 1;
  } while (1);


  // closing the dictionary file
  fclose(dictionary_file);
  //////////////////////////End of reading////////////////////////
  ///////////////You can add your code here!//////////////////////
  //counting how long the whole grid is
  char* current_char = grid;
  while (*current_char != '\0')
  {
    grid_total_length += 1;
    current_char += 1;
  }
  //counting how long each row is in the grid
  
  current_char = grid;
  while (*current_char != '\n')
  {
    grid_row_length += 1;
    current_char += 1;
  }
  grid_row_length +=1;
  
  // storing the starting index of each word in the dictionary
  idx = 0;
  do {
    c_input = dictionary[idx];
    if(c_input == '\0') {
      break;
    }
    if(c_input == '\n') {
      dictionary_idx[dict_idx ++] = start_idx;
      start_idx = idx + 1;
    }
    idx += 1;
  } while (1);

  dict_num_words = dict_idx;

  strfind();

  return 0;
}
