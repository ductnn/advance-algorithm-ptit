// Thuật toán Quick Search (Sunday): dịch theo ký tự NGAY SAU cửa sổ y[j+m];
// các ký tự trong cửa sổ có thể được so sánh theo thứ tự bất kỳ.
#include "kiemnghiem.h"

// Bảng dịch Quick Search: qsBc[c] = m - (vị trí xuất hiện cuối của c trong x);
// bằng m + 1 nếu c không có trong x.
void preQsBc(char *x, int m, int qsBc[]) {
  int i;
  for (i = 0; i < ASIZE; ++i) qsBc[i] = m + 1;
  for (i = 0; i < m; ++i) qsBc[U(x[i])] = m - i;
}
void QS(char *x, int m, char *y, int n) {
  int i, j, qsBc[ASIZE];

  /* Tiền xử lý */
  preQsBc(x, m, qsBc);

  /* Tìm kiếm */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    i = 0;
    while (i < m && CMP(i, j + i)) ++i;
    if (i == m) OUTPUT(j);
    j += qsBc[U(y[j + m])];  // y[n] = '\0' khi cửa sổ ở cuối văn bản
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, QS, "Quick Search"); }
