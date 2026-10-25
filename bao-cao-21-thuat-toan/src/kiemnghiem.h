// kiemnghiem.h — Bộ công cụ kiểm nghiệm dùng chung cho 21 thuật toán.
//  - Đếm số phép so sánh ký tự giữa mẫu x và văn bản y (CMP).
//  - Đếm các thao tác cơ sở khác: so sánh giá trị băm, chuyển trạng thái,
//    tra bảng dịch chuyển... (THAOTAC).
//  - Ghi vết (trace) từng lần thử ra stderr khi chạy với tham số --vet.
//  - Hàm main dùng chung: chạy trên ví dụ chuẩn hoặc trên hai tệp x, y.
#pragma once
#include <algorithm>
#include <cstdarg>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

#define ASIZE 256                      // kích thước bảng chữ cái (ASCII mở rộng)
#define U(c) ((unsigned char)(c))      // ký tự -> chỉ số bảng (0..255)
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define MIN(a, b) ((a) < (b) ? (a) : (b))

static long long soSoSanh = 0;   // số phép so sánh ký tự x[i] với y[j]
static long long soThaoTac = 0;  // số thao tác cơ sở khác (tùy thuật toán)
static long long soLanXuatHien = 0;
static bool ghiVet = false;      // bật ghi vết khi chạy với --vet

// In một dòng vết ra stderr (chỉ khi bật ghi vết).
static void VET(const char *fmt, ...) {
  if (!ghiVet) return;
  va_list ap;
  va_start(ap, fmt);
  vfprintf(stderr, fmt, ap);
  va_end(ap);
  fputc('\n', stderr);
}

// Ghi vết một bảng tiền xử lý a[0..len-1] (để in minh họa trong báo cáo).
static void VET_BANG(const char *ten, const int *a, int len) {
  if (!ghiVet) return;
  fprintf(stderr, "P %s", ten);
  for (int i = 0; i < len; ++i) fprintf(stderr, " %d", a[i]);
  fputc('\n', stderr);
}

// So sánh x[i] với y[j], có đếm và ghi vết. Dùng qua macro CMP(i, j).
static inline bool soSanh(const char *x, int i, const char *y, int j) {
  ++soSoSanh;
  bool kq = (x[i] == y[j]);
  VET("C %d %d %d", i, j, kq ? 1 : 0);
  return kq;
}
#define CMP(i, j) soSanh(x, (i), y, (j))

// Đánh dấu bắt đầu một lần thử: cửa sổ y[j .. j+m-1].
static inline void ATTEMPT(int j) { VET("A %d", j); }

// Đếm một thao tác cơ sở khác trên ký tự văn bản y[j].
static inline void THAOTAC(int j) {
  ++soThaoTac;
  VET("R %d", j);
}

// Báo một vị trí xuất hiện của mẫu.
static void OUTPUT(int j) {
  ++soLanXuatHien;
  printf("Tim thay mau tai vi tri j = %d\n", j);
}

typedef void (*ThuatToan)(char *x, int m, char *y, int n);

static std::string docTep(const char *ten) {
  std::string s;
  FILE *f = fopen(ten, "rb");
  if (!f) { perror(ten); exit(1); }
  int c;
  while ((c = fgetc(f)) != EOF)
    if (c != '\n' && c != '\r') s.push_back((char)c);
  fclose(f);
  return s;
}

// main dùng chung:
//   ./prog            : chạy trên ví dụ chuẩn x = GCAGAGAG
//   ./prog --vet      : như trên, kèm ghi vết từng bước ra stderr
//   ./prog tepX tepY  : chạy trên mẫu/văn bản đọc từ tệp (kiểm nghiệm)
static int chayChuongTrinh(int argc, char **argv, ThuatToan f, const char *ten) {
  std::string sx = "GCAGAGAG";
  std::string sy = "GCATCGCAGAGAGTATACAGTACG";
  if (argc >= 2 && strcmp(argv[1], "--vet") == 0) ghiVet = true;
  else if (argc >= 3) { sx = docTep(argv[1]); sy = docTep(argv[2]); }
  int m = (int)sx.size(), n = (int)sy.size();
  // Đệm thêm m + 2 ký tự '\0' sau văn bản để các thuật toán đọc y[n], y[n+1]
  // (Quick Search, Berry-Ravindran) hoặc đặt lính canh (Tuned Boyer-Moore).
  std::vector<char> x(sx.begin(), sx.end()), y(sy.begin(), sy.end());
  x.resize(m + 2, '\0');
  y.resize(n + m + 2, '\0');
  printf("Thuat toan: %s\n", ten);
  if (n <= 80) printf("x = %s (m = %d)\ny = %s (n = %d)\n", sx.c_str(), m, sy.c_str(), n);
  else printf("m = %d, n = %d\n", m, n);
  f(x.data(), m, y.data(), n);
  printf("So lan xuat hien: %lld\n", soLanXuatHien);
  printf("So phep so sanh ky tu: %lld\n", soSoSanh);
  printf("So thao tac khac: %lld\n", soThaoTac);
  return 0;
}
