// Thuật toán Not So Naive: so sánh x[1] trước, rồi x[2..m-1], cuối cùng x[0];
// dựa vào việc x[0] có bằng x[1] hay không để dịch 1 hoặc 2 vị trí.
#include "kiemnghiem.h"

void NSN(char *x, int m, char *y, int n) {
  int i, j, k, ell;
  if (m < 2) {
    fprintf(stderr, "NSN: mau phai co do dai >= 2\n");
    exit(1);
  }

  /* Tiền xử lý */
  if (x[0] == x[1]) {
    k = 2;
    ell = 1;
  } else {
    k = 1;
    ell = 2;
  }

  /* Tìm kiếm */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    if (!CMP(1, j + 1))
      j += k;
    else {
      i = 2;
      while (i < m && CMP(i, j + i)) ++i;
      if (i == m && CMP(0, j)) OUTPUT(j);
      j += ell;
    }
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, NSN, "Not So Naive"); }
