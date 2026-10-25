// Thuật toán Shift-Or: mô phỏng automat không đơn định bằng các phép toán
// trên bit. Bit i của state bằng 0 khi x[0..i] khớp với hậu tố của y[0..j].
#include "kiemnghiem.h"

#define WORD (int)(sizeof(unsigned int) * 8)  // số bit của một từ máy

// Tiền xử lý: S[c] có bit i bằng 0 khi và chỉ khi x[i] == c.
unsigned int preSo(char *x, int m, unsigned int S[]) {
  unsigned int j, lim;
  int i;
  for (i = 0; i < ASIZE; ++i) S[i] = ~0u;
  for (lim = i = 0, j = 1; i < m; ++i, j <<= 1) {
    S[U(x[i])] &= ~j;
    lim |= j;
  }
  lim = ~(lim >> 1);  // state < lim  <=>  bit m-1 của state bằng 0
  return (lim);
}

void SO(char *x, int m, char *y, int n) {
  unsigned int lim, state;
  unsigned int S[ASIZE];
  int j;
  if (m > WORD) {
    fprintf(stderr, "SO: chi ho tro mau co do dai <= %d\n", WORD);
    exit(1);
  }

  /* Tiền xử lý */
  lim = preSo(x, m, S);

  /* Tìm kiếm: mỗi ký tự văn bản chỉ cần 1 phép dịch bit và 1 phép OR */
  for (state = ~0u, j = 0; j < n; ++j) {
    state = (state << 1) | S[U(y[j])];
    THAOTAC(j);
    VET("S %d %u", j, state);
    if (state < lim) OUTPUT(j - m + 1);
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, SO, "Shift-Or"); }
