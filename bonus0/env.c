#include <stdlib.h>
#include <stdio.h>
int main (){
  printf("%p", getenv("SHELLCODE"));
  return 0;
}