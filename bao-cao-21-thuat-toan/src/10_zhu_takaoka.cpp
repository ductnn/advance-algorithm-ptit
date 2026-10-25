// Thuật toán Zhu-Takaoka: biến thể của Boyer-Moore, bảng ký tự tồi được tính
// theo CẶP hai ký tự cuối cửa sổ y[j+m-2] y[j+m-1].
#include "kiemnghiem.h"

// suff[i] = độ dài hậu tố chung dài nhất của x[0..i] và x.
void suffixes(char *x, int m, int *suff) {
  int f = 0, g, i;
  suff[m - 1] = m;
  g = m - 1;
  for (i = m - 2; i >= 0; --i) {
    if (i > g && suff[i + m - 1 - f] < i - g)
      suff[i] = suff[i + m - 1 - f];
    else {
      if (i < g) g = i;
      f = i;
      while (g >= 0 && x[g] == x[g + m - 1 - f]) --g;
      suff[i] = f - g;
    }
  }
}

// Bảng hậu tố tốt (good-suffix): bmGs[i] = độ dịch an toàn khi x[i] không
// khớp còn x[i+1..m-1] đã khớp.
void preBmGs(char *x, int m, int bmGs[]) {
  int i, j;
  std::vector<int> suff(m);
  suffixes(x, m, suff.data());
  for (i = 0; i < m; ++i) bmGs[i] = m;
  j = 0;
  for (i = m - 1; i >= 0; --i)
    if (suff[i] == i + 1)
      for (; j < m - 1 - i; ++j)
        if (bmGs[j] == m) bmGs[j] = m - 1 - i;
  for (i = 0; i <= m - 2; ++i) bmGs[m - 1 - suff[i]] = m - 1 - i;
}

// ztBc[a][b] = độ dịch khi hai ký tự cuối cửa sổ là "ab".
void preZtBc(char *x, int m, std::vector<std::vector<int> > &ztBc) {
  int i;
  ztBc.assign(ASIZE, std::vector<int>(ASIZE, m));
  for (i = 0; i < ASIZE; ++i) ztBc[i][U(x[0])] = m - 1;
  for (i = 1; i < m - 1; ++i) ztBc[U(x[i - 1])][U(x[i])] = m - 1 - i;
}

void ZT(char *x, int m, char *y, int n) {
  int i, j;
  std::vector<std::vector<int> > ztBc;
  std::vector<int> bmGs(m);

  /* Tiền xử lý */
  preZtBc(x, m, ztBc);
  preBmGs(x, m, bmGs.data());
  VET_BANG("bmGs", bmGs.data(), m);

  /* Tìm kiếm */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    i = m - 1;
    while (i >= 0 && CMP(i, i + j)) --i;
    if (i < 0) {
      OUTPUT(j);
      j += bmGs[0];
    } else
      j += MAX(bmGs[i], ztBc[U(y[j + m - 2])][U(y[j + m - 1])]);
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, ZT, "Zhu-Takaoka"); }
