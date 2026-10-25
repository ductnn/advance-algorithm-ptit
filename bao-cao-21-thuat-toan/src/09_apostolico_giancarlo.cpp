// Thuật toán Apostolico-Giancarlo: biến thể của Boyer-Moore, lưu skip[i] = độ
// dài hậu tố của mẫu đã khớp kết thúc tại vị trí i của cửa sổ, kết hợp với
// bảng suff để nhảy qua các đoạn chắc chắn khớp/không khớp.
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

void AG(char *x, int m, char *y, int n) {
  int i, j, k, s, shift;
  std::vector<int> bmGs(m), skip(m, 0), suff(m);
  int bmBc[ASIZE];

  /* Tiền xử lý */
  preBmGs(x, m, bmGs.data());
  preBmBc(x, m, bmBc);
  suffixes(x, m, suff.data());
  VET_BANG("bmGs", bmGs.data(), m);
  VET_BANG("suff", suff.data(), m);

  /* Tìm kiếm */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    i = m - 1;
    while (i >= 0) {
      k = skip[i];  // độ dài đoạn đã khớp (biết từ các lần thử trước)
      s = suff[i];
      if (k > 0)
        if (k > s) {
          if (i + 1 == s) i = (-1);  // chắc chắn có xuất hiện
          else i -= s;               // chắc chắn không khớp tại i - s
          break;
        } else {
          i -= k;
          if (k < s) break;
        }
      else {
        if (CMP(i, i + j)) --i;
        else break;
      }
    }
    if (i < 0) {
      OUTPUT(j);
      skip[m - 1] = m;
      shift = bmGs[0];
    } else {
      skip[m - 1] = m - 1 - i;
      shift = MAX(bmGs[i], bmBc[U(y[i + j])] - m + 1 + i);
    }
    j += shift;
    // dịch bảng skip theo cửa sổ mới
    memmove(skip.data(), skip.data() + shift, (m - shift) * sizeof(int));
    memset(skip.data() + m - shift, 0, shift * sizeof(int));
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, AG, "Apostolico-Giancarlo"); }
