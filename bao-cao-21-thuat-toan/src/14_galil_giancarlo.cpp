// Thuật toán Galil-Giancarlo: cải tiến Colussi khi mẫu bắt đầu bằng một dãy
// ký tự giống nhau x = c^(ell+1) d ... ; khi đó có thể bỏ bớt so sánh nhờ
// nhớ được đoạn văn bản toàn ký tự c đã quét.
#include "kiemnghiem.h"

// Tiền xử lý Colussi. Các vị trí của mẫu được chia làm hai tập:
//  - "lỗ khuyết" (noholes, kmin[i] > 0): so sánh từ trái sang phải trước;
//  - "lỗ" (holes, kmin[i] == 0): so sánh từ phải sang trái sau.
// h[] là thứ tự so sánh; shift[], next[] là độ dịch và vị trí tiếp tục.
int preColussi(char *x, int m, int h[], int next[], int shift[]) {
  int i, k, nd, q, r = 0, s;
  std::vector<int> hmax(m + 2), kmin(m + 2), nhd0(m + 2), rmin(m + 2);

  /* Tính hmax */
  i = k = 1;
  do {
    while (x[i] == x[i - k]) i++;
    hmax[k] = i;
    q = k + 1;
    while (hmax[q - k] + k < i) {
      hmax[q] = hmax[q - k] + k;
      q++;
    }
    k = q;
    if (k == i + 1) i = k;
  } while (k <= m);

  /* Tính kmin */
  for (i = 0; i < m; ++i) kmin[i] = 0;
  for (i = m; i >= 1; --i)
    if (hmax[i] < m) kmin[hmax[i]] = i;

  /* Tính rmin */
  for (i = m - 1; i >= 0; --i) {
    if (hmax[i + 1] == m) r = i + 1;
    if (kmin[i] == 0) rmin[i] = r;
    else rmin[i] = 0;
  }

  /* Tính h: noholes trước (tăng dần), holes sau (giảm dần) */
  s = -1;
  r = m;
  for (i = 0; i < m; ++i)
    if (kmin[i] == 0) h[--r] = i;
    else h[++s] = i;
  nd = s;

  /* Tính shift */
  for (i = 0; i <= nd; ++i) shift[i] = kmin[h[i]];
  for (i = nd + 1; i < m; ++i) shift[i] = rmin[h[i]];
  shift[m] = rmin[0];

  /* Tính nhd0: số noholes đứng trước vị trí i */
  s = 0;
  for (i = 0; i < m; ++i) {
    nhd0[i] = s;
    if (kmin[i] > 0) ++s;
  }

  /* Tính next */
  for (i = 0; i <= nd; ++i) next[i] = nhd0[h[i] - kmin[h[i]]];
  for (i = nd + 1; i < m; ++i) next[i] = nhd0[m - rmin[h[i]]];
  next[m] = nhd0[m - rmin[h[m - 1]]];

  return (nd);
}

void GG(char *x, int m, char *y, int n) {
  int i, j, k, ell, last, nd;
  std::vector<int> h(m + 1), next(m + 1), shift(m + 1);
  char heavy;

  for (ell = 0; ell + 1 < m && x[ell] == x[ell + 1]; ell++);
  if (ell == m - 1) {
    /* Trường hợp đặc biệt: mẫu là lũy thừa của một ký tự */
    for (j = ell = 0; j < n; ++j) {
      ATTEMPT(j - ell);
      if (CMP(0, j)) {
        ++ell;
        if (ell >= m) OUTPUT(j - m + 1);
      } else
        ell = 0;
    }
  } else {
    /* Tiền xử lý */
    nd = preColussi(x, m, h.data(), next.data(), shift.data());
    VET_BANG("h", h.data(), m);
    VET_BANG("next", next.data(), m + 1);
    VET_BANG("shift", shift.data(), m + 1);
    VET("N %d %d", nd, ell);

    /* Tìm kiếm */
    i = j = heavy = 0;
    last = -1;
    while (j <= n - m) {
      ATTEMPT(j);
      if (heavy && i == 0) {
        // Quét tiếp dãy ký tự x[0] bắt đầu từ last + 1
        k = last - j + 1;
        while (CMP(0, j + k)) k++;
        if (k <= ell || !CMP(ell + 1, j + k)) {
          i = 0;
          j += (k + 1);
          last = j - 1;
        } else {
          i = 1;
          last = j + k;
          j = last - (ell + 1);
        }
        heavy = 0;
      } else {
        while (i < m && last < j + h[i] && CMP(h[i], j + h[i])) ++i;
        if (i >= m || last >= j + h[i]) {
          OUTPUT(j);
          i = m;
        }
        if (i > nd) last = j + m - 1;
        j += shift[i];
        i = next[i];
      }
      heavy = (j > last ? 0 : 1);
    }
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, GG, "Galil-Giancarlo"); }
