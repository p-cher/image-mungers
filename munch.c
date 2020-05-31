#include <stdio.h>
#define SIZE 1024

int main() {
  int munch[SIZE][SIZE];
  for (int t=0;t<SIZE;t++) {
    for (int y=0;y<SIZE;y++) {
      for (int x=0;x<SIZE;x++) {
	if (y==(x^t)) {
	  munch[y][x]=t;
	}
      }
    }
  }
  printf("P5\n%d %d\n%d\n",SIZE,SIZE,SIZE);
  for (int y=0;y<SIZE;y++) {
    for (int x=0;x<SIZE;x++) {
      if (SIZE>255) {
        putchar(munch[y][x]/256);
        putchar(munch[y][x]%256);
      } else {
        putchar(munch[y][x]);
      }
    }
  }
  return 0;
}
