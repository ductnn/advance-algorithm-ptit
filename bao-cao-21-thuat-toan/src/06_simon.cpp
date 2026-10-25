// Thuật toán Simon: dùng automat đoán nhận Σ*x nhưng chỉ lưu các cung "có ý
// nghĩa" (cung lùi không về trạng thái đầu). Số cung như vậy không quá m.
#include "kiemnghiem.h"

// L[p] = danh sách đích của các cung có ý nghĩa đi ra từ trạng thái p
// (p = chỉ số ký tự cuối của tiền tố đã khớp, từ -1 đến m-1).
typedef std::vector<std::vector<int> > DanhSach;

// Trả về trạng thái kế tiếp từ p khi đọc y[j]; -1 nếu quay về trạng thái đầu.
int getTransition(char *x, int m, int p, DanhSach &L, char *y, int j) {
  if (p < m - 1 && CMP(p + 1, j)) return (p + 1);  // cung tiến
  else if (p > -1) {
    // duyệt danh sách cung lùi (phần tử thêm sau được duyệt trước)
    for (int t = (int)L[p].size() - 1; t >= 0; --t)
      if (CMP(L[p][t], j)) return (L[p][t]);
    return (-1);
  } else
    return (-1);
}

void setTransition(int p, int q, DanhSach &L) { L[p].push_back(q); }

int preSimon(char *x, int m, DanhSach &L) {
  int i, k, ell;
  L.assign(m, std::vector<int>());
  ell = -1;
  for (i = 1; i < m; ++i) {
    k = ell;
    std::vector<int> cell = (ell == -1 ? std::vector<int>() : L[k]);
    ell = -1;
    if (x[i] == x[k + 1]) ell = k + 1;
    else setTransition(i - 1, k + 1, L);
    for (int t = (int)cell.size() - 1; t >= 0; --t) {
      k = cell[t];
      if (x[i] == x[k]) ell = k;
      else setTransition(i - 1, k, L);
    }
  }
  return (ell);
}

void SIMON(char *x, int m, char *y, int n) {
  int j, ell, state;
  DanhSach L;

  /* Tiền xử lý */
  ell = preSimon(x, m, L);
  for (int p = 0; p < m; ++p) {
    std::string s;
    for (int q : L[p]) s += std::to_string(q) + " ";
    VET("L %d %s", p, s.c_str());
  }

  /* Tìm kiếm */
  for (state = -1, j = 0; j < n; ++j) {
    int truoc = state;
    state = getTransition(x, m, state, L, y, j);
    VET("S %d %d %d", j, truoc, state);
    if (state >= m - 1) {
      OUTPUT(j - m + 1);
      state = ell;
    }
  }
}

int main(int argc, char **argv) { return chayChuongTrinh(argc, argv, SIMON, "Simon"); }
