#include <stdio.h>

int test(int a, int b){
  int t;
  t = a + b;
  return t;
  }
int main(){
  int a, b, result;
  a = 1;
  b = 2;
  result = test(a, b);
  printf("test(%d, %d) = %d\n", a, b, result);
  }
