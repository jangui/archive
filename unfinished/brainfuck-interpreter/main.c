#include <stdio.h>
#include <stdlib.h>
#include <math.h>

struct node {
  struct node *next;
  struct node *prev;
  int data;
};

struct node* add_node(struct node *curr) {
  //create new data node
  struct node *newData = (struct node*)malloc(sizeof(struct node));
  curr->next = newData;
  newData->prev = curr;
  newData->data = 0;
  return newData;
}

void process_bf(char *bf, struct node *currData, char *startLoop);

void process_loop(char *bf, struct node *currData, char *startLoop) {
  for(;;) {
    switch (*bf) {
      case '[':
        if (currData->data == 0) {
          //go to end of loop
          int count = 0;
          //find end of loop
          while (*bf != ']' && count != 0) { 
            bf++;
            //count occurences of nested loop so we know actual end of current loop
            if (*bf == '[') count++; 
            else if (*bf == ']') count--;
          }
          break;
        }
        *startLoop = *bf;
        bf++;
        process_bf(bf, currData, startLoop);
        break;

      case ']':
        if (currData->data != 0) {*bf = *startLoop;break;}
        return;

      default:
        process_bf(bf, currData, startLoop);
    }
    bf++;
  }
}

void process_bf(char *bf, struct node *currData, char *startLoop) {
  for(;;) {
    switch (*bf) {
      case '+':
        currData->data++;
        break;

      case '-':
        currData->data--;
        break;

      case '>':
        if (currData->next == NULL) currData = add_node(currData);
        else currData = currData->next;
        break;

      case '<':
        if (currData->prev == NULL) {
          printf("error: tried accessing -1 data cell\n");
          exit(1);
        }
        currData = currData->prev;
        break;

      case '.':
        printf("%c\n", currData->data);
        break;

      case ',': ;
        currData->data = getchar();
        break;

      case '[': 
        process_loop(bf, currData, startLoop);
        break;

      case ']': 
        return;

      case '\0':
        return;

      default:
        break;
    }
    bf++;
  }
}

void clean(struct node *head) {
  //if only one node free it
  if (head->next == NULL) {
    free(head);   
    return;
  }
  //else clean whole list
  while (head->next != NULL) {
    head->prev = NULL; //clear prev
    head = head->next; //move to next
    head->prev->next = NULL; //clear old's next
    free(head->prev); //free old
  }
  free(head);
  head = NULL;
  return;
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("usage: ./interpreter <brainfuck>\n");
    exit(1);
  }
  //make start node
  struct node *head = (struct node*)malloc(sizeof(struct node));
  head->data = 0;
  head->next = NULL;
  head->prev = NULL;

  char sl;
  char *startLoop = &sl;

  process_bf(argv[1], head, startLoop); 
  clean(head);
  return 0;
}
