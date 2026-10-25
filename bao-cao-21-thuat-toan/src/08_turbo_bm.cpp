// Thuật toán Turbo Boyer-Moore: biến thể của Boyer-Moore, ghi nhớ đoạn văn bản
// đã khớp với hậu tố của mẫu ở lần thử trước để "nhảy qua" khi so sánh và
// cho phép một bước dịch "turbo".
#include "kiemnghiem.h"

// Bảng ký tự tồi (bad-character): bmBc[c] = khoảng cách từ lần xuất hiện
// cuối cùng của c trong x[0..m-2] tới cuối mẫu; bằng m nếu c không xuất hiện.
void preBmBc(char *x, int m, int bmBc[]) {
  int i;
  for (i = 0; i < ASIZE; ++i) bmBc[i] = m;
  for (i = 0; i < m - 1; ++i) bmBc[U(x[i])] = m - i - 1;
}

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

void TBM(char *x, int m, char *y, int n) {
  int bcShift, i, j, shift, u, v, turboShift;
  std::vector<int> bmGs(m);
  int bmBc[ASIZE];

  /* Tiền xử lý */
  preBmGs(x, m, bmGs.data());
  preBmBc(x, m, bmBc);
  VET_BANG("bmGs", bmGs.data(), m);

  /* Tìm kiếm */
  j = u = 0;  // u: độ dài đoạn đã khớp ở lần thử trước (bộ nhớ)
  shift = m;
  while (j <= n - m) {
    ATTEMPT(j);
    i = m - 1;
    while (i >= 0 && CMP(i, i + j)) {
      --i;
      if (u != 0 && i == m - 1 - shift) i -= u;  // nhảy qua đoạn đã biết khớp
    }
    if (i < 0) {
      OUTPUT(j);
      shift = bmGs[0];
      u = m - shift;
    } else {
      v = m - 1 - i;
      turboShift = u - v;
      bcShift = bmBc[U(y[i + j])] - m + 1 + i;
      shift = MAX(turboShift, bcShift);
      shift = MAX(shift, bmGs[i]);
      if (shift == bmGs[i])
        u = MIN(m - shift, v);
      else {
        if (turboShift < bcShift) shift = MAX(shift, u + 1);
        u = 0;
      }
    }
    j += shift;
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, TBM, "Turbo Boyer-Moore"); }
