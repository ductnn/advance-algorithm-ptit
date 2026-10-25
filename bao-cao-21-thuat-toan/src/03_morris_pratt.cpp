// Thuật toán Morris-Pratt: duyệt văn bản từ trái sang phải, không bao giờ lùi
// trên văn bản; khi gặp ký tự không khớp, dịch mẫu theo bảng biên mpNext.
#include "kiemnghiem.h"

// mpNext[i] = độ dài biên dài nhất của x[0..i-1]; mpNext[0] = -1.
void preMp(char *x, int m, int mpNext[]) {
  int i, j;
  i = 0;
  j = mpNext[0] = -1;
  while (i < m) {
    while (j > -1 && x[i] != x[j]) j = mpNext[j];
    mpNext[++i] = ++j;
  }
}

void MP(char *x, int m, char *y, int n) {
  int i, j;
  std::vector<int> mpNext(m + 1);

  /* Tiền xử lý */
  preMp(x, m, mpNext.data());
  VET_BANG("mpNext", mpNext.data(), m + 1);

  /* Tìm kiếm */
  i = j = 0;
  ATTEMPT(0);
  while (j < n) {
    while (i > -1 && !CMP(i, j)) {
      i = mpNext[i];  // không khớp: dịch mẫu đi i - mpNext[i] vị trí
      ATTEMPT(j - i);
    }
    i++;
    j++;
    if (i >= m) {
      OUTPUT(j - i);
      i = mpNext[i];
      ATTEMPT(j - i);
    }
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, MP, "Morris-Pratt"); }
