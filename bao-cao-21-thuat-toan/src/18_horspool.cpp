// Thuật toán Horspool: đơn giản hóa Boyer-Moore, chỉ dùng bảng ký tự tồi tính
// theo ký tự CUỐI cửa sổ y[j+m-1] để dịch, bất kể ký tự không khớp nằm ở đâu.
#include "kiemnghiem.h"

// Bảng ký tự tồi (bad-character): bmBc[c] = khoảng cách từ lần xuất hiện
// cuối cùng của c trong x[0..m-2] tới cuối mẫu; bằng m nếu c không xuất hiện.
void preBmBc(char *x, int m, int bmBc[]) {
  int i;
  for (i = 0; i < ASIZE; ++i) bmBc[i] = m;
  for (i = 0; i < m - 1; ++i) bmBc[U(x[i])] = m - i - 1;
}
void HORSPOOL(char *x, int m, char *y, int n) {
  int i, j, bmBc[ASIZE];
  char c;

  /* Tiền xử lý */
  preBmBc(x, m, bmBc);

  /* Tìm kiếm: so sánh ký tự cuối trước, sau đó x[0..m-2] từ trái sang phải */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    c = y[j + m - 1];
    if (CMP(m - 1, j + m - 1)) {
      i = 0;
      while (i < m - 1 && CMP(i, j + i)) ++i;
      if (i == m - 1) OUTPUT(j);
    }
    j += bmBc[U(c)];
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, HORSPOOL, "Horspool"); }
