// Thuật toán Tuned Boyer-Moore: cài đặt Horspool với "vòng lặp nhanh" — dịch
// liên tiếp 3 bước theo bảng ký tự tồi mà không so sánh, cho tới khi ký tự cuối
// cửa sổ khớp x[m-1]; dùng lính canh ở cuối văn bản để bỏ phép kiểm tra biên.
#include "kiemnghiem.h"

// Bảng ký tự tồi (bad-character): bmBc[c] = khoảng cách từ lần xuất hiện
// cuối cùng của c trong x[0..m-2] tới cuối mẫu; bằng m nếu c không xuất hiện.
void preBmBc(char *x, int m, int bmBc[]) {
  int i;
  for (i = 0; i < ASIZE; ++i) bmBc[i] = m;
  for (i = 0; i < m - 1; ++i) bmBc[U(x[i])] = m - i - 1;
}
void TUNEDBM(char *x, int m, char *y, int n) {
  int i, j, k, shift, bmBc[ASIZE];

  /* Tiền xử lý */
  preBmBc(x, m, bmBc);
  shift = bmBc[U(x[m - 1])];
  bmBc[U(x[m - 1])] = 0;     // ký tự cuối khớp => k = 0 dừng vòng lặp nhanh
  memset(y + n, x[m - 1], m);  // lính canh: m bản sao của x[m-1]

  /* Tìm kiếm */
  j = 0;
  while (j < n) {
    THAOTAC(j + m - 1);
    k = bmBc[U(y[j + m - 1])];
    while (k != 0) {  // vòng lặp nhanh: 3 lần dịch mỗi vòng
      j += k; THAOTAC(j + m - 1); k = bmBc[U(y[j + m - 1])];
      j += k; THAOTAC(j + m - 1); k = bmBc[U(y[j + m - 1])];
      j += k; THAOTAC(j + m - 1); k = bmBc[U(y[j + m - 1])];
    }
    if (j <= n - m) {
      // y[j+m-1] == x[m-1] đã được bảo đảm, chỉ cần so sánh x[0..m-2]
      ATTEMPT(j);
      i = 0;
      while (i < m - 1 && CMP(i, j + i)) ++i;
      if (i == m - 1) OUTPUT(j);
    }
    j += shift;
  }
  memset(y + n, 0, m);  // khôi phục phần đệm
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, TUNEDBM, "Tuned Boyer-Moore"); }
