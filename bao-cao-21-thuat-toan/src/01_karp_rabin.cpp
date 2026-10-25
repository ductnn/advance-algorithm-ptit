// Thuật toán Karp-Rabin: dùng hàm băm "cuộn" (rolling hash) để lọc nhanh
// các cửa sổ; chỉ so sánh từng ký tự khi giá trị băm của cửa sổ bằng băm của mẫu.
#include "kiemnghiem.h"

// Tính lại giá trị băm khi trượt cửa sổ: bỏ ký tự a ở đầu, thêm ký tự b ở cuối.
// Phép tính trên số nguyên không dấu 32 bit, tức là lấy theo modulo 2^32.
#define REHASH(a, b, h) ((((h) - (a) * d) << 1) + (b))

void KR(char *x, int m, char *y, int n) {
  unsigned int d, hx, hy;
  int i, j;

  /* Tiền xử lý: d = 2^(m-1) dùng để loại ký tự đầu cửa sổ */
  for (d = i = 1; i < m; ++i) d = (d << 1);
  for (hy = hx = i = 0; i < m; ++i) {
    hx = ((hx << 1) + U(x[i]));
    hy = ((hy << 1) + U(y[i]));
  }

  /* Tìm kiếm */
  j = 0;
  while (j <= n - m) {
    ATTEMPT(j);
    THAOTAC(j);  // một phép so sánh giá trị băm hx == hy
    VET("H %d %u %u", j, hy, hx);
    if (hx == hy) {
      // Băm trùng: kiểm tra lại từng ký tự để loại trường hợp đụng độ
      i = 0;
      while (i < m && CMP(i, j + i)) ++i;
      if (i == m) OUTPUT(j);
    }
    hy = REHASH(U(y[j]), U(y[j + m]), hy);
    ++j;
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, KR, "Karp-Rabin"); }
