// Thuật toán Automat hữu hạn (DFA): xây automat đơn định nhỏ nhất đoán nhận
// ngôn ngữ Σ*x; mỗi ký tự văn bản được xử lý đúng một lần bằng một bước chuyển.
#include "kiemnghiem.h"

// delta[q * ASIZE + c] = trạng thái kế tiếp từ q khi đọc c.
// Trạng thái q (0..m) = độ dài tiền tố dài nhất của x là hậu tố của văn bản đã đọc.
void preAut(char *x, int m, std::vector<int> &delta) {
  int i, c, r;
  delta.assign((m + 1) * ASIZE, 0);
  delta[0 * ASIZE + U(x[0])] = 1;
  r = 0;  // r: trạng thái ứng với biên dài nhất của x[0..i-1]
  for (i = 1; i <= m; ++i) {
    for (c = 0; c < ASIZE; ++c) delta[i * ASIZE + c] = delta[r * ASIZE + c];
    if (i < m) {
      delta[i * ASIZE + U(x[i])] = i + 1;  // cung "tiến" theo mẫu
      r = delta[r * ASIZE + U(x[i])];
    }
  }
}

void AUT(char *x, int m, char *y, int n) {
  int j, state;
  std::vector<int> delta;

  /* Tiền xử lý */
  preAut(x, m, delta);
  for (int q = 0; q <= m; ++q)
    VET("D %d %d %d %d %d", q, delta[q * ASIZE + 'A'], delta[q * ASIZE + 'C'],
        delta[q * ASIZE + 'G'], delta[q * ASIZE + 'T']);

  /* Tìm kiếm */
  for (state = 0, j = 0; j < n; ++j) {
    int truoc = state;
    state = delta[state * ASIZE + U(y[j])];
    THAOTAC(j);  // một bước chuyển trạng thái
    VET("S %d %d %d", j, truoc, state);
    if (state == m) OUTPUT(j - m + 1);
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, AUT, "Automat huu han"); }
