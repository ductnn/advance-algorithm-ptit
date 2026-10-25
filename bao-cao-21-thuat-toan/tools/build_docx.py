# -*- coding: utf-8 -*-
"""Sinh báo cáo Word cho 21 thuật toán đối sánh mẫu.

Cách dùng:  python build_docx.py <đường_dẫn_docx_đầu_ra>
Yêu cầu: python-docx; các chương trình đã biên dịch trong ../bin;
         kết quả kiểm nghiệm trong tools/ketqua.json (do kiem_nghiem.py sinh ra).
"""
import json
import os
import re
import subprocess
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from noi_dung import NHOM, THUAT_TOAN  # noqa: E402

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THU_MUC_GOC = os.path.dirname(GOC)
BIN = os.path.join(GOC, 'bin')
SRC = os.path.join(GOC, 'src')
BIA = os.path.join(THU_MUC_GOC, 'BiaTieuLuan.docx')
DAU_RA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(THU_MUC_GOC, 'draft.docx')

X = 'GCAGAGAG'
Y = 'GCATCGCAGAGAGTATACAGTACG'
M, N = len(X), len(Y)
ABC = 'ACGT'

FONT = 'Times New Roman'
FONT_MA = 'Courier New'
XANH_DAM = RGBColor(0x17, 0x36, 0x5D)
NEN_TIEU_DE = 'DDEBF7'
NEN_KHOP = 'C6EFCE'
NEN_LECH = 'FFC7CE'
NEN_MA = 'F5F5F5'

KET_QUA = json.load(open(os.path.join(GOC, 'tools', 'ketqua.json')))
TEN_KICH_BAN_NGAN = ['DNA, m=8', 'DNA, m=32', 'Latin, m=8', 'Latin, m=32', 'Xấu nhất']


# ----------------------------------------------------------------------------- tiện ích XML
def dat_font(rpr_owner, ten=FONT):
    """Gán font cho mọi bảng mã (ascii, hAnsi, eastAsia, cs), bỏ font theo theme."""
    rpr = rpr_owner.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.insert(0, rf)
    for k in list(rf.attrib):
        if 'Theme' in k or 'theme' in k:
            del rf.attrib[k]
    for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'):
        rf.set(qn(k), ten)


def to_nen(cell, mau):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), mau)
    tcpr.append(shd)


def vien_bang(table, mau='808080', co=4):
    tblpr = table._tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for canh in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement('w:' + canh)
        e.set(qn('w:val'), 'single')
        e.set(qn('w:sz'), str(co))
        e.set(qn('w:space'), '0')
        e.set(qn('w:color'), mau)
        borders.append(e)
    tblpr.append(borders)


def le_o(table, trai_phai=60):
    tblpr = table._tbl.tblPr
    mar = OxmlElement('w:tblCellMar')
    for canh, v in (('left', trai_phai), ('right', trai_phai), ('top', 0), ('bottom', 0)):
        e = OxmlElement('w:' + canh)
        e.set(qn('w:w'), str(v))
        e.set(qn('w:type'), 'dxa')
        mar.append(e)
    tblpr.append(mar)


def co_dinh_bang(table, widths_cm):
    table.autofit = False
    tblpr = table._tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblpr.append(layout)
    grid = table._tbl.tblGrid
    for gc, w in zip(grid.findall(qn('w:gridCol')), widths_cm):
        gc.set(qn('w:w'), str(int(w * 567)))
    for row in table.rows:
        for cell, w in zip(row.cells, widths_cm):
            cell.width = Cm(w)


def lap_lai_tieu_de(row):
    trpr = row._tr.get_or_add_trPr()
    e = OxmlElement('w:tblHeader')
    e.set(qn('w:val'), 'true')
    trpr.append(e)


def khong_tach_dong(row):
    trpr = row._tr.get_or_add_trPr()
    trpr.append(OxmlElement('w:cantSplit'))


def them_truong(paragraph, lenh, giu_cho=''):
    """Chèn một field (PAGE, TOC, ...) vào đoạn văn."""
    r = paragraph.add_run()
    fc = OxmlElement('w:fldChar')
    fc.set(qn('w:fldCharType'), 'begin')
    r._r.append(fc)
    r = paragraph.add_run()
    it = OxmlElement('w:instrText')
    it.set(qn('xml:space'), 'preserve')
    it.text = lenh
    r._r.append(it)
    r = paragraph.add_run()
    fc = OxmlElement('w:fldChar')
    fc.set(qn('w:fldCharType'), 'separate')
    r._r.append(fc)
    paragraph.add_run(giu_cho)
    r = paragraph.add_run()
    fc = OxmlElement('w:fldChar')
    fc.set(qn('w:fldCharType'), 'end')
    r._r.append(fc)


# ----------------------------------------------------------------------------- tài liệu
class BaoCao:
    def __init__(self):
        self.doc = Document(BIA)
        self.chuong = 0
        self.so_bang = 0
        self._cau_hinh_style()
        self._sua_bia()
        self._tao_section_noi_dung()

    # ---- cấu hình chung
    def _cau_hinh_style(self):
        st = self.doc.styles['Normal']
        dat_font(st.element)
        st.font.size = Pt(13)
        rpr = st.element.get_or_add_rPr()
        lang = OxmlElement('w:lang')
        lang.set(qn('w:val'), 'vi-VN')
        rpr.append(lang)
        pf = st.paragraph_format
        pf.space_after = Pt(6)
        pf.line_spacing = 1.3
        for ten, co, can_giua in (('Heading 1', 15, True), ('Heading 2', 14, False), ('Heading 3', 13, False)):
            s = self.doc.styles[ten]
            dat_font(s.element)
            s.font.size = Pt(co)
            s.font.bold = True
            s.font.italic = (ten == 'Heading 3')
            s.font.color.rgb = XANH_DAM
            s.paragraph_format.space_before = Pt(12 if ten != 'Heading 1' else 0)
            s.paragraph_format.space_after = Pt(6 if ten != 'Heading 1' else 18)
            s.paragraph_format.keep_with_next = True
            s.paragraph_format.line_spacing = 1.15
            if can_giua:
                s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        # Word tự cập nhật mục lục khi mở tệp
        if not os.environ.get('KHONG_CAP_NHAT_TRUONG'):
            settings = self.doc.settings.element
            uf = OxmlElement('w:updateFields')
            uf.set(qn('w:val'), 'true')
            settings.append(uf)

    def _sua_bia(self):
        ps = self.doc.paragraphs
        mon = ps[5]
        for r in mon.runs[1:]:
            r._r.getparent().remove(r._r)
        mon.runs[0].text = 'MÔN: CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT NÂNG CAO'
        mon.runs[0].font.size = Pt(16)
        mon.paragraph_format.space_after = Pt(18)
        # Tên chuyên đề, chèn ngay sau dòng tên môn
        chen = []
        for text, co, dam, nghieng, sau in (
                ('CHUYÊN ĐỀ', 14, True, False, 4),
                ('CÁC THUẬT TOÁN ĐỐI SÁNH MẪU', 20, True, False, 4),
                ('(EXACT STRING-MATCHING ALGORITHMS)', 14, True, False, 10),
                ('Trình bày, đánh giá, kiểm nghiệm và lập trình 21 thuật toán', 13, False, True, 40)):
            p = self.doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(sau)
            r = p.add_run(text)
            r.font.size = Pt(co)
            r.bold = dam
            r.italic = nghieng
            r.font.color.rgb = XANH_DAM
            chen.append(p)
        moc = mon._p
        for p in chen:
            moc.addnext(p._p)
            moc = p._p

    def _tao_section_noi_dung(self):
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        sp = sec._sectPr
        for tag in ('w:pgBorders', 'w:headerReference', 'w:footerReference'):
            for e in sp.findall(qn(tag)):
                sp.remove(e)
        pg = OxmlElement('w:pgNumType')
        pg.set(qn('w:start'), '1')
        sp.append(pg)
        sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)
        sec.left_margin, sec.right_margin = Cm(3), Cm(2)
        sec.header.is_linked_to_previous = False
        sec.footer.is_linked_to_previous = False
        fp = sec.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        them_truong(fp, 'PAGE', '1')
        hp = sec.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = hp.add_run('Chuyên đề: Các thuật toán đối sánh mẫu')
        r.italic = True
        r.font.size = Pt(10)
        r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

    # ---- khối văn bản
    def doan(self, text, can='justify', nghieng=False, dam=False, co=None, sau=None, thut=True):
        p = self.doc.add_paragraph()
        self._noi_tuyen(p, text, nghieng=nghieng, dam=dam, co=co)
        p.alignment = {'justify': WD_ALIGN_PARAGRAPH.JUSTIFY, 'center': WD_ALIGN_PARAGRAPH.CENTER,
                       'left': WD_ALIGN_PARAGRAPH.LEFT}[can]
        if thut and can == 'justify':
            p.paragraph_format.first_line_indent = Cm(1)
        if sau is not None:
            p.paragraph_format.space_after = Pt(sau)
        return p

    def _noi_tuyen(self, p, text, nghieng=False, dam=False, co=None):
        text = text.replace('Σ*', 'Σ∗')
        for phan in re.split(r'(\*\*.+?\*\*|\*[^*]+?\*|`[^`]+?`)', text):
            if not phan:
                continue
            if phan.startswith('**'):
                r = p.add_run(phan[2:-2])
                r.bold = True
            elif phan.startswith('*') and len(phan) > 2:
                r = p.add_run(phan[1:-1])
                r.italic = True
            elif phan.startswith('`'):
                r = p.add_run(phan[1:-1])
                dat_font(r._r, FONT_MA)
                r.font.size = Pt(11)
            else:
                r = p.add_run(phan)
            if nghieng:
                r.italic = True
            if dam:
                r.bold = True
            if co:
                r.font.size = Pt(co)

    def gach(self, text, cap=0):
        p = self.doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(1.0 + 0.8 * cap)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.space_after = Pt(3)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.add_run('–\t' if cap else '•\t')
        p.paragraph_format.tab_stops.add_tab_stop(Cm(1.0 + 0.8 * cap))
        self._noi_tuyen(p, text)

    def muc_nho(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.italic = True

    def cong_thuc(self, text):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(text)
        dat_font(r._r, FONT_MA)
        r.font.size = Pt(11)

    def tieu_de(self, text, cap):
        h = self.doc.add_heading(text, level=cap)
        return h

    def ngat_trang(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def chu_thich_bang(self, text):
        self.so_bang += 1
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run('Bảng %d.%d. ' % (self.chuong, self.so_bang))
        r.bold = True
        r.italic = True
        r.font.size = Pt(11)
        r = p.add_run(text)
        r.italic = True
        r.font.size = Pt(11)

    # ---- bảng
    def bang(self, rows, widths, tieu_de=1, co=10.5, can=None, chu_thich=None, dam_cot_dau=False):
        if chu_thich:
            self.chu_thich_bang(chu_thich)
        t = self.doc.add_table(rows=len(rows), cols=len(rows[0]))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        vien_bang(t)
        le_o(t, 80)
        for ri, row in enumerate(rows):
            for ci, val in enumerate(row):
                cell = t.cell(ri, ci)
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.first_line_indent = Cm(0)
                a = (can[ci] if can else 'center')
                p.alignment = {'center': WD_ALIGN_PARAGRAPH.CENTER, 'left': WD_ALIGN_PARAGRAPH.LEFT,
                               'justify': WD_ALIGN_PARAGRAPH.JUSTIFY}[a]
                self._noi_tuyen(p, str(val), co=co, dam=(ri < tieu_de) or (dam_cot_dau and ci == 0))
                if ri < tieu_de:
                    to_nen(cell, NEN_TIEU_DE)
            if ri < tieu_de:
                lap_lai_tieu_de(t.rows[ri])
            khong_tach_dong(t.rows[ri])
        co_dinh_bang(t, widths)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)
        return t

    def khoi_ma(self, code, co=8):
        t = self.doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        vien_bang(t, 'BFBFBF', 4)
        le_o(t, 100)
        cell = t.cell(0, 0)
        to_nen(cell, NEN_MA)
        dong = code.rstrip('\n').split('\n')
        for k, line in enumerate(dong):
            p = cell.paragraphs[0] if k == 0 else cell.add_paragraph()
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.first_line_indent = Cm(0)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(line.replace('\t', '    ') if line else ' ')
            dat_font(r._r, FONT_MA)
            r.font.size = Pt(co)
        co_dinh_bang(t, [16.0])
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def bang_vet(self, attempts, chu_thich, x=X):
        """Bảng mô phỏng từng lần thử: mỗi dòng một cửa sổ, ô tô màu là ký tự được so sánh."""
        self.chu_thich_bang(chu_thich)
        ncol = N + 3
        t = self.doc.add_table(rows=2 + len(attempts), cols=ncol)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        vien_bang(t, 'A6A6A6', 2)
        le_o(t, 10)
        for row in t.rows:
            for cell in row.cells:
                pf = cell.paragraphs[0].paragraph_format
                pf.line_spacing = Pt(11)
                pf.space_after = Pt(0)
                pf.first_line_indent = Cm(0)

        def ghi(cell, text, co=8, dam=False, mau=None, mu=None):
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.line_spacing = Pt(11)
            p.paragraph_format.first_line_indent = Cm(0)
            r = p.add_run(text)
            r.font.size = Pt(co)
            r.bold = dam
            if mau:
                r.font.color.rgb = mau
            if mu:
                r2 = p.add_run(mu)
                r2.font.size = Pt(5.5)
                r2.font.superscript = True

        ghi(t.cell(0, 0), 'j', dam=True)
        ghi(t.cell(1, 0), 'y', dam=True)
        for c in range(N):
            ghi(t.cell(0, c + 1), str(c), co=6.5)
            ghi(t.cell(1, c + 1), Y[c], dam=True)
            to_nen(t.cell(1, c + 1), NEN_TIEU_DE)
        ghi(t.cell(0, N + 1), 'SS', dam=True, co=7)
        ghi(t.cell(0, N + 2), 'Dịch', dam=True, co=7)
        for k, a in enumerate(attempts):
            row = 2 + k
            ghi(t.cell(row, 0), '%d' % (k + 1), co=7.5)
            o = {}
            for thu_tu, (i, tpos, ok) in enumerate(a['ev'], 1):
                o.setdefault(tpos, [i, ok, []])
                o[tpos][1] = o[tpos][1] and ok
                o[tpos][2].append(str(thu_tu))
            for c in range(N):
                cell = t.cell(row, c + 1)
                if c in o:
                    i, ok, ds = o[c]
                    ghi(cell, x[i], dam=True, mu=','.join(ds))
                    to_nen(cell, NEN_KHOP if ok else NEN_LECH)
                elif a['pos'] <= c < a['pos'] + M:
                    ghi(cell, x[c - a['pos']], mau=RGBColor(0x8C, 0x8C, 0x8C))
            ghi(t.cell(row, N + 1), str(a['so']), co=7.5)
            ghi(t.cell(row, N + 2), str(a['dich']), co=7.5)
            khong_tach_dong(t.rows[row])
        lap_lai_tieu_de(t.rows[0])
        lap_lai_tieu_de(t.rows[1])
        co_dinh_bang(t, [0.6] + [0.56] * N + [0.7, 0.8])
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)

    def bang_ngang(self, nhan_dong, gia_tri, chu_thich, to_mau=None):
        """Bảng có cột là các vị trí j = 0..n-1 (dùng cho Shift-Or, automat, Simon)."""
        self.chu_thich_bang(chu_thich)
        t = self.doc.add_table(rows=len(nhan_dong), cols=N + 1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        vien_bang(t, 'A6A6A6', 2)
        le_o(t, 10)
        for ri, nhan in enumerate(nhan_dong):
            for ci in range(N + 1):
                cell = t.cell(ri, ci)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.first_line_indent = Cm(0)
                text = nhan if ci == 0 else str(gia_tri[ri][ci - 1])
                r = p.add_run(text)
                r.font.size = Pt(7.5)
                r.bold = (ci == 0 or ri < 2)
                if ri < 2 and ci > 0:
                    to_nen(cell, NEN_TIEU_DE)
                if to_mau and ci > 0 and to_mau(ri, ci - 1):
                    to_nen(cell, NEN_KHOP)
            khong_tach_dong(t.rows[ri])
        co_dinh_bang(t, [1.5] + [0.6] * N)
        self.doc.add_paragraph().paragraph_format.space_after = Pt(2)


# ----------------------------------------------------------------------------- chạy chương trình
def chay(ten, *args):
    r = subprocess.run([os.path.join(BIN, ten)] + list(args), capture_output=True, text=True)
    return r.stdout, r.stderr.splitlines()


def doc_vet(vet):
    """Tách vết thành các lần thử (A/C/B) và các bảng tiền xử lý (P)."""
    attempts, cur, bang = [], None, {}
    for line in vet:
        t = line.split()
        if not t:
            continue
        if t[0] == 'A':
            pos = int(t[1])
            if cur is None or cur['pos'] != pos:
                cur = {'pos': pos, 'ev': []}
                attempts.append(cur)
        elif t[0] == 'C' and cur is not None:
            cur['ev'].append((int(t[1]), int(t[2]), t[3] == '1'))
        elif t[0] == 'B' and cur is not None:
            tpos = int(t[1])
            cur['ev'].append((tpos - cur['pos'], tpos, t[2] != '-1'))
        elif t[0] == 'P':
            bang[t[1]] = [int(v) for v in t[2:]]
    attempts = [a for a in attempts if a['ev']]
    for k, a in enumerate(attempts):
        a['so'] = len(a['ev'])
        a['dich'] = attempts[k + 1]['pos'] - a['pos'] if k + 1 < len(attempts) else '—'
    return attempts, bang


# ----------------------------------------------------------------------------- bảng tiền xử lý (Python)
def bm_bc(x):
    m = len(x)
    return {c: next((m - 1 - i for i in range(m - 2, -1, -1) if x[i] == c), m) for c in ABC}


def qs_bc(x):
    m = len(x)
    return {c: next((m - i for i in range(m - 1, -1, -1) if x[i] == c), m + 1) for c in ABC}


def zt_bc(x):
    m = len(x)
    z = {a: {b: m for b in ABC} for a in ABC}
    for a in ABC:
        z[a][x[0]] = m - 1
    for i in range(1, m - 1):
        z[x[i - 1]][x[i]] = m - 1 - i
    return z


def br_bc(x):
    m = len(x)
    z = {a: {b: m + 2 for b in ABC} for a in ABC}
    for a in ABC:
        z[a][x[0]] = m + 1
    for i in range(m - 1):
        z[x[i]][x[i + 1]] = m - i
    for a in ABC:
        z[x[m - 1]][a] = 1
    return z


def factor_oracle(x):
    xr = x[::-1]
    m = len(x)
    tr = [dict() for _ in range(m + 1)]
    s = [-1] * (m + 1)
    for i in range(1, m + 1):
        c = xr[i - 1]
        tr[i - 1][c] = i
        k = s[i - 1]
        while k > -1 and c not in tr[k]:
            tr[k][c] = i
            k = s[k]
        s[i] = 0 if k == -1 else tr[k][c]
    ket = set()
    k = m
    while k > -1:
        ket.add(k)
        k = s[k]
    return tr, s, ket


def bang_chi_so(bc, cac_dong, chu_thich, co_m=True):
    """Bảng có cột là chỉ số i của mẫu; cac_dong = [(nhãn, danh sách giá trị)]."""
    k = M + 1 if co_m else M
    rows = [['i'] + [str(i) for i in range(k)], ['x[i]'] + list(X) + ([''] if co_m else [])]
    for nhan, vals in cac_dong:
        rows.append([nhan] + [str(v) for v in vals[:k]] + [''] * (k - len(vals)))
    w = 2.2
    bc.bang(rows, [w] + [min(1.2, 13.5 / k)] * k, tieu_de=1, co=10, chu_thich=chu_thich, dam_cot_dau=True)


def bang_ky_tu(bc, cac_dong, chu_thich, khac=None):
    rows = [['c'] + list(ABC) + (['ký tự khác'] if khac else [])]
    for nhan, d, v_khac in cac_dong:
        rows.append([nhan] + [str(d[c]) for c in ABC] + ([str(v_khac)] if khac else []))
    bc.bang(rows, [2.8] + [1.3] * 4 + ([2.4] if khac else []), co=10.5, chu_thich=chu_thich, dam_cot_dau=True)


def bang_hai_ky_tu(bc, z, ten, chu_thich, khac):
    rows = [['%s[a][b]' % ten] + ['b = %s' % b for b in ABC]]
    for a in ABC:
        rows.append(['a = %s' % a] + [str(z[a][b]) for b in ABC])
    bc.bang(rows, [2.8] + [1.6] * 4, co=10.5, chu_thich=chu_thich, dam_cot_dau=True)
    bc.doan(khac, nghieng=True, co=11)


# ----------------------------------------------------------------------------- phần tiền xử lý từng thuật toán
def tien_xu_ly(bc, tt, bang, vet):
    kieu = tt.get('tien_xu_ly')
    ten = tt['ten'].replace('Thuật toán ', '')
    if kieu == 'mp':
        bang_chi_so(bc, [('mpNext[i]', bang['mpNext'])], 'Bảng mpNext của mẫu x = GCAGAGAG.')
    elif kieu == 'kmp':
        bang_chi_so(bc, [('kmpNext[i]', bang['kmpNext'])], 'Bảng kmpNext của mẫu x = GCAGAGAG.')
    elif kieu == 'nsn':
        bc.doan('Với x = GCAGAGAG: x[0] = G ≠ x[1] = C, do đó **k = 1** (độ dịch khi x[1] không khớp) và '
                '**ell = 2** (độ dịch khi x[1] khớp).')
    elif kieu in ('bm', 'ag'):
        bang_ky_tu(bc, [('bmBc[c]', bm_bc(X), M)], 'Bảng ký tự tồi bmBc của %s.' % ten, khac=True)
        dong = [('suff[i]', bang['suff'])] if kieu == 'ag' else []
        bang_chi_so(bc, dong + [('bmGs[i]', bang['bmGs'])], 'Bảng hậu tố tốt bmGs%s.' %
                    (' và mảng suff' if kieu == 'ag' else ''), co_m=False)
    elif kieu == 'zt':
        bang_hai_ky_tu(bc, zt_bc(X), 'ztBc', 'Bảng ztBc (hai ký tự cuối cửa sổ) thu gọn trên {A, C, G, T}.',
                       'Với các cặp chứa ký tự ngoài mẫu, ztBc = 8 (hoặc 7 nếu b = x[0] = G).')
        bang_chi_so(bc, [('bmGs[i]', bang['bmGs'])], 'Bảng hậu tố tốt bmGs.', co_m=False)
    elif kieu == 'br':
        bang_hai_ky_tu(bc, br_bc(X), 'brBc', 'Bảng brBc (hai ký tự ngay sau cửa sổ) thu gọn trên {A, C, G, T}.',
                       'Với cặp ab mà a = x[7] = G thì brBc = 1; các cặp không xuất hiện trong mẫu và không '
                       'thỏa điều kiện nào khác cho brBc = m + 2 = 10.')
    elif kieu == 'bom':
        tr, s, ket = factor_oracle(X)
        rows = [['Trạng thái q'] + list(ABC) + ['S[q]', 'Kết?']]
        for q in range(M + 1):
            rows.append([str(q)] + [str(tr[q].get(c, '–')) for c in ABC] + [str(s[q]), 'có' if q in ket else ''])
        bc.bang(rows, [2.6] + [1.3] * 4 + [1.4, 1.4], co=10.5, dam_cot_dau=True,
                chu_thich='Factor oracle của xᴿ = GAGAGACG: hàm chuyển, liên kết hậu tố S và trạng thái kết.')
    elif kieu == 'colussi':
        nd = ell = None
        for line in vet:
            if line.startswith('N '):
                v = [int(t) for t in line.split()[1:]]
                nd = v[0]
                ell = v[1] if len(v) > 1 else None
        bang_chi_so(bc, [('h[i]', bang['h']), ('next[i]', bang['next']), ('shift[i]', bang['shift'])],
                    'Các bảng tiền xử lý h, next, shift (nd = %d).' % nd)
        if ell is not None:
            bc.doan('Ngoài ra, ell = %d vì x[0] = G ≠ x[1] = C (mẫu không bắt đầu bằng dãy ký tự lặp).' % ell)
    elif kieu in ('om', 'ms'):
        thu_tu = [int(l.split()[1]) for l in vet if l.startswith('O ')]
        if kieu == 'om':
            freq = {c: Y.count(c) for c in ABC}
            bang_ky_tu(bc, [('freq[c]', freq, None)], 'Tần suất ký tự trong văn bản ví dụ.')
        else:
            bang_chi_so(bc, [('minShift[i]', bang['minShift'])], 'Bảng minShift.', co_m=False)
        rows = [['Thứ tự k'] + [str(k) for k in range(M)],
                ['pat[k].loc'] + [str(i) for i in thu_tu],
                ['pat[k].c'] + [X[i] for i in thu_tu],
                ['adaptedGs[k]'] + [str(v) for v in bang['adaptedGs'][:M]]]
        bc.bang(rows, [2.6] + [1.3] * M, co=10, dam_cot_dau=True,
                chu_thich='Thứ tự so sánh và bảng adaptedGs (adaptedGs[8] = %d dùng khi cả mẫu khớp).'
                % bang['adaptedGs'][M])
        bang_ky_tu(bc, [('qsBc[c]', qs_bc(X), M + 1)], 'Bảng qsBc (Quick Search).', khac=True)
    elif kieu == 'skip':
        rows = [['c', 'z[c] (vị trí của c trong x)']]
        for c in ABC:
            ds = [i for i in range(M - 1, -1, -1) if X[i] == c]
            rows.append([c, ', '.join(map(str, ds)) if ds else '(rỗng)'])
        bc.bang(rows, [1.5, 7.0], co=10.5, chu_thich='Các thùng z[c] của mẫu x = GCAGAGAG.')
    elif kieu == 'horspool':
        bang_ky_tu(bc, [('bmBc[c]', bm_bc(X), M)], 'Bảng ký tự tồi bmBc.', khac=True)
    elif kieu == 'qs':
        bang_ky_tu(bc, [('qsBc[c]', qs_bc(X), M + 1)], 'Bảng qsBc.', khac=True)
    elif kieu == 'tuned':
        b = bm_bc(X)
        b2 = dict(b)
        b2[X[-1]] = 0
        bang_ky_tu(bc, [('bmBc ban đầu', b, M), ('bmBc sau sửa', b2, M)],
                   'Bảng bmBc trước và sau khi gán bmBc[x[m−1]] = 0; shift = bmBc[G] = %d.' % b['G'], khac=True)
    elif kieu == 'dfa':
        rows = [['Trạng thái'] + ['δ(q, %s)' % c for c in ABC] + ['ký tự khác']]
        for line in vet:
            if line.startswith('D '):
                v = line.split()[1:]
                rows.append([v[0] + (' (kết)' if v[0] == str(M) else '')] + v[1:] + ['0'])
        bc.bang(rows, [2.6] + [1.8] * 4 + [2.0], co=10.5, dam_cot_dau=True,
                chu_thich='Hàm chuyển trạng thái δ của automat đoán nhận Σ∗GCAGAGAG.')
    elif kieu == 'simon':
        rows = [['Trạng thái p', 'x[0..p]', 'L[p] (đích các cung lùi)', 'Ký tự trên cung']]
        for line in vet:
            if line.startswith('L '):
                v = line.split()[1:]
                p, ds = int(v[0]), [int(t) for t in v[1:]][::-1]
                rows.append([str(p), X[:p + 1], ', '.join(map(str, ds)) if ds else '—',
                             ', '.join('%s → %d' % (X[q], q) for q in ds) if ds else '—'])
        bc.bang(rows, [2.4, 3.0, 4.4, 4.4], co=10.5,
                chu_thich='Danh sách cung có ý nghĩa của automat Simon (ell = 0).')


# ----------------------------------------------------------------------------- phần mô phỏng
def mo_phong(bc, tt, vet, attempts, ten):
    kieu = tt['vet']
    if kieu == 'grid':
        bc.bang_vet(attempts, 'Mô phỏng từng lần thử của %s trên ví dụ chuẩn.' % ten)
    elif kieu == 'kr':
        d = 1 << (M - 1)
        hx = None
        rows = [['j', 'Cửa sổ y[j..j+7]', 'hy (băm cửa sổ)', 'hy = hx ?', 'Số so sánh ký tự']]
        dem = {}
        cur = None
        for line in vet:
            t = line.split()
            if t[0] == 'H':
                cur = int(t[1])
                hx = int(t[3])
                rows.append([t[1], Y[cur:cur + M], t[2], 'BẰNG' if t[2] == t[3] else 'khác', '0'])
                dem[cur] = len(rows) - 1
            elif t[0] == 'C':
                rows[dem[cur]][4] = str(int(rows[dem[cur]][4]) + 1)
        bc.doan('Tiền xử lý: d = 2^(m−1) = %d; giá trị băm của mẫu hx = hash(GCAGAGAG) = %d (mã ASCII: '
                'A = 65, C = 67, G = 71, T = 84).' % (d, hx))
        bc.bang(rows, [1.0, 4.2, 3.2, 2.4, 3.2], co=10, chu_thich='Mô phỏng pha tìm kiếm của Karp-Rabin.')
    elif kieu == 'so':
        masks = {}
        for c in ABC:
            masks[c] = ['0' if X[i] == c else '1' for i in range(M)]
        rows = [['i'] + [str(i) for i in range(M)], ['x[i]'] + list(X)]
        for c in ABC:
            rows.append(['S[%s]' % c] + masks[c])
        bc.bang(rows, [2.0] + [1.2] * M, co=10.5, dam_cot_dau=True,
                chu_thich='Mặt nạ S[c] (bit i = 0 khi x[i] = c); mọi ký tự khác có S = 11111111.')
        states = [int(l.split()[2]) for l in vet if l.startswith('S ')]
        nhan = ['j', 'y[j]'] + ['R[%d]' % i for i in range(M)]
        gt = [list(range(N)), list(Y)] + [[(s >> i) & 1 for s in states] for i in range(M)]
        bc.bang_ngang(nhan, gt, 'Vector trạng thái R sau mỗi bước của Shift-Or (ô tô màu: bit bằng 0).',
                      to_mau=lambda r, c: r >= 2 and gt[r][c] == 0)
    elif kieu == 'dfa':
        sts = [int(l.split()[3]) for l in vet if l.startswith('S ')]
        gt = [list(range(N)), list(Y), sts]
        bc.bang_ngang(['j', 'y[j]', 'trạng thái'], gt,
                      'Dãy trạng thái của automat khi đọc văn bản (ô tô màu: trạng thái kết 8).',
                      to_mau=lambda r, c: r == 2 and gt[r][c] == M)
    elif kieu == 'simon':
        sts, ss, dem = [], [], 0
        for line in vet:
            if line.startswith('C '):
                dem += 1
            elif line.startswith('S '):
                sts.append(int(line.split()[3]))
                ss.append(dem)
                dem = 0
        gt = [list(range(N)), list(Y), sts, ss]
        bc.bang_ngang(['j', 'y[j]', 'trạng thái', 'SS'], gt,
                      'Dãy trạng thái của thuật toán Simon (ô tô màu: đạt trạng thái m − 1 = 7).',
                      to_mau=lambda r, c: r == 2 and gt[r][c] == M - 1)
    for p in tt['dien_giai_vet']:
        bc.doan(p)


# ----------------------------------------------------------------------------- kiểm nghiệm
def kiem_nghiem(bc, tt, stdout, ten):
    bc.doan('**Kết quả chạy chương trình trên ví dụ chuẩn** (lệnh `./%s`):' % tt['id'], thut=False)
    bc.khoi_ma(stdout, co=9)
    rows = [['Kịch bản', 'm', 'n', 'Số lần xuất hiện', 'Số phép so sánh ký tự', 'So sánh / ký tự',
             'Thao tác khác']]
    for kb in KET_QUA:
        r = kb['thuat_toan'][tt['id']]
        rows.append([kb['kich_ban'].split(',')[0].replace(' (σ = 4)', ' (σ=4)').replace(' (σ = 26)', ' (σ=26)')
                     if not kb['kich_ban'].startswith('Xấu') else 'y = aⁿ, x = a⁸',
                     str(kb['m']), '{:,}'.format(kb['n']).replace(',', '.'),
                     '{:,}'.format(kb['xuat_hien']).replace(',', '.'),
                     '{:,}'.format(r['so_sanh']).replace(',', '.'),
                     ('%.3f' % (r['so_sanh'] / kb['n'])).replace('.', ','),
                     '{:,}'.format(r['thao_tac']).replace(',', '.')])
    bc.bang(rows, [3.4, 0.9, 1.9, 2.0, 2.6, 2.0, 2.4], co=9.5,
            can=['left'] + ['center'] * 6,
            chu_thich='Kết quả thực nghiệm của %s trên các bộ dữ liệu ngẫu nhiên.' % ten)
    if tt.get('thao_tac'):
        bc.doan('Cột "Thao tác khác" ở đây là %s.' % tt['thao_tac'], nghieng=True, co=12)
    bc.doan(tt['nhan_xet'])


# ----------------------------------------------------------------------------- các chương
def chuong_mo_dau(bc):
    p = bc.doan('MỤC LỤC', can='center', dam=True, co=15)
    p.runs[0].font.color.rgb = XANH_DAM
    p = bc.doc.add_paragraph()
    them_truong(p, 'TOC \\o "1-2" \\h \\z \\u',
                '(Mục lục sẽ được Word cập nhật khi mở tệp; nếu chưa hiển thị, nhấn chuột phải → Update Field.)')
    bc.ngat_trang()
    bc.tieu_de('LỜI MỞ ĐẦU', 1)
    for t in [
        'Đối sánh mẫu (string matching) là bài toán tìm tất cả các vị trí xuất hiện của một xâu mẫu trong '
        'một văn bản. Đây là một trong những bài toán cơ bản nhất của khoa học máy tính: các thuật toán đối '
        'sánh mẫu là thành phần cốt lõi của trình soạn thảo, công cụ tìm kiếm văn bản (grep), hệ quản trị cơ '
        'sở dữ liệu, phần mềm phát hiện mã độc và các hệ thống phân tích dữ liệu sinh học (DNA, protein).',
        'Mặc dù dữ liệu ngày càng được lưu trữ dưới nhiều hình thức, văn bản vẫn là dạng chủ yếu để trao '
        'đổi thông tin, và khối lượng dữ liệu cần tìm kiếm tăng lên rất nhanh. Vì thế các thuật toán đối sánh '
        'mẫu phải hiệu quả ngay cả khi tốc độ và dung lượng của thiết bị lưu trữ được cải thiện.',
        'Tiểu luận này trình bày **21 thuật toán đối sánh mẫu chính xác**, được chọn và phân bổ đều vào bốn '
        'nhóm theo thứ tự so sánh ký tự: từ trái sang phải, từ phải sang trái, theo một thứ tự xác định và '
        'theo thứ tự bất kỳ. Với mỗi thuật toán, tiểu luận lần lượt (1) trình bày ý tưởng, cơ chế và mô phỏng '
        'từng bước trên một ví dụ chuẩn; (2) đánh giá độ phức tạp thời gian trong các trường hợp tốt nhất, '
        'trung bình, xấu nhất và độ phức tạp bộ nhớ; (3) kiểm nghiệm bằng thực nghiệm số phép so sánh; '
        '(4) cài đặt hoàn chỉnh bằng C++.',
        'Toàn bộ nội dung lý thuyết được tham khảo từ tài liệu *Handbook of Exact String-Matching '
        'Algorithms* của Christian Charras và Thierry Lecroq. Mọi bảng mô phỏng và số liệu thực nghiệm '
        'trong tiểu luận đều được sinh tự động từ chính các chương trình C++ đi kèm, bảo đảm tính nhất quán '
        'giữa phần trình bày và phần cài đặt.',
    ]:
        bc.doan(t)


def chuong_1(bc, ket_qua_vd):
    bc.chuong = 1
    bc.so_bang = 0
    bc.ngat_trang()
    bc.tieu_de('CHƯƠNG 1. TỔNG QUAN VỀ BÀI TOÁN ĐỐI SÁNH MẪU', 1)
    bc.tieu_de('1.1. Phát biểu bài toán', 2)
    bc.doan('Cho mẫu x = x[0..m−1] độ dài m và văn bản y = y[0..n−1] độ dài n, cả hai được xây dựng trên '
            'một bảng chữ cái hữu hạn Σ có kích thước σ. Bài toán đối sánh mẫu chính xác yêu cầu tìm **tất '
            'cả** các vị trí j (0 ≤ j ≤ n − m) sao cho y[j..j+m−1] = x.')
    bc.doan('Hầu hết các thuật toán gồm hai pha: **pha tiền xử lý** chỉ làm việc trên mẫu x (và có thể trên '
            'bảng chữ cái) để xây dựng các bảng phụ trợ; **pha tìm kiếm** dùng các bảng này để quét văn bản. '
            'Pha tìm kiếm thường được mô tả qua khái niệm **cửa sổ trượt**: một cửa sổ độ dài m được đặt '
            'lên văn bản, các ký tự trong cửa sổ được so sánh với mẫu — gọi là một **lần thử** (attempt) '
            'tại vị trí j. Sau mỗi lần thử, cửa sổ được **dịch** (shift) sang phải. Các thuật toán khác nhau '
            'ở hai điểm: thứ tự so sánh các ký tự trong cửa sổ và cách tính độ dịch an toàn lớn nhất.')
    bc.tieu_de('1.2. Một số khái niệm cơ bản', 2)
    for t in [
        '**Tiền tố (prefix):** u là tiền tố của w nếu tồn tại v (có thể rỗng) để w = uv. Ví dụ: GCA là '
        'tiền tố của GCAGAGAG.',
        '**Hậu tố (suffix):** v là hậu tố của w nếu tồn tại u (có thể rỗng) để w = uv. Ví dụ: GAG là hậu tố '
        'của GCAGAGAG.',
        '**Nhân tố (factor, xâu con):** z là nhân tố của w nếu tồn tại u, v để w = uzv. Ví dụ: AGAG là nhân '
        'tố của GCAGAGAG.',
        '**Biên (border):** u là biên của w nếu u vừa là tiền tố vừa là hậu tố thực sự của w. Ví dụ: G là '
        'biên khác rỗng duy nhất (cũng là dài nhất) của GCAGAGAG; xâu AGAG có các biên AG và xâu rỗng.',
        '**Chu kỳ (period):** số nguyên dương p là chu kỳ của w nếu w[i] = w[i + p] với mọi 0 ≤ i < |w| − p. '
        'Chu kỳ nhỏ nhất của w bằng |w| trừ độ dài biên dài nhất. Ví dụ chu kỳ nhỏ nhất của GCAGAGAG là '
        '8 − 1 = 7; của AGAG là 2.',
        '**Đảo ngược:** xᴿ là xâu x viết theo chiều ngược lại. Ví dụ (GCAGAGAG)ᴿ = GAGAGACG.',
    ]:
        bc.gach(t)
    bc.tieu_de('1.3. Thuật toán vét cạn và mô hình đánh giá', 2)
    bc.doan('Thuật toán vét cạn (Brute Force) thử lần lượt mọi vị trí j = 0, 1, …, n − m, so sánh từ trái '
            'sang phải và luôn dịch đúng 1 vị trí. Nó không cần tiền xử lý, không cần bộ nhớ phụ, nhưng tốn '
            'O(m·n) thời gian trong trường hợp xấu nhất (số phép so sánh kỳ vọng là khoảng 2n trên văn bản '
            'ngẫu nhiên). Trên ví dụ chuẩn, thuật toán vét cạn thực hiện **%d** phép so sánh ký tự. Đây là '
            'mốc để so sánh mức cải tiến của 21 thuật toán trong tiểu luận.' % ket_qua_vd['bf'])
    bc.doan('Độ phức tạp của mỗi thuật toán được đánh giá theo các tiêu chí: thời gian tiền xử lý; thời '
            'gian tìm kiếm trong trường hợp tốt nhất, trung bình (văn bản ngẫu nhiên) và xấu nhất; bộ nhớ '
            'phụ trợ (không tính bộ nhớ lưu x và y). Trong đó m là độ dài mẫu, n là độ dài văn bản, σ là kích '
            'thước bảng chữ cái, w là độ dài từ máy (số bit của một số nguyên).')
    bc.tieu_de('1.4. Phân loại và lựa chọn 21 thuật toán', 2)
    bc.doan('Dựa trên thứ tự mà các ký tự của mẫu được so sánh với các ký tự của cửa sổ văn bản, các thuật '
            'toán đối sánh mẫu được chia thành bốn nhóm. Tiểu luận chọn 21 thuật toán tiêu biểu, phân bổ vào '
            'đủ cả bốn nhóm (mỗi nhóm có từ 4 tới 7 thuật toán), đại diện cho các kỹ thuật chính: băm, song '
            'song bit, automat, hàm biên, hàm hậu tố tốt / ký tự tồi, factor oracle, thứ tự so sánh tối ưu '
            'và thùng ký tự.')
    rows = [['STT', 'Thuật toán', 'Nhóm', 'Tiền xử lý', 'Tìm kiếm (xấu nhất)', 'Bộ nhớ phụ']]
    for k, tt in enumerate(THUAT_TOAN, 1):
        pt = tt['phuc_tap']
        rows.append([str(k), tt['ten'].replace('Thuật toán ', ''), str(tt['nhom']), pt['tien_xu_ly'],
                     pt['xau'], pt['bo_nho']])
    bc.bang(rows, [1.0, 5.0, 1.2, 2.6, 3.6, 2.6], co=10, can=['center', 'left', 'center', 'center', 'center',
                                                             'center'],
            chu_thich='Danh sách 21 thuật toán được trình bày (nhóm 1: trái → phải; 2: phải → trái; '
                      '3: thứ tự xác định; 4: thứ tự bất kỳ).')
    bc.tieu_de('1.5. Dữ liệu ví dụ và phương pháp kiểm nghiệm', 2)
    bc.doan('**Ví dụ chuẩn.** Mọi thuật toán đều được mô phỏng trên cùng một cặp dữ liệu:')
    bc.cong_thuc('x = GCAGAGAG  (m = 8),    y = GCATCGCAGAGAGTATACAGTACG  (n = 24)')
    bc.doan('Mẫu xuất hiện đúng một lần trong văn bản, tại vị trí j = 5. Mẫu có cấu trúc khá "giàu": các '
            'ký tự G và A xen kẽ (đoạn AGAG có chu kỳ 2), và chỉ có biên dài nhất là G, nên thể hiện rõ khác '
            'biệt giữa các thuật toán.')
    bc.doan('**Cách đọc bảng mô phỏng.** Mỗi dòng ứng với một lần thử; cột j là vị trí trong văn bản. Các '
            'ký tự của mẫu đặt tại cửa sổ hiện tại được in màu xám; ô **nền xanh** là ký tự đã được so sánh '
            'và khớp, ô **nền đỏ** là ký tự so sánh không khớp. Số nhỏ phía trên bên phải mỗi ô là thứ tự '
            'của phép so sánh trong lần thử đó — nhờ vậy có thể thấy rõ thứ tự so sánh đặc trưng của từng '
            'nhóm. Cột SS là số phép so sánh của lần thử, cột Dịch là độ dịch tới lần thử kế tiếp (chỉ liệt '
            'kê các lần thử có thực hiện so sánh).')
    bc.doan('**Đại lượng đo.** Đại lượng chính là **số phép so sánh ký tự** giữa mẫu và văn bản trong pha '
            'tìm kiếm — đại lượng không phụ thuộc máy tính và trình biên dịch. Với các thuật toán không so '
            'sánh ký tự trực tiếp (Karp-Rabin, Shift-Or, Automat, BOM) hoặc có thao tác tốn kém khác (Skip '
            'Search, Tuned BM), chương trình đếm thêm **số thao tác khác** (so sánh băm, bước chuyển trạng '
            'thái, lần đọc ký tự, lần tra bảng).')
    bc.doan('**Kiểm tra tính đúng.** Cả 21 chương trình được kiểm tra trên 250 cặp (x, y) sinh ngẫu nhiên '
            '(bảng chữ cái 1–4 ký tự, có cả văn bản tuần hoàn, 2 ≤ m ≤ 20, n ≤ 150); với mọi cặp, danh '
            'sách vị trí xuất hiện trùng khớp với kết quả của thuật toán vét cạn.')
    rows = [['Kịch bản', 'Bảng chữ cái', 'm', 'n', 'Số lần xuất hiện']]
    for kb in KET_QUA:
        bcc = 'A, C, G, T' if 'DNA' in kb['kich_ban'] else ('a–z' if 'Latin' in kb['kich_ban'] else 'a')
        rows.append([kb['kich_ban'].split(',')[0] if not kb['kich_ban'].startswith('Xấu') else 'Xấu nhất',
                     bcc, str(kb['m']), '{:,}'.format(kb['n']).replace(',', '.'),
                     '{:,}'.format(kb['xuat_hien']).replace(',', '.')])
    bc.doan('**Thực nghiệm.** Mỗi chương trình được chạy trên 5 kịch bản dưới đây. Văn bản ngẫu nhiên có '
            'phân bố đều; mẫu được trích từ một vị trí ngẫu nhiên của văn bản để bảo đảm có ít nhất một lần '
            'xuất hiện. Kịch bản cuối là trường hợp xấu nhất kinh điển y = aⁿ, x = a⁸ (mọi vị trí đều là '
            'một lần xuất hiện). Số lần xuất hiện của mọi chương trình đều được đối chiếu tự động với đáp án.')
    bc.bang(rows, [5.4, 2.8, 1.0, 2.4, 3.0], co=10.5, can=['left'] + ['center'] * 4,
            chu_thich='Các kịch bản kiểm nghiệm thực nghiệm.')
    bc.doan('Môi trường: %s, biên dịch với tùy chọn `-std=c++17 -O2`.' % ket_qua_vd['moi_truong'])
    bc.tieu_de('1.6. Bộ công cụ kiểm nghiệm dùng chung', 2)
    bc.doan('Để mã nguồn các thuật toán gọn và đồng nhất, phần đếm phép so sánh, ghi vết và hàm main được '
            'đặt trong tệp tiêu đề `kiemnghiem.h` dùng chung. Trong mã nguồn các thuật toán, `CMP(i, j)` '
            'tương đương với biểu thức `x[i] == y[j]` kèm theo việc đếm; `OUTPUT(j)` in ra một vị trí xuất '
            'hiện; `ATTEMPT(j)`, `THAOTAC(j)`, `VET(...)` chỉ phục vụ ghi vết và đếm, không ảnh hưởng tới '
            'logic của thuật toán. Mỗi chương trình có thể chạy theo ba cách: không tham số (ví dụ chuẩn), '
            'với `--vet` (in vết từng bước) hoặc với hai tệp mẫu/văn bản.')
    bc.khoi_ma(open(os.path.join(SRC, 'kiemnghiem.h')).read())


def chuong_thuat_toan(bc, nhom):
    bc.chuong = nhom['so'] + 1
    bc.so_bang = 0
    bc.ngat_trang()
    bc.tieu_de('CHƯƠNG %d. %s' % (bc.chuong, nhom['ten']), 1)
    for t in nhom['gioi_thieu']:
        bc.doan(t)
    ds = [tt for tt in THUAT_TOAN if tt['nhom'] == nhom['so']]
    for k, tt in enumerate(ds, 1):
        so = '%d.%d' % (bc.chuong, k)
        ten = tt['ten'].replace('Thuật toán ', '')
        stdout, vet = chay(tt['id'], '--vet')
        attempts, bang = doc_vet(vet)
        bc.tieu_de('%s. %s' % (so, tt['ten']), 2)
        bc.doan('Nguồn gốc: %s.' % tt['nguon'], nghieng=True, co=12, thut=False)

        bc.tieu_de('%s.1. Trình bày thuật toán' % so, 3)
        bc.muc_nho('a) Ý tưởng chính')
        for t in tt['y_tuong']:
            if t.startswith('• '):
                bc.gach(t[2:])
            else:
                bc.doan(t)
        bc.muc_nho('b) Cơ chế hoạt động')
        for loai, t in tt['co_che']:
            if loai == 'p':
                bc.doan(t)
            elif loai == 'b':
                bc.gach(t)
            else:
                bc.cong_thuc(t)
        bc.muc_nho('c) Đặc điểm chính')
        for t in tt['dac_diem']:
            bc.gach(t)
        if tt.get('tien_xu_ly'):
            bc.muc_nho('d) Pha tiền xử lý trên mẫu ví dụ x = GCAGAGAG')
            tien_xu_ly(bc, tt, bang, vet)
            bc.muc_nho('e) Mô phỏng từng bước pha tìm kiếm')
        else:
            bc.muc_nho('d) Mô phỏng từng bước trên ví dụ chuẩn')
        mo_phong(bc, tt, vet, attempts, ten)

        bc.tieu_de('%s.2. Đánh giá độ phức tạp' % so, 3)
        pt = tt['phuc_tap']
        rows = [['Tiêu chí', 'Độ phức tạp'],
                ['Thời gian tiền xử lý', pt['tien_xu_ly']],
                ['Tìm kiếm — trường hợp tốt nhất', pt['tot']],
                ['Tìm kiếm — trường hợp trung bình', pt['tb']],
                ['Tìm kiếm — trường hợp xấu nhất', pt['xau']],
                ['Bộ nhớ phụ trợ (extra space)', pt['bo_nho']]]
        bc.bang(rows, [6.5, 6.5], co=11, can=['left', 'center'],
                chu_thich='Độ phức tạp của thuật toán %s.' % ten)
        for t in pt['giai_thich']:
            bc.doan(t)

        bc.tieu_de('%s.3. Kiểm nghiệm thuật toán' % so, 3)
        kiem_nghiem(bc, tt, stdout, ten)

        bc.tieu_de('%s.4. Lập trình theo thuật toán' % so, 3)
        bc.doan('Chương trình C++ hoàn chỉnh (tệp `%s.cpp`, dùng tệp tiêu đề `kiemnghiem.h` ở mục 1.6; biên '
                'dịch: `clang++ -std=c++17 -O2 %s.cpp -o %s`):' % (tt['id'], tt['id'], tt['id']), thut=False)
        bc.khoi_ma(open(os.path.join(SRC, tt['id'] + '.cpp')).read())


def chuong_tong_hop(bc, so_sanh_vd):
    bc.chuong = 6
    bc.so_bang = 0
    bc.ngat_trang()
    bc.tieu_de('CHƯƠNG 6. TỔNG HỢP VÀ ĐÁNH GIÁ', 1)
    bc.tieu_de('6.1. So sánh độ phức tạp lý thuyết', 2)
    rows = [['Thuật toán', 'Nhóm', 'Tiền xử lý', 'Tốt nhất', 'Trung bình', 'Xấu nhất', 'Bộ nhớ']]
    for tt in THUAT_TOAN:
        pt = tt['phuc_tap']
        rows.append([tt['ten'].replace('Thuật toán ', ''), str(tt['nhom']), pt['tien_xu_ly'], pt['tot'], pt['tb'],
                     pt['xau'], pt['bo_nho']])
    bc.bang(rows, [3.6, 1.1, 2.1, 1.9, 2.4, 2.8, 2.1], co=8.5, can=['left'] + ['center'] * 6,
            chu_thich='Tổng hợp độ phức tạp của 21 thuật toán.')
    bc.tieu_de('6.2. So sánh kết quả thực nghiệm', 2)
    bc.doan('Bảng dưới đây tổng hợp chi phí của các thuật toán, tính bằng **tổng số phép so sánh ký tự và '
            'thao tác khác chia cho độ dài văn bản n** (đơn vị: thao tác/ký tự văn bản). Cột "Ví dụ" là số '
            'phép so sánh ký tự (kèm số thao tác khác nếu có) trên ví dụ chuẩn; thuật toán vét cạn cần %d '
            'phép so sánh trên ví dụ này.' % so_sanh_vd['bf'])
    rows = [['Thuật toán', 'Ví dụ'] + TEN_KICH_BAN_NGAN]
    tot_nhat = []
    for kb in KET_QUA:
        tot_nhat.append(min((r['so_sanh'] + r['thao_tac']) / kb['n'] for r in kb['thuat_toan'].values()))
    for tt in THUAT_TOAN:
        vd = so_sanh_vd[tt['id']]
        o = [tt['ten'].replace('Thuật toán ', ''), '%d' % vd[0] + (' + %d' % vd[1] if vd[1] else '')]
        for k, kb in enumerate(KET_QUA):
            r = kb['thuat_toan'][tt['id']]
            v = (r['so_sanh'] + r['thao_tac']) / kb['n']
            s = ('%.3f' % v).replace('.', ',')
            o.append('**%s**' % s if abs(v - tot_nhat[k]) < 1e-9 else s)
        rows.append(o)
    bc.bang(rows, [4.4, 1.6] + [2.0] * 5, co=9, can=['left'] + ['center'] * 6,
            chu_thich='Chi phí thực nghiệm (thao tác/ký tự văn bản); giá trị in đậm là tốt nhất của mỗi cột.')
    bc.tieu_de('6.3. Nhận xét', 2)
    for t in [
        '**Nhóm 1 (trái → phải)** có chi phí ổn định, xấp xỉ 1 thao tác/ký tự, gần như không phụ thuộc độ '
        'dài mẫu và kích thước bảng chữ cái. Shift-Or và Automat hữu hạn đúng bằng n thao tác trong mọi '
        'trường hợp; Morris-Pratt, KMP và Simon bảo đảm tối đa 2n − 1 phép so sánh. Nhóm này phù hợp khi cần '
        'bảo đảm thời gian xấu nhất, khi văn bản được đọc dạng luồng, hoặc khi mẫu ngắn trên bảng chữ cái nhỏ.',
        '**Nhóm 2 (phải → trái)** cho chi phí dưới tuyến tính và giảm rõ rệt khi m tăng. Zhu-Takaoka và '
        'Backward Oracle Matching đặc biệt hiệu quả trên bảng chữ cái nhỏ (DNA) với mẫu dài; Turbo-BM và '
        'Apostolico-Giancarlo vẫn giữ được thời gian tuyến tính ở trường hợp xấu nhất (1 thao tác/ký tự '
        'với y = aⁿ) nhờ cơ chế ghi nhớ.',
        '**Nhóm 3 (thứ tự xác định)** gồm hai hướng khác nhau: Colussi và Galil-Giancarlo hướng tới cận xấu '
        'nhất tốt nhất (3n/2 và 4n/3 phép so sánh) nhưng không "nhảy cóc"; Optimal Mismatch, Maximal Shift '
        'và Skip Search hướng tới hiệu quả trung bình, đạt chi phí dưới tuyến tính. Skip Search rất mạnh '
        'trên bảng chữ cái lớn.',
        '**Nhóm 4 (thứ tự bất kỳ)** đơn giản nhất về cài đặt nhưng là nhóm nhanh nhất trong thực tế với bảng '
        'chữ cái lớn: Horspool, Quick Search, Tuned BM chỉ đọc khoảng 1/m số ký tự văn bản. Nhược điểm chung '
        'là trường hợp xấu nhất O(m·n), thể hiện rõ ở kịch bản y = aⁿ (≈ m thao tác/ký tự).',
        '**Khuyến nghị lựa chọn:** với văn bản ngôn ngữ tự nhiên (σ lớn), dùng Quick Search, Horspool hoặc '
        'Tuned BM; với DNA và mẫu dài, dùng Zhu-Takaoka, Berry-Ravindran hoặc BOM; khi cần bảo đảm thời gian '
        'xấu nhất tuyến tính, dùng Turbo-BM, Apostolico-Giancarlo (vẫn dưới tuyến tính trung bình) hoặc '
        'KMP/Colussi; với mẫu ngắn (m ≤ 32) và yêu cầu đơn giản, ổn định, Shift-Or là lựa chọn tốt.',
    ]:
        bc.doan(t)


def ket_luan(bc):
    bc.ngat_trang()
    bc.tieu_de('KẾT LUẬN', 1)
    for t in [
        'Tiểu luận đã trình bày đầy đủ 21 thuật toán đối sánh mẫu chính xác thuộc cả bốn nhóm phân loại theo '
        'thứ tự so sánh. Với mỗi thuật toán, tiểu luận đã nêu ý tưởng, cơ chế hoạt động, các bảng tiền xử lý '
        'và mô phỏng từng bước trên cùng một ví dụ chuẩn; phân tích độ phức tạp thời gian trong các trường '
        'hợp tốt nhất, trung bình, xấu nhất cùng độ phức tạp bộ nhớ; kiểm nghiệm bằng thực nghiệm trên năm '
        'kịch bản dữ liệu; và cung cấp mã nguồn C++ hoàn chỉnh, đã được kiểm tra tính đúng.',
        'Kết quả thực nghiệm khẳng định các nhận định lý thuyết: các thuật toán quét trái sang phải có chi '
        'phí tuyến tính ổn định; các thuật toán họ Boyer-Moore và các biến thể dựa trên ký tự tồi đạt chi '
        'phí dưới tuyến tính, càng tốt khi mẫu càng dài và bảng chữ cái càng lớn, nhưng có thể suy biến về '
        'O(m·n) trên văn bản tuần hoàn nếu không có cơ chế ghi nhớ. Không có thuật toán nào tốt nhất trong '
        'mọi tình huống — việc lựa chọn cần dựa trên đặc điểm của bảng chữ cái, độ dài mẫu và yêu cầu về '
        'thời gian xấu nhất.',
        'Hướng phát triển: mở rộng cho bài toán tìm nhiều mẫu đồng thời, đối sánh xấp xỉ (cho phép sai khác) '
        'và đo thời gian chạy thực tế trên các tập dữ liệu thật (văn bản tiếng Việt, hệ gen).',
    ]:
        bc.doan(t)
    bc.tieu_de('TÀI LIỆU THAM KHẢO', 1)
    bc.doan('[1] Christian Charras, Thierry Lecroq. *Handbook of Exact String-Matching Algorithms*.', thut=False)


# ----------------------------------------------------------------------------- main
def main():
    so_sanh_vd = {}
    for tt in THUAT_TOAN:
        out, _ = chay(tt['id'])
        so_sanh_vd[tt['id']] = (int(re.search(r'So phep so sanh ky tu: (\d+)', out).group(1)),
                                int(re.search(r'So thao tac khac: (\d+)', out).group(1)))
    bf = 0
    for j in range(N - M + 1):
        i = 0
        while i < M and X[i] == Y[i + j]:
            i += 1
        bf += i + (1 if i < M else 0)
    so_sanh_vd['bf'] = bf
    trinh_bien_dich = subprocess.run(['clang++', '--version'], capture_output=True, text=True).stdout.split('\n')[0]
    so_sanh_vd['moi_truong'] = 'macOS, trình biên dịch %s' % trinh_bien_dich.strip()

    bc = BaoCao()
    chuong_mo_dau(bc)
    chuong_1(bc, so_sanh_vd)
    for nhom in NHOM:
        chuong_thuat_toan(bc, nhom)
    chuong_tong_hop(bc, so_sanh_vd)
    ket_luan(bc)
    bc.doc.save(DAU_RA)
    print('Đã lưu', DAU_RA)


if __name__ == '__main__':
    main()
