"""Chạy kiểm nghiệm thực nghiệm 21 chương trình trên các bộ dữ liệu ngẫu nhiên.

Mỗi chương trình được gọi dạng `prog tepX tepY`; kết quả (số lần xuất hiện,
số phép so sánh ký tự, số thao tác khác) được ghi vào tools/ketqua.json.
"""
import glob, json, os, random, re, subprocess, sys

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(GOC, 'bin')
TMP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(GOC, 'data')
os.makedirs(TMP, exist_ok=True)

random.seed(2026)
N = 1_000_000


def ngau_nhien(sigma, n):
    return ''.join(random.choice(sigma) for _ in range(n))


KICH_BAN = []
dna = ngau_nhien('ACGT', N)
latin = ngau_nhien('abcdefghijklmnopqrstuvwxyz', N)
for ten, y, m in [('DNA (σ = 4), m = 8', dna, 8), ('DNA (σ = 4), m = 32', dna, 32),
                  ('Chữ cái Latin (σ = 26), m = 8', latin, 8),
                  ('Chữ cái Latin (σ = 26), m = 32', latin, 32)]:
    p = random.randrange(N - m)
    KICH_BAN.append((ten, y[p:p + m], y))
KICH_BAN.append(('Xấu nhất: y = a^n (n = 10^5), x = a^8', 'a' * 8, 'a' * 100_000))

ket_qua = []
for ten, x, y in KICH_BAN:
    open(os.path.join(TMP, 'x.txt'), 'w').write(x)
    open(os.path.join(TMP, 'y.txt'), 'w').write(y)
    mong_doi = sum(1 for i in range(len(y) - len(x) + 1) if y.startswith(x, i))
    dong = {'kich_ban': ten, 'm': len(x), 'n': len(y), 'x': x, 'xuat_hien': mong_doi, 'thuat_toan': {}}
    for b in sorted(glob.glob(BIN + '/*')):
        out = subprocess.run([b, os.path.join(TMP, 'x.txt'), os.path.join(TMP, 'y.txt')],
                             capture_output=True, text=True).stdout
        so = lambda nhan: int(re.search(nhan + r': (\d+)', out).group(1))
        kq = {'xuat_hien': so('So lan xuat hien'), 'so_sanh': so('So phep so sanh ky tu'),
              'thao_tac': so('So thao tac khac')}
        assert kq['xuat_hien'] == mong_doi, (b, ten, kq, mong_doi)
        dong['thuat_toan'][os.path.basename(b)] = kq
    ket_qua.append(dong)
    print('xong:', ten)

json.dump(ket_qua, open(os.path.join(GOC, 'tools', 'ketqua.json'), 'w'), ensure_ascii=False, indent=1)
