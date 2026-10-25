// Thuật toán Berry-Ravindran: dịch theo cặp hai ký tự NGAY SAU cửa sổ
// y[j+m] y[j+m+1] (mở rộng ý tưởng của Quick Search).
#include "kiemnghiem.h"

// brBc[a][b] = độ dịch khi hai ký tự ngay sau cửa sổ là "ab".
void preBrBc(char *x, int m, std::vector<std::vector<int> > &brBc) {
  int a, i;
  brBc.assign(ASIZE, std::vector<int>(ASIZE, m + 2));
  for (a = 0; a < ASIZE; ++a) brBc[a][U(x[0])] = m + 1;
  for (i = 0; i < m - 1; ++i) brBc[U(x[i])][U(x[i + 1])] = m - i;
  for (a = 0; a < ASIZE; ++a) brBc[U(x[m - 1])][a] = 1;
}

void BR(char *x, int m, char *y, int n) {
  int i, j;
  std::vector<std::vector<int> > brBc;

  /* Tiền xử lý */
  preBrBc(x, m, brBc);
  y[n + 1] = '\0';  // y[n], y[n+1] được dùng khi cửa sổ ở cuối văn bản

  /* Tìm kiếm: so sánh cửa sổ từ trái sang phải */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    i = 0;
    while (i < m && CMP(i, j + i)) ++i;
    if (i == m) OUTPUT(j);
    j += brBc[U(y[j + m])][U(y[j + m + 1])];
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, BR, "Berry-Ravindran"); }
