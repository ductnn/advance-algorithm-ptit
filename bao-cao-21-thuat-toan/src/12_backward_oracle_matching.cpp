// Thuật toán Backward Oracle Matching (BOM): đọc cửa sổ từ phải sang trái trên
// "factor oracle" của mẫu đảo ngược. Khi oracle không có cung đi tiếp thì
// đoạn vừa đọc chắc chắn không phải nhân tố của x, có thể dịch xa.
#include "kiemnghiem.h"

#define UNDEFINED (-1)

// Xây factor oracle của xR = x[m-1] x[m-2] ... x[0].
// Trạng thái 0..m; trans[q*ASIZE + c] = đích (hoặc UNDEFINED);
// T[q] = true nếu q là trạng thái kết (đoán nhận hậu tố của xR).
void oracle(char *x, int m, std::vector<int> &trans, std::vector<char> &T) {
  int i, k;
  std::vector<int> S(m + 1);  // liên kết hậu tố (supply function)
  trans.assign((m + 1) * ASIZE, UNDEFINED);
  T.assign(m + 1, 0);
  S[0] = -1;
  for (i = 1; i <= m; ++i) {
    int c = U(x[m - i]);  // ký tự thứ i của xR
    trans[(i - 1) * ASIZE + c] = i;
    k = S[i - 1];
    while (k > -1 && trans[k * ASIZE + c] == UNDEFINED) {
      trans[k * ASIZE + c] = i;
      k = S[k];
    }
    S[i] = (k == -1 ? 0 : trans[k * ASIZE + c]);
  }
  for (k = m; k > -1; k = S[k]) T[k] = 1;  // các trạng thái trên đường hậu tố
}

void BOM(char *x, int m, char *y, int n) {
  int i, j, p, q, shift, period = 0;
  std::vector<int> trans;
  std::vector<char> T;

  /* Tiền xử lý */
  oracle(x, m, trans, T);

  /* Tìm kiếm */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    i = m - 1;
    p = 0;
    shift = m;
    while (i >= 0) {
      THAOTAC(i + j);  // đọc một ký tự văn bản và thử một bước chuyển
      q = trans[p * ASIZE + U(y[i + j])];
      VET("B %d %d", i + j, q);
      if (q == UNDEFINED) break;
      p = q;
      if (T[p]) {  // y[i+j..j+m-1] là tiền tố của x
        period = shift;
        shift = i;
      }
      --i;
    }
    if (i < 0) {
      OUTPUT(j);
      shift = period;
    }
    j += shift;
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, BOM, "Backward Oracle Matching"); }
