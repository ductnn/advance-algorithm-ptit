// Thuật toán Optimal Mismatch: so sánh các ký tự của mẫu theo thứ tự tần suất
// xuất hiện TĂNG DẦN trong văn bản (ký tự hiếm trước) để phát hiện không khớp
// sớm nhất; dịch theo max(hậu tố tốt thích nghi, Quick Search).
#include "kiemnghiem.h"

int freq[ASIZE];  // tần suất ký tự (ở đây được đếm trực tiếp trên văn bản)

// Bảng dịch Quick Search: qsBc[c] = m - (vị trí xuất hiện cuối của c trong x);
// bằng m + 1 nếu c không có trong x.
void preQsBc(char *x, int m, int qsBc[]) {
  int i;
  for (i = 0; i < ASIZE; ++i) qsBc[i] = m + 1;
  for (i = 0; i < m; ++i) qsBc[U(x[i])] = m - i;
}
// Mỗi phần tử: vị trí loc trong mẫu và ký tự c = x[loc].
typedef struct patternScanOrder {
  int loc;
  char c;
} pattern;

// Sắp xếp m vị trí của mẫu theo thứ tự so sánh (hàm so sánh pcmp);
// phần tử pat[m] (ký tự kết thúc) giữ nguyên ở cuối.
void orderPattern(char *x, int m, bool (*pcmp)(const pattern &, const pattern &), pattern *pat) {
  int i;
  for (i = 0; i <= m; ++i) {
    pat[i].loc = i;
    pat[i].c = x[i];
  }
  std::sort(pat, pat + m, pcmp);
}

// Tìm độ dịch nhỏ nhất >= lshift sao cho ploc phần tử đầu tiên (theo thứ tự
// so sánh) của mẫu vẫn khớp sau khi dịch.
int matchShift(char *x, int m, int ploc, int lshift, pattern *pat) {
  int i, j;
  for (; lshift < m; ++lshift) {
    i = ploc;
    while (--i >= 0) {
      if ((j = (pat[i].loc - lshift)) < 0) continue;
      if (pat[i].c != x[j]) break;
    }
    if (i < 0) break;
  }
  return (lshift);
}

// Bảng hậu tố tốt thích nghi: adaptedGs[ploc] = độ dịch khi ploc phần tử đầu
// đã khớp và phần tử thứ ploc không khớp.
void preAdaptedGs(char *x, int m, int adaptedGs[], pattern *pat) {
  int lshift, i, ploc;
  adaptedGs[0] = lshift = 1;
  for (ploc = 1; ploc <= m; ++ploc) {
    lshift = matchShift(x, m, ploc, lshift, pat);
    adaptedGs[ploc] = lshift;
  }
  for (ploc = 0; ploc <= m; ++ploc) {
    lshift = adaptedGs[ploc];
    while (lshift < m) {
      i = pat[ploc].loc - lshift;
      if (i < 0 || pat[ploc].c != x[i]) break;
      ++lshift;
      lshift = matchShift(x, m, ploc, lshift, pat);
    }
    adaptedGs[ploc] = lshift;
  }
}

// Ký tự hiếm hơn đứng trước; cùng tần suất thì vị trí lớn hơn đứng trước.
bool optimalPcmp(const pattern &pat1, const pattern &pat2) {
  int fx = freq[U(pat1.c)] - freq[U(pat2.c)];
  return (fx ? fx < 0 : pat2.loc < pat1.loc);
}

void OM(char *x, int m, char *y, int n) {
  int i, j;
  std::vector<int> adaptedGs(m + 1);
  std::vector<pattern> pat(m + 1);
  int qsBc[ASIZE];

  /* Tiền xử lý */
  memset(freq, 0, sizeof(freq));
  for (j = 0; j < n; ++j) ++freq[U(y[j])];
  orderPattern(x, m, optimalPcmp, pat.data());
  preQsBc(x, m, qsBc);
  preAdaptedGs(x, m, adaptedGs.data(), pat.data());
  VET_BANG("adaptedGs", adaptedGs.data(), m + 1);
  for (i = 0; i < m; ++i) VET("O %d", pat[i].loc);

  /* Tìm kiếm: so sánh theo thứ tự pat[0], pat[1], ... */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    i = 0;
    while (i < m && CMP(pat[i].loc, j + pat[i].loc)) ++i;
    if (i >= m) OUTPUT(j);
    j += MAX(adaptedGs[i], qsBc[U(y[j + m])]);
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, OM, "Optimal Mismatch"); }
