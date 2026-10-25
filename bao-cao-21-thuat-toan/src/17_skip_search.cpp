// Thuật toán Skip Search: chỉ "nhìn" các ký tự văn bản y[m-1], y[2m-1], ...
// (bước nhảy m). Với mỗi ký tự c nhìn thấy, thử mọi cách đặt mẫu sao cho
// một lần xuất hiện của c trong x trùng với nó (dùng các "thùng" z[c]).
#include "kiemnghiem.h"

void SKIP(char *x, int m, char *y, int n) {
  int i, j, k;
  std::vector<std::vector<int> > z(ASIZE);

  /* Tiền xử lý: z[c] = danh sách vị trí của c trong x (vị trí lớn đứng trước) */
  for (i = m - 1; i >= 0; --i) z[U(x[i])].push_back(i);

  /* Tìm kiếm */
  for (j = m - 1; j < n; j += m) {
    THAOTAC(j);  // tra thùng của ký tự y[j]
    for (int t = 0; t < (int)z[U(y[j])].size(); ++t) {
      int p = z[U(y[j])][t];
      if (j - p > n - m) continue;  // cửa sổ vượt quá cuối văn bản
      ATTEMPT(j - p);
      k = 0;
      while (k < m && CMP(k, j - p + k)) ++k;
      if (k == m) OUTPUT(j - p);
    }
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, SKIP, "Skip Search"); }
