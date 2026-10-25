// Thuật toán Knuth-Morris-Pratt: cải tiến Morris-Pratt bằng bảng kmpNext dựa
// trên "biên chặt" — tránh so sánh lại cùng ký tự đã biết chắc là không khớp.
#include "kiemnghiem.h"

// kmpNext[i] = độ dài biên chặt dài nhất của x[0..i-1] (biên u sao cho
// ký tự đứng sau u khác x[i]); bằng -1 nếu không tồn tại.
void preKmp(char *x, int m, int kmpNext[]) {
  int i, j;
  i = 0;
  j = kmpNext[0] = -1;
  while (i < m) {
    while (j > -1 && x[i] != x[j]) j = kmpNext[j];
    i++;
    j++;
    if (x[i] == x[j]) kmpNext[i] = kmpNext[j];
    else kmpNext[i] = j;
  }
}

void KMP(char *x, int m, char *y, int n) {
  int i, j;
  std::vector<int> kmpNext(m + 1);

  /* Tiền xử lý */
  preKmp(x, m, kmpNext.data());
  VET_BANG("kmpNext", kmpNext.data(), m + 1);

  /* Tìm kiếm */
  i = j = 0;
  ATTEMPT(0);
  while (j < n) {
    while (i > -1 && !CMP(i, j)) {
      i = kmpNext[i];
      ATTEMPT(j - i);
    }
    i++;
    j++;
    if (i >= m) {
      OUTPUT(j - i);
      i = kmpNext[i];
      ATTEMPT(j - i);
    }
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, KMP, "Knuth-Morris-Pratt"); }
