# -*- coding: utf-8 -*-
"""Nội dung văn bản của báo cáo: phần mở đầu, tổng quan và 21 thuật toán.

Quy ước định dạng nội tuyến: **đậm**, *nghiêng*, `mã`.
Mỗi thuật toán là một dict; phần bảng tiền xử lý, bảng mô phỏng và số liệu
kiểm nghiệm được build_docx.py sinh tự động từ chương trình C++ tương ứng.
"""

NHOM = [
    {
        'so': 1,
        'ten': 'NHÓM 1 — CÁC THUẬT TOÁN SO SÁNH TỪ TRÁI SANG PHẢI',
        'gioi_thieu': [
            'Đây là cách tiếp cận tự nhiên nhất: các ký tự của cửa sổ văn bản được đối chiếu với mẫu '
            'theo đúng chiều đọc, từ trái sang phải. Ưu điểm lớn của nhóm này là con trỏ trên văn bản '
            'không bao giờ phải lùi lại (hoặc lùi rất ít), vì vậy rất thích hợp khi văn bản được đọc '
            'tuần tự theo luồng (stream). Đổi lại, mọi ký tự văn bản đều phải được xem xét ít nhất một '
            'lần nên độ phức tạp tốt nhất cũng là Θ(n).',
            'Nhóm gồm 7 thuật toán: Karp-Rabin (băm), Shift-Or (song song bit), Morris-Pratt, '
            'Knuth-Morris-Pratt, Automat hữu hạn, Simon (dựa trên automat) và Not So Naive.',
        ],
    },
    {
        'so': 2,
        'ten': 'NHÓM 2 — CÁC THUẬT TOÁN SO SÁNH TỪ PHẢI SANG TRÁI',
        'gioi_thieu': [
            'Họ thuật toán Boyer-Moore so sánh cửa sổ bắt đầu từ ký tự cuối của mẫu. Khi phát hiện '
            'không khớp, thông tin về đoạn hậu tố đã khớp và ký tự gây ra sự không khớp cho phép dịch '
            'mẫu đi rất xa — thường gần bằng m. Nhờ đó số ký tự văn bản thực sự được xem xét có thể ít '
            'hơn n (độ phức tạp dưới tuyến tính, sublinear), và đây là nhóm thuật toán hiệu quả nhất '
            'trong thực tế.',
            'Nhóm gồm 5 thuật toán: Turbo Boyer-Moore, Apostolico-Giancarlo, Zhu-Takaoka, '
            'Berry-Ravindran và Backward Oracle Matching.',
        ],
    },
    {
        'so': 3,
        'ten': 'NHÓM 3 — CÁC THUẬT TOÁN SO SÁNH THEO MỘT THỨ TỰ XÁC ĐỊNH',
        'gioi_thieu': [
            'Ở nhóm này, các vị trí của mẫu được so sánh theo một thứ tự đặc biệt được tính trước '
            'trong pha tiền xử lý, chứ không phải đơn thuần từ trái sang phải hay từ phải sang trái. '
            'Thứ tự đó có thể được chọn để đạt cận lý thuyết tốt nhất về số phép so sánh trong trường '
            'hợp xấu nhất (Colussi, Galil-Giancarlo), để phát hiện không khớp sớm nhất (Optimal '
            'Mismatch), để đạt bước dịch lớn nhất (Maximal Shift), hoặc chỉ "nhảy" tới một số ký tự '
            'văn bản cách nhau m vị trí (Skip Search).',
            'Nhóm gồm 5 thuật toán: Colussi, Galil-Giancarlo, Optimal Mismatch, Maximal Shift và '
            'Skip Search.',
        ],
    },
    {
        'so': 4,
        'ten': 'NHÓM 4 — CÁC THUẬT TOÁN SO SÁNH THEO THỨ TỰ BẤT KỲ',
        'gioi_thieu': [
            'Với các thuật toán trong nhóm này, thứ tự so sánh các ký tự bên trong cửa sổ không ảnh '
            'hưởng tới tính đúng đắn: độ dịch chỉ phụ thuộc vào một ký tự cố định của văn bản (ký tự '
            'cuối cửa sổ hoặc ký tự ngay sau cửa sổ). Vì vậy việc kiểm tra cửa sổ có thể dùng hàm '
            'so sánh khối bộ nhớ của hệ thống (memcmp) hoặc một thứ tự "may mắn" bất kỳ. Các thuật toán '
            'này rất đơn giản, tiền xử lý nhẹ và thường là nhanh nhất trong thực tế.',
            'Nhóm gồm 4 thuật toán: Horspool, Quick Search, Tuned Boyer-Moore và Raita.',
        ],
    },
]

THUAT_TOAN = [
    # ------------------------------------------------------------------ NHÓM 1
    {
        'id': '01_karp_rabin', 'nhom': 1, 'ten': 'Thuật toán Karp-Rabin',
        'nguon': 'Karp và Rabin, 1987',
        'y_tuong': [
            'Thay vì so sánh trực tiếp từng ký tự, thuật toán gán cho mỗi xâu độ dài m một giá trị '
            'băm (hash). Nếu hai xâu bằng nhau thì giá trị băm của chúng bằng nhau; điều ngược lại '
            'không chắc đúng (có thể đụng độ), nên chỉ khi băm trùng mới cần kiểm tra lại bằng so sánh '
            'ký tự. Điểm mấu chốt là hàm băm phải tính lại được trong O(1) khi cửa sổ trượt sang phải '
            'một vị trí (*rolling hash*).',
        ],
        'co_che': [
            ('p', 'Hàm băm được dùng là: hash(w[0..m−1]) = (w[0]·2^(m−1) + w[1]·2^(m−2) + … + w[m−1]·2^0) '
                  'mod q, với q là số nguyên lớn (ở đây q = 2^32, tự nhiên có được nhờ phép tràn số '
                  'nguyên không dấu 32 bit). Khi trượt cửa sổ, giá trị băm mới được tính bằng:'),
            ('code', 'rehash(a, b, h) = ((h − a·2^(m−1))·2 + b) mod q'),
            ('p', 'trong đó a là ký tự rời khỏi cửa sổ và b là ký tự mới đi vào.'),
            ('b', '**Pha tiền xử lý:** tính d = 2^(m−1), giá trị băm hx của mẫu và hy của cửa sổ đầu tiên '
                  'y[0..m−1] — tốn O(m).'),
            ('b', '**Pha tìm kiếm:** với mỗi vị trí j từ 0 tới n−m: nếu hx = hy thì so sánh lần lượt '
                  'x[0..m−1] với y[j..j+m−1]; sau đó cập nhật hy bằng rehash(y[j], y[j+m], hy).'),
        ],
        'dac_diem': [
            'Dùng hàm băm, tiền xử lý O(m) thời gian và O(1) bộ nhớ phụ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất (mọi cửa sổ đều băm trùng), kỳ vọng O(n + m).',
            'Dễ mở rộng cho bài toán tìm nhiều mẫu cùng lúc hoặc tìm mẫu hai chiều.',
        ],
        'vet': 'kr',
        'dien_giai_vet': [
            'Bảng trên cho thấy pha tìm kiếm chỉ phải so sánh giá trị băm ở 17 cửa sổ; chỉ duy nhất cửa '
            'sổ j = 5 có giá trị băm trùng với hx và khi đó 8 phép so sánh ký tự xác nhận đây là một '
            'lần xuất hiện thật. Không xảy ra đụng độ nào trên ví dụ này.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m)', 'tot': 'O(n + m)', 'tb': 'O(n + m)', 'xau': 'O(m·n)', 'bo_nho': 'O(1)',
            'giai_thich': [
                'Mỗi lần trượt cửa sổ chỉ tốn O(1) để cập nhật băm, nên phần tính băm luôn là Θ(n). '
                'Trường hợp xấu nhất xảy ra khi gần như mọi cửa sổ đều băm trùng với mẫu (ví dụ y = aⁿ, '
                'x = aᵐ): mỗi cửa sổ phải kiểm tra lại m ký tự, tổng O(m·n). Với hàm băm "tốt", xác suất '
                'đụng độ ≈ 1/q nên số phép kiểm tra thừa có kỳ vọng rất nhỏ, cho thời gian kỳ vọng O(n + m).',
            ],
        },
        'thao_tac': 'số lần so sánh giá trị băm hx = hy',
        'nhan_xet': 'Trên văn bản ngẫu nhiên, số phép so sánh ký tự gần như chỉ bằng m × (số lần xuất hiện) '
                    'vì đụng độ băm rất hiếm; chi phí chính là n phép so sánh băm. Ở kịch bản y = aⁿ, mọi '
                    'cửa sổ đều là một lần xuất hiện nên thuật toán phải so sánh ≈ 8 ký tự cho mỗi vị trí — '
                    'đúng với cận O(m·n).',
    },
    {
        'id': '02_shift_or', 'nhom': 1, 'ten': 'Thuật toán Shift-Or',
        'nguon': 'Baeza-Yates và Gonnet, 1992',
        'y_tuong': [
            'Thuật toán mô phỏng một automat không đơn định nhận biết mẫu x bằng các phép toán trên bit '
            '(*bit-parallelism*). Một vector trạng thái R gồm m bit được duy trì sao cho sau khi đọc '
            'y[j], bit thứ i của R bằng 0 khi và chỉ khi x[0..i] là hậu tố của y[0..j] (tức là tiền tố '
            'độ dài i+1 của mẫu đang khớp, kết thúc tại j). Khi bit m−1 bằng 0 thì có một lần xuất hiện '
            'kết thúc tại j.',
        ],
        'co_che': [
            ('p', 'Với mỗi ký tự c của bảng chữ cái, tiền xử lý một mặt nạ S[c]: bit i của S[c] bằng 0 '
                  'nếu x[i] = c và bằng 1 nếu ngược lại. Khi đọc ký tự mới y[j], vector trạng thái được '
                  'cập nhật chỉ bằng một phép dịch trái và một phép OR:'),
            ('code', 'R_j = (R_{j−1} << 1) | S[y[j]]'),
            ('p', 'Phép dịch trái "kéo dài" mọi tiền tố đang khớp thêm một ký tự (bit 0 được đưa vào ứng với '
                  'tiền tố rỗng luôn khớp), còn phép OR với S[y[j]] loại bỏ những tiền tố mà ký tự tiếp '
                  'theo của mẫu khác y[j].'),
            ('b', '**Pha tiền xử lý:** tính S[c] cho mọi c ∈ Σ và hằng lim dùng để kiểm tra bit m−1 — '
                  'O(m + σ).'),
            ('b', '**Pha tìm kiếm:** duyệt y một lần; mỗi ký tự tốn O(1) phép toán bit khi m không vượt '
                  'quá độ dài từ máy w (ở đây w = 32).'),
        ],
        'dac_diem': [
            'Dùng song song bit; hiệu quả khi độ dài mẫu không vượt quá độ dài từ máy.',
            'Tiền xử lý O(m + σ) thời gian và bộ nhớ; tìm kiếm O(n), không phụ thuộc kích thước bảng '
            'chữ cái và độ dài mẫu.',
            'Dễ mở rộng cho tìm kiếm xấp xỉ (cho phép sai khác) và tìm kiếm theo lớp ký tự.',
        ],
        'vet': 'so',
        'dien_giai_vet': [
            'Mỗi cột là một bước đọc ký tự y[j]; các dòng R[i] ghi bit thứ i của vector trạng thái sau '
            'bước đó (0 = tiền tố x[0..i] đang khớp). Tại j = 12 bit R[7] bằng 0, nghĩa là x xuất hiện '
            'kết thúc tại vị trí 12, tức bắt đầu tại 12 − 8 + 1 = 5.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ)', 'tot': 'Θ(n)', 'tb': 'Θ(n)', 'xau': 'O(n·⌈m/w⌉)', 'bo_nho': 'O(σ·⌈m/w⌉)',
            'giai_thich': [
                'Mỗi ký tự văn bản chỉ cần một phép dịch, một phép OR và một phép so sánh với lim, tức O(1) '
                'khi m ≤ w. Nếu m > w thì vector trạng thái cần ⌈m/w⌉ từ máy và chi phí tăng tương ứng. '
                'Thuật toán không so sánh ký tự trực tiếp nên số phép so sánh ký tự bằng 0; chi phí được '
                'đo bằng số bước cập nhật trạng thái, luôn đúng bằng n.',
            ],
        },
        'thao_tac': 'số bước cập nhật vector trạng thái',
        'nhan_xet': 'Số thao tác luôn đúng bằng n trong mọi kịch bản, kể cả trường hợp xấu nhất — một '
                    'ưu điểm về tính ổn định. Đổi lại, thuật toán không bao giờ "nhảy cóc" được qua văn '
                    'bản như các thuật toán nhóm 2, 4.',
    },
    {
        'id': '03_morris_pratt', 'nhom': 1, 'ten': 'Thuật toán Morris-Pratt',
        'nguon': 'Morris và Pratt, 1970',
        'y_tuong': [
            'Thuật toán cải tiến phương pháp vét cạn bằng cách tận dụng thông tin về phần mẫu đã khớp. '
            'Giả sử ở lần thử tại vị trí j, đoạn u = x[0..i−1] = y[j..j+i−1] đã khớp và x[i] ≠ y[i+j]. '
            'Khi đó có thể dịch mẫu sao cho một **biên** v của u (xâu vừa là tiền tố vừa là hậu tố thực '
            'sự của u) khớp với phần cuối của u trong văn bản. Dịch theo biên dài nhất là an toàn (không '
            'bỏ sót lần xuất hiện) và con trỏ trên văn bản không bao giờ phải lùi lại.',
        ],
        'co_che': [
            ('p', 'Bảng mpNext được tính trước: mpNext[i] là độ dài biên dài nhất của x[0..i−1] (với '
                  'mpNext[0] = −1). Khi không khớp tại x[i], mẫu được dịch i − mpNext[i] vị trí và việc so '
                  'sánh tiếp tục từ x[mpNext[i]] với chính ký tự văn bản vừa không khớp.'),
            ('b', '**Pha tiền xử lý:** tính mpNext bằng chính thuật toán so khớp áp dụng lên mẫu — O(m).'),
            ('b', '**Pha tìm kiếm:** con trỏ j trên văn bản chỉ tăng; mỗi phép so sánh thất bại làm mẫu '
                  'dịch ít nhất 1 vị trí. Do đó có tối đa 2n − 1 phép so sánh ký tự.'),
        ],
        'dac_diem': [
            'So sánh từ trái sang phải; tiền xử lý O(m) thời gian và bộ nhớ.',
            'Tìm kiếm O(n + m); tối đa 2n − 1 phép so sánh ký tự văn bản.',
            'Độ trễ (số lần so sánh trên cùng một ký tự văn bản) bị chặn bởi m.',
        ],
        'tien_xu_ly': 'mp',
        'vet': 'grid',
        'dien_giai_vet': [
            'Lần thử đầu tiên khớp được u = GCA rồi thất bại tại x[3] (G ≠ T). Vì mpNext[3] = 0 nên mẫu '
            'dịch 3 vị trí và so sánh tiếp x[0] với chính y[3]. Lần thử tại j = 5 khớp trọn 8 ký tự; sau '
            'đó mẫu dịch theo mpNext[8] = 1 (dịch 7) và tiếp tục so x[1] với y[13]. Lưu ý chương trình '
            'tiếp tục quét đến hết văn bản (j < n) nên các lần thử cuối có cửa sổ vượt quá n − m vẫn được '
            'tính vào tổng số phép so sánh.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m)', 'tot': 'Θ(n)', 'tb': 'O(n + m)', 'xau': 'O(n + m), ≤ 2n − 1 so sánh',
            'bo_nho': 'O(m)',
            'giai_thich': [
                'Xét đại lượng 2j − i (j là chỉ số văn bản, i là chỉ số mẫu): mỗi phép so sánh thành công '
                'tăng j và i nên tăng đại lượng này 1; mỗi phép so sánh thất bại làm i giảm ít nhất 1. Vì '
                'đại lượng bị chặn bởi 2n nên tổng số phép so sánh không vượt quá 2n − 1. Lập luận tương '
                'tự cho pha tiền xử lý cho O(m).',
            ],
        },
        'nhan_xet': 'Số phép so sánh trên mỗi ký tự văn bản luôn xấp xỉ 1 (từ 1,0 đến 1,25), gần như '
                    'không đổi khi m tăng — đặc trưng của các thuật toán quét trái sang phải: không thể '
                    'đọc ít hơn n ký tự.',
    },
    {
        'id': '04_knuth_morris_pratt', 'nhom': 1, 'ten': 'Thuật toán Knuth-Morris-Pratt (KMP)',
        'nguon': 'Knuth, Morris và Pratt, 1977',
        'y_tuong': [
            'KMP là bản cải tiến của Morris-Pratt. Khi x[i] ≠ y[i+j] và mẫu được dịch để biên v của u '
            'khớp, nếu ký tự đứng ngay sau v trong mẫu lại bằng đúng x[i] thì chắc chắn sẽ lại không '
            'khớp với y[i+j] — phép so sánh đó là lãng phí. KMP chỉ dùng các **biên chặt** (*tagged '
            'border*): biên v của u sao cho x[|v|] ≠ x[i].',
        ],
        'co_che': [
            ('p', 'Bảng kmpNext[i] là độ dài biên chặt dài nhất của x[0..i−1], hoặc −1 nếu không tồn tại. '
                  'Nó được tính như mpNext nhưng thêm một bước: nếu x[i] = x[j] thì kmpNext[i] = '
                  'kmpNext[j], ngược lại kmpNext[i] = j.'),
            ('b', '**Pha tiền xử lý:** O(m) thời gian và bộ nhớ.'),
            ('b', '**Pha tìm kiếm:** giống hệt Morris-Pratt nhưng dùng kmpNext thay cho mpNext.'),
        ],
        'dac_diem': [
            'So sánh từ trái sang phải; tiền xử lý O(m).',
            'Tìm kiếm O(n + m); tối đa 2n − 1 phép so sánh ký tự.',
            'Độ trễ bị chặn bởi log m / log Φ, với Φ = (1 + √5)/2 là tỉ lệ vàng.',
        ],
        'tien_xu_ly': 'kmp',
        'vet': 'grid',
        'dien_giai_vet': [
            'So với Morris-Pratt, điểm khác biệt nằm ở lần thử đầu tiên: khi x[3] = G không khớp y[3] = T, '
            'Morris-Pratt dịch theo mpNext[3] = 0 rồi so tiếp x[0] = G với T — chắc chắn thất bại vì x[0] = '
            'x[3]. KMP có kmpNext[3] = −1 nên bỏ qua hẳn phép so sánh vô ích đó và chuyển ngay sang j = 4. '
            'Nhờ vậy KMP tiết kiệm được 1 phép so sánh trên ví dụ.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m)', 'tot': 'Θ(n)', 'tb': 'O(n + m)', 'xau': 'O(n + m), ≤ 2n − 1 so sánh',
            'bo_nho': 'O(m)',
            'giai_thich': [
                'Lập luận như Morris-Pratt cho cận 2n − 1. Điểm mạnh riêng của KMP là độ trễ: một ký tự '
                'văn bản bị so sánh nhiều nhất O(log m / log Φ) lần, vì các biên chặt liên tiếp có độ dài giảm '
                'theo cấp số tương tự dãy Fibonacci.',
            ],
        },
        'nhan_xet': 'Kết quả rất gần Morris-Pratt trên văn bản ngẫu nhiên; khác biệt rõ nhất là ở DNA với '
                    'm = 32 (1,016 so với 1,242 phép so sánh/ký tự) do mẫu dài có nhiều biên "không chặt" '
                    'mà KMP loại bỏ được.',
    },
    {
        'id': '05_automat_huu_han', 'nhom': 1, 'ten': 'Thuật toán Automat hữu hạn (DFA)',
        'nguon': 'thuật toán kinh điển dựa trên automat',
        'y_tuong': [
            'Xây dựng automat hữu hạn đơn định (DFA) nhỏ nhất đoán nhận ngôn ngữ Σ*x — tập các xâu kết '
            'thúc bằng x. Automat có m + 1 trạng thái 0, 1, …, m; trạng thái q có nghĩa là "tiền tố dài '
            'nhất của x đang là hậu tố của phần văn bản đã đọc có độ dài q". Trạng thái m là trạng thái '
            'kết thúc: mỗi lần tới đó là một lần xuất hiện của mẫu.',
        ],
        'co_che': [
            ('p', 'Hàm chuyển δ(q, c) = độ dài tiền tố dài nhất của x là hậu tố của x[0..q−1]·c. Bảng δ '
                  'được xây theo từng trạng thái: hàng của trạng thái i được sao chép từ hàng của trạng thái '
                  'r (ứng với biên dài nhất của x[0..i−1]), sau đó cung "tiến" δ(i, x[i]) = i + 1 được ghi đè.'),
            ('b', '**Pha tiền xử lý:** O(m·σ) thời gian và bộ nhớ cho bảng chuyển trạng thái.'),
            ('b', '**Pha tìm kiếm:** đọc lần lượt từng ký tự y[j] và thực hiện đúng một bước chuyển '
                  'q ← δ(q, y[j]); nếu q = m thì báo xuất hiện tại j − m + 1.'),
        ],
        'dac_diem': [
            'Xây automat tối thiểu đoán nhận Σ*x; tiền xử lý O(m·σ) thời gian và bộ nhớ.',
            'Tìm kiếm thời gian thực O(n): mỗi ký tự văn bản được xem xét đúng một lần.',
            'Thích hợp khi bảng chữ cái nhỏ (DNA, nhị phân) và mẫu được dùng để tìm trên nhiều văn bản.',
        ],
        'tien_xu_ly': 'dfa',
        'vet': 'dfa',
        'dien_giai_vet': [
            'Automat đi qua trạng thái 3 tại j = 2 (đã khớp GCA) nhưng y[3] = T đưa nó về trạng thái 0. Từ '
            'j = 5, các trạng thái tăng dần 1, 2, …, 8: tại j = 12 automat đạt trạng thái kết thúc 8, '
            'báo xuất hiện tại 12 − 8 + 1 = 5. Tổng cộng đúng n = 24 bước chuyển.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m·σ)', 'tot': 'Θ(n)', 'tb': 'Θ(n)', 'xau': 'Θ(n)', 'bo_nho': 'O(m·σ)',
            'giai_thich': [
                'Mỗi ký tự văn bản ứng với đúng một lần tra bảng δ nên pha tìm kiếm luôn là Θ(n) và là '
                '"thời gian thực" (độ trễ bằng 1). Nhược điểm là bảng δ có (m + 1)·σ ô — với σ = 256 và m '
                'lớn, bộ nhớ và thời gian tiền xử lý đáng kể.',
            ],
        },
        'thao_tac': 'số bước chuyển trạng thái',
        'nhan_xet': 'Giống Shift-Or, chi phí luôn đúng bằng n bước chuyển trong mọi kịch bản; không '
                    'có trường hợp xấu, nhưng cũng không bao giờ dưới tuyến tính.',
    },
    {
        'id': '06_simon', 'nhom': 1, 'ten': 'Thuật toán Simon',
        'nguon': 'Simon, 1993',
        'y_tuong': [
            'Automat tối thiểu đoán nhận Σ*x có (m + 1)·σ cung nhưng phần lớn các cung đi về trạng thái '
            'ban đầu. Simon nhận thấy chỉ có các cung **có ý nghĩa** cần lưu: cung "tiến" (q → q + 1) và '
            'các cung "lùi" không về trạng thái đầu. Số cung lùi có ý nghĩa không vượt quá m, nên automat '
            'được biểu diễn gọn trong O(m) bộ nhớ, độc lập với kích thước bảng chữ cái.',
        ],
        'co_che': [
            ('p', 'Trạng thái p (từ −1 tới m − 1) có nghĩa là x[0..p] đang khớp. Với mỗi trạng thái p, '
                  'danh sách L[p] chứa đích của các cung lùi có ý nghĩa. Khi đọc ký tự c = y[j]:'),
            ('b', 'nếu x[p + 1] = c thì đi theo cung tiến tới p + 1;'),
            ('b', 'ngược lại duyệt L[p], tìm phần tử q có x[q] = c và chuyển tới q;'),
            ('b', 'nếu không tìm thấy thì quay về trạng thái đầu −1.'),
            ('p', 'Khi đạt trạng thái m − 1, báo một lần xuất hiện rồi chuyển về trạng thái ell (biên dài '
                  'nhất của x) để tiếp tục.'),
        ],
        'dac_diem': [
            'Biến thể tiết kiệm bộ nhớ của automat hữu hạn; tiền xử lý O(m) thời gian và bộ nhớ.',
            'Tìm kiếm O(m + n); tối đa 2n − 1 phép so sánh ký tự.',
            'Độ trễ bị chặn bởi min(1 + log₂ m, σ).',
        ],
        'tien_xu_ly': 'simon',
        'vet': 'simon',
        'dien_giai_vet': [
            'Mỗi cột là một bước đọc y[j]: "SS" là số phép so sánh ký tự thực hiện ở bước đó (thử cung tiến '
            'rồi lần lượt các cung trong danh sách). Tại j = 12 automat đạt trạng thái 7 = m − 1, báo xuất '
            'hiện tại vị trí 5 rồi quay về trạng thái ell = 0.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m)', 'tot': 'Θ(n)', 'tb': 'O(n + m)', 'xau': 'O(n + m), ≤ 2n − 1 so sánh',
            'bo_nho': 'O(m)',
            'giai_thich': [
                'Tổng số cung có ý nghĩa là O(m) nên tiền xử lý tuyến tính theo m và không phụ thuộc σ. Mỗi '
                'phép so sánh thất bại trong danh sách tương ứng với việc chuyển tới một trạng thái nhỏ '
                'hơn, nên lập luận phân bổ (amortized) giống KMP cho cận 2n − 1 phép so sánh.',
            ],
        },
        'nhan_xet': 'Số phép so sánh trùng khớp với KMP trên cả bốn kịch bản ngẫu nhiên — đúng như lý '
                    'thuyết, Simon "ghi nhớ" cùng lượng thông tin như KMP nhưng tổ chức dưới dạng automat.',
    },
    {
        'id': '07_not_so_naive', 'nhom': 1, 'ten': 'Thuật toán Not So Naive',
        'nguon': 'Hancart, 1992',
        'y_tuong': [
            'Là cải tiến rất nhẹ của thuật toán vét cạn, dựa trên quan hệ giữa hai ký tự đầu của mẫu. Giả '
            'sử x[0] ≠ x[1]: nếu ở lần thử tại j ta biết x[1] = y[j+1] thì chắc chắn x[0] ≠ y[j+1], do '
            'đó có thể bỏ qua lần thử tại j + 1 và dịch thẳng 2 vị trí. Lập luận tương tự khi x[0] = x[1] '
            'và x[1] ≠ y[j+1].',
        ],
        'co_che': [
            ('p', 'Các ký tự của cửa sổ được so sánh theo thứ tự x[1], x[2], …, x[m−1], cuối cùng là x[0]. '
                  'Hai hằng số k và ell được tính trước:'),
            ('b', 'nếu x[0] = x[1] thì k = 2, ell = 1;'),
            ('b', 'nếu x[0] ≠ x[1] thì k = 1, ell = 2.'),
            ('p', 'Khi x[1] ≠ y[j+1], mẫu dịch k vị trí; ngược lại (x[1] khớp), sau khi kiểm tra phần còn '
                  'lại, mẫu dịch ell vị trí.'),
        ],
        'dac_diem': [
            'Tiền xử lý thời gian và bộ nhớ hằng số O(1).',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất; hơi dưới tuyến tính trong trường hợp trung bình.',
            'Yêu cầu m ≥ 2.',
        ],
        'tien_xu_ly': 'nsn',
        'vet': 'grid',
        'dien_giai_vet': [
            'Với x = GCAGAGAG ta có x[0] = G ≠ x[1] = C nên k = 1, ell = 2. Lần thử tại j = 0 khớp x[1], x[2] '
            'rồi thất bại tại x[3]; vì x[1] đã khớp nên mẫu dịch ell = 2 (bỏ qua j = 1). Tại j = 5, ký tự '
            'x[0] được so sánh sau cùng (thứ tự 8). Từ j = 7 đến 15 mỗi lần thử chỉ tốn 1 phép so sánh x[1] '
            'và dịch k = 1.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(1)', 'tot': 'Θ(n)', 'tb': 'O(n) (hệ số < 1)', 'xau': 'O(m·n)', 'bo_nho': 'O(1)',
            'giai_thich': [
                'Độ dịch tối đa là 2 nên số lần thử ít nhất ≈ n/2, mỗi lần ít nhất 1 phép so sánh, vì vậy '
                'thời gian luôn Ω(n). Trường hợp xấu nhất như vét cạn: mỗi cửa sổ khớp gần hết m ký tự '
                'mà độ dịch chỉ là 1 hoặc 2, cho O(m·n).',
            ],
        },
        'nhan_xet': 'Trên văn bản ngẫu nhiên, Not So Naive tốn khoảng 0,76–1,07 phép so sánh/ký tự — '
                    'tốt hơn Morris-Pratt nhờ bước dịch 2 khi x[1] khớp. Ở kịch bản y = aⁿ thuật toán '
                    'bộc lộ nhược điểm O(m·n): ≈ 8 phép so sánh/ký tự.',
    },
    # ------------------------------------------------------------------ NHÓM 2
    {
        'id': '08_turbo_bm', 'nhom': 2, 'ten': 'Thuật toán Turbo Boyer-Moore',
        'nguon': 'Crochemore và cộng sự, 1992',
        'y_tuong': [
            'Turbo-BM là biến thể của Boyer-Moore (BM). Thuật toán BM so sánh cửa sổ từ phải sang trái '
            'và khi không khớp thì dịch theo giá trị lớn nhất của hai hàm: **hậu tố tốt** (*good-suffix*, '
            'bảng bmGs) và **ký tự tồi** (*bad-character*, bảng bmBc). Nhược điểm của BM là "quên" phần '
            'đã khớp ở lần thử trước nên trường hợp xấu nhất là O(m·n) khi tìm mọi lần xuất hiện.',
            'Turbo-BM ghi nhớ đoạn u của văn bản đã khớp với một hậu tố của mẫu ở lần thử trước. Ở lần '
            'thử hiện tại, khi quá trình so sánh đi tới đoạn u, thuật toán "nhảy qua" u (không so sánh '
            'lại). Ngoài ra nó còn cho phép một bước dịch **turbo** dựa trên độ dài u và độ dài đoạn v '
            'vừa khớp.',
        ],
        'co_che': [
            ('b', '**bmBc[c]:** khoảng cách từ lần xuất hiện cuối cùng của c trong x[0..m−2] tới cuối mẫu '
                  '(bằng m nếu c không xuất hiện).'),
            ('b', '**bmGs[i]:** độ dịch nhỏ nhất sao cho hậu tố x[i+1..m−1] đã khớp lại khớp với một vị '
                  'trí khác của mẫu (ký tự đứng trước phải khác x[i]), hoặc một tiền tố của x khớp với hậu '
                  'tố của đoạn đã khớp. Bảng được tính qua mảng phụ suff trong O(m).'),
            ('b', '**Bộ nhớ u:** độ dài đoạn đã khớp ở lần thử trước. Khi so sánh tới vị trí i = m − 1 − '
                  'shift, chỉ số i được giảm thêm u để nhảy qua đoạn đó.'),
            ('b', '**Turbo-shift = u − v**, với v là độ dài hậu tố vừa khớp ở lần thử hiện tại. Độ dịch '
                  'thực tế là max(turboShift, bcShift, bmGs[i]); nếu turbo-shift được chọn thì độ dịch ít '
                  'nhất là u + 1.'),
        ],
        'dac_diem': [
            'Biến thể của Boyer-Moore, không cần tiền xử lý thêm ngoài bmBc và bmGs; bộ nhớ phụ chỉ là '
            'hằng số so với BM.',
            'Tiền xử lý O(m + σ) thời gian và bộ nhớ.',
            'Tìm kiếm O(n); tối đa 2n phép so sánh ký tự trong trường hợp xấu nhất.',
        ],
        'tien_xu_ly': 'bm',
        'vet': 'grid',
        'dien_giai_vet': [
            'Lần thử tại j = 1 khớp hậu tố "AG" (v = 2) rồi thất bại tại x[5]; mẫu dịch bmGs[5] = 4 và ghi '
            'nhớ u = 2. Ở lần thử tại j = 5, sau khi so sánh x[7], x[6], x[5], x[4] (chỉ số i đạt '
            'm − 1 − shift = 3), thuật toán nhảy qua u = 2 ký tự x[3], x[2] — đoạn y[8..9] đã biết là khớp từ '
            'lần thử trước — và chỉ so sánh tiếp x[1], x[0]. Lần xuất hiện được xác nhận với 6 thay vì 8 '
            'phép so sánh.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ)', 'tot': 'O(n/m)', 'tb': 'dưới tuyến tính', 'xau': 'O(n), ≤ 2n so sánh',
            'bo_nho': 'O(m + σ)',
            'giai_thich': [
                'Nhờ cơ chế nhớ và turbo-shift, mỗi ký tự văn bản chỉ có thể bị so sánh lại một số lần bị '
                'chặn, cho tổng không quá 2n phép so sánh — tuyến tính kể cả khi tìm mọi lần xuất hiện '
                '(trong khi BM gốc là O(m·n)). Trường hợp tốt nhất, mỗi lần thử chỉ 1 phép so sánh và dịch '
                'm vị trí, cho O(n/m).',
            ],
        },
        'nhan_xet': 'Số phép so sánh giảm mạnh khi m tăng (DNA: 0,398 → 0,166 phép so sánh/ký tự) — '
                    'đặc trưng dưới tuyến tính của họ Boyer-Moore. Ở kịch bản y = aⁿ, nhờ cơ chế nhớ u, '
                    'Turbo-BM chỉ tốn đúng 1 phép so sánh/ký tự thay vì m như Horspool hay Quick Search.',
    },
    {
        'id': '09_apostolico_giancarlo', 'nhom': 2, 'ten': 'Thuật toán Apostolico-Giancarlo',
        'nguon': 'Apostolico và Giancarlo, 1986',
        'y_tuong': [
            'Cũng là một biến thể của Boyer-Moore có ghi nhớ, nhưng lưu nhiều thông tin hơn Turbo-BM. Ở mỗi '
            'lần thử kết thúc tại vị trí văn bản j + m − 1, thuật toán lưu skip[j + m − 1] = độ dài hậu tố '
            'của mẫu đã khớp kết thúc tại đó. Ở các lần thử sau, khi so sánh tới một vị trí có skip > 0, '
            'thuật toán dùng bảng suff của mẫu để suy ra ngay kết quả của cả một đoạn so sánh mà không cần '
            'đọc lại văn bản.',
        ],
        'co_che': [
            ('p', 'Tại vị trí i của cửa sổ, đặt k = skip[i] (đoạn văn bản đã biết khớp với hậu tố độ dài k '
                  'của x) và s = suff[i] (độ dài hậu tố chung dài nhất của x[0..i] và x). Bốn trường hợp:'),
            ('b', 'k = 0: so sánh trực tiếp x[i] với y[i+j].'),
            ('b', 'k > s: nếu s = i + 1 thì có một lần xuất hiện; ngược lại chắc chắn không khớp tại '
                  'vị trí i − s, dừng lần thử.'),
            ('b', 'k < s: không khớp tại i − k, dừng lần thử.'),
            ('b', 'k = s: nhảy qua k ký tự (i ← i − k) và tiếp tục.'),
            ('p', 'Độ dịch giống Boyer-Moore: max(bmGs[i], bmBc[y[i+j]] − m + 1 + i). Bảng skip được dịch '
                  'theo cửa sổ để chỉ cần O(m) bộ nhớ.'),
        ],
        'dac_diem': [
            'Biến thể của Boyer-Moore; tiền xử lý O(m + σ) thời gian và bộ nhớ.',
            'Tìm kiếm O(n); tối đa 3n/2 phép so sánh ký tự trong trường hợp xấu nhất.',
            'Mỗi ký tự văn bản được so sánh "khớp" nhiều nhất một lần.',
        ],
        'tien_xu_ly': 'ag',
        'vet': 'grid',
        'dien_giai_vet': [
            'Trên ví dụ, Apostolico-Giancarlo có cùng dãy lần thử với Turbo-BM. Ở lần thử j = 5, khi chỉ số '
            'i = 3, ta có skip[3] = 2 (đoạn y[7..8] = "AG" đã khớp với hậu tố của mẫu ở lần thử j = 1) và '
            'suff[3] = 2: trường hợp k = s, thuật toán nhảy qua 2 ký tự x[3], x[2] rồi so sánh tiếp x[1], x[0].',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ)', 'tot': 'O(n/m)', 'tb': 'dưới tuyến tính', 'xau': 'O(n), ≤ 3n/2 so sánh',
            'bo_nho': 'O(m + σ)',
            'giai_thich': [
                'Mỗi phép so sánh thành công gắn với một ký tự văn bản chưa từng được so sánh khớp trước '
                'đó, nên có tối đa n phép so sánh thành công; số phép so sánh thất bại không vượt quá số '
                'lần thử. Phân tích chặt cho cận 3n/2.',
            ],
        },
        'nhan_xet': 'Số liệu gần như trùng Turbo-BM trên văn bản ngẫu nhiên vì trường hợp nhảy qua '
                    'đoạn đã khớp hiếm khi xảy ra; ưu thế lý thuyết (3n/2 thay vì 2n) chỉ thể hiện trên '
                    'các văn bản có tính chu kỳ cao.',
    },
    {
        'id': '10_zhu_takaoka', 'nhom': 2, 'ten': 'Thuật toán Zhu-Takaoka',
        'nguon': 'Zhu và Takaoka, 1987',
        'y_tuong': [
            'Zhu-Takaoka là biến thể của Boyer-Moore trong đó hàm ký tự tồi được tính dựa trên **hai ký tự '
            'cuối** của cửa sổ y[j+m−2] y[j+m−1] thay vì một. Với bảng chữ cái nhỏ (như DNA), một ký tự '
            'xuất hiện ở hầu hết các vị trí của mẫu nên bước dịch theo ký tự tồi rất ngắn; xét cặp hai ký '
            'tự cho thông tin "hiếm" hơn và bước dịch dài hơn.',
        ],
        'co_che': [
            ('p', 'Bảng hai chiều ztBc[a][b], với a, b ∈ Σ, bằng:'),
            ('b', 'm − 1 − i, với i lớn nhất (i < m − 1) sao cho x[i−1]x[i] = ab;'),
            ('b', 'ngược lại m − 1 nếu x[0] = b (cặp chỉ có thể khớp ở đầu mẫu);'),
            ('b', 'ngược lại m.'),
            ('p', 'Pha tìm kiếm so sánh từ phải sang trái như BM; khi không khớp tại i, dịch '
                  'max(bmGs[i], ztBc[y[j+m−2]][y[j+m−1]]).'),
        ],
        'dac_diem': [
            'Biến thể của Boyer-Moore dùng cặp ký tự cuối cửa sổ.',
            'Tiền xử lý O(m + σ²) thời gian và bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất.',
        ],
        'tien_xu_ly': 'zt',
        'vet': 'grid',
        'dien_giai_vet': [
            'Lần thử đầu tiên thất bại ngay tại x[7] (G ≠ A). Hai ký tự cuối cửa sổ là "CA", cặp này xuất '
            'hiện trong mẫu tại x[1]x[2] nên ztBc[C][A] = 8 − 1 − 2 = 5: mẫu được dịch thẳng 5 vị trí tới '
            'đúng lần xuất hiện j = 5 (Boyer-Moore chỉ dịch được 1). Tổng cộng chỉ 14 phép so sánh.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ²)', 'tot': 'O(n/m)', 'tb': 'dưới tuyến tính', 'xau': 'O(m·n)',
            'bo_nho': 'O(m + σ²)',
            'giai_thich': [
                'Bảng ztBc có σ² ô nên tiền xử lý và bộ nhớ là O(m + σ²) — với σ = 256 là 65 536 ô. '
                'Thuật toán không ghi nhớ đoạn đã khớp nên trường hợp xấu nhất như BM: O(m·n).',
            ],
        },
        'nhan_xet': 'Zhu-Takaoka cho số phép so sánh thấp nhất nhóm 2 trên DNA (0,222 với m = 8 và '
                    '0,089 với m = 32) — xác nhận lợi ích của bảng hai ký tự khi bảng chữ cái nhỏ. Ở '
                    'kịch bản y = aⁿ nó chịu chi phí O(m·n) (≈ 8 phép so sánh/ký tự).',
    },
    {
        'id': '11_berry_ravindran', 'nhom': 2, 'ten': 'Thuật toán Berry-Ravindran',
        'nguon': 'Berry và Ravindran, 1999',
        'y_tuong': [
            'Berry-Ravindran kết hợp ý tưởng của Quick Search (dịch theo ký tự ngay sau cửa sổ) và '
            'Zhu-Takaoka (dùng cặp ký tự): độ dịch được tính theo **hai ký tự liên tiếp ngay sau cửa sổ** '
            'y[j+m] y[j+m+1]. Vì cả hai ký tự này nằm ngoài cửa sổ, độ dịch có thể lên tới m + 2.',
        ],
        'co_che': [
            ('p', 'Bảng brBc[a][b] bằng giá trị nhỏ nhất trong các khả năng:'),
            ('b', '1 nếu x[m−1] = a;'),
            ('b', 'm − i nếu x[i]x[i+1] = ab (lấy i lớn nhất);'),
            ('b', 'm + 1 nếu x[0] = b;'),
            ('b', 'm + 2 trong các trường hợp còn lại.'),
            ('p', 'Ở mỗi lần thử, cửa sổ được so sánh (theo thứ tự bất kỳ, ở đây từ trái sang phải); sau đó '
                  'dịch brBc[y[j+m]][y[j+m+1]]. Văn bản được đệm thêm hai ký tự rỗng để truy cập y[n], y[n+1].'),
        ],
        'dac_diem': [
            'Lai giữa Quick Search và Zhu-Takaoka.',
            'Tiền xử lý O(m + σ²) thời gian và bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất.',
        ],
        'tien_xu_ly': 'br',
        'vet': 'grid',
        'dien_giai_vet': [
            'Sau lần thử j = 0, cặp ký tự sau cửa sổ là y[8]y[9] = "GA"; vì x[7] = G nên brBc[G][A] = 1. Ở '
            'j = 1 và j = 3, cặp sau cửa sổ là "AG" — khớp x[6]x[7] — cho độ dịch 2. Sau lần xuất hiện tại '
            'j = 5, cặp "TA" không có trong mẫu nên mẫu được dịch tối đa m + 2 = 10 vị trí.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ²)', 'tot': 'O(n/(m + 2))', 'tb': 'dưới tuyến tính', 'xau': 'O(m·n)',
            'bo_nho': 'O(σ²)',
            'giai_thich': [
                'Trường hợp tốt nhất mỗi lần thử tốn 1 phép so sánh và dịch m + 2, cho O(n/(m + 2)). Không '
                'có cơ chế nhớ nên trường hợp xấu nhất là O(m·n).',
            ],
        },
        'nhan_xet': 'Trên bảng chữ cái 26 ký tự, Berry-Ravindran đạt 0,112 phép so sánh/ký tự với m = 8 — '
                    'tốt nhất trong nhóm 2 — vì cặp ký tự sau cửa sổ thường không xuất hiện trong mẫu, cho '
                    'độ dịch m + 2.',
    },
    {
        'id': '12_backward_oracle_matching', 'nhom': 2, 'ten': 'Thuật toán Backward Oracle Matching (BOM)',
        'nguon': 'Allauzen, Crochemore và Raffinot, 1999',
        'y_tuong': [
            'BOM đọc cửa sổ từ phải sang trái nhưng thay vì so sánh với mẫu, nó đi trên một automat được '
            'xây từ mẫu đảo ngược xᴿ gọi là **factor oracle**. Oracle có đúng m + 1 trạng thái và nhận mọi '
            'nhân tố (xâu con) của xᴿ (có thể nhận thêm một số xâu khác). Khi đang đọc ngược cửa sổ mà '
            'oracle không có cung đi tiếp, đoạn vừa đọc chắc chắn **không phải** là nhân tố của x — do đó '
            'không có lần xuất hiện nào chứa đoạn này và có thể dịch cửa sổ qua hẳn nó.',
        ],
        'co_che': [
            ('b', '**Xây oracle** của xᴿ trong O(m) bước: trạng thái i tương ứng tiền tố độ dài i của xᴿ; '
                  'thêm cung i−1 → i nhãn xᴿ[i−1], sau đó đi theo liên kết hậu tố S để thêm các cung bổ '
                  'sung tới i. Các trạng thái trên đường liên kết hậu tố từ m là trạng thái kết.'),
            ('b', '**Tìm kiếm:** đọc y[j+m−1], y[j+m−2], … trên oracle. Mỗi khi tới một trạng thái kết tại '
                  'vị trí i, đoạn y[i+j..j+m−1] là một tiền tố của x, ghi nhớ độ dịch shift = i. Nếu đọc '
                  'hết m ký tự thì có xuất hiện. Nếu gặp cung không xác định, dịch cửa sổ shift vị trí.'),
        ],
        'dac_diem': [
            'Dùng factor oracle của mẫu đảo ngược; oracle có m + 1 trạng thái và không quá 2m − 1 cung.',
            'Tiền xử lý O(m) (với bảng chuyển đầy đủ, bộ nhớ O(m·σ) như cài đặt ở đây).',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất; tối ưu trong trường hợp trung bình '
            'O(n·log m / (m·log σ)).',
        ],
        'tien_xu_ly': 'bom',
        'vet': 'grid',
        'dien_giai_vet': [
            'Các ô tô màu là các ký tự văn bản được đọc trên oracle (xanh: có cung chuyển, đỏ: không có '
            'cung). Ở lần thử j = 0, sau khi đọc y[7], y[6], y[5] = "GCA" (đọc ngược) oracle tới trạng thái '
            'kết — "GCA" là tiền tố của x — rồi thất bại tại y[4]; cửa sổ dịch 5 để đặt tiền tố này vào đầu '
            'cửa sổ mới. Lần thử j = 5 đọc trọn 8 ký tự và báo xuất hiện.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m) (bảng: O(m·σ))', 'tot': 'O(n/m)', 'tb': 'O(n·log m / (m·log σ))', 'xau': 'O(m·n)',
            'bo_nho': 'O(m·σ) hoặc O(m) với danh sách cung',
            'giai_thich': [
                'Trong trường hợp trung bình, chỉ khoảng O(log m / log σ) ký tự cuối cửa sổ cần đọc trước khi '
                'xâu đọc được không còn là nhân tố của x, và cửa sổ dịch gần m vị trí — đây là cận tối ưu '
                'cho bài toán. Trường hợp xấu nhất (văn bản tuần hoàn) mỗi cửa sổ đọc m ký tự và dịch ít.',
            ],
        },
        'thao_tac': 'số ký tự văn bản được đọc (mỗi lần là một bước chuyển trên oracle)',
        'nhan_xet': 'BOM chỉ đọc 0,12 ký tự văn bản trên mỗi ký tự với DNA và m = 32 — rất tốt trên bảng '
                    'chữ cái nhỏ và mẫu dài. Ở kịch bản y = aⁿ, mỗi lần thử đọc trọn 8 ký tự rồi chỉ dịch '
                    '1 (chu kỳ của mẫu), cho chi phí O(m·n).',
    },
    # ------------------------------------------------------------------ NHÓM 3
    {
        'id': '13_colussi', 'nhom': 3, 'ten': 'Thuật toán Colussi',
        'nguon': 'Colussi, 1991',
        'y_tuong': [
            'Colussi là một tinh chỉnh của KMP. Các vị trí của mẫu được chia làm hai tập rời nhau:',
            '• **noholes** — các vị trí i > 0 mà kmin[i] > 0, trong đó kmin[i] là chu kỳ nhỏ nhất k sao '
            'cho x[i] ≠ x[i − k] trong khi x[0..i−1] có chu kỳ k (lần đầu tiên chu kỳ k "bị phá" tại i);',
            '• **holes** — các vị trí còn lại.',
            'Ở mỗi lần thử, các noholes được so sánh trước theo thứ tự tăng dần (từ trái sang phải), sau '
            'đó mới tới các holes theo thứ tự giảm dần (từ phải sang trái). Thứ tự này cho phép tính '
            'trước độ dịch và vị trí tiếp tục sao cho không ký tự văn bản nào bị so sánh quá nhiều lần.',
        ],
        'co_che': [
            ('b', '**h[ ]:** thứ tự so sánh — h[0..nd] là các noholes tăng dần, h[nd+1..m−1] là các holes '
                  'giảm dần.'),
            ('b', '**shift[i]:** độ dịch khi không khớp tại vị trí h[i] (bằng kmin[h[i]] với noholes, '
                  'rmin[h[i]] với holes); **next[i]:** số noholes đã biết chắc khớp sau khi dịch, để lần '
                  'thử tiếp theo bắt đầu từ h[next[i]].'),
            ('b', '**last:** vị trí văn bản xa nhất đã biết khớp — không bao giờ so sánh lại các ký tự '
                  'văn bản trước last.'),
        ],
        'dac_diem': [
            'Tinh chỉnh của KMP; tiền xử lý O(m) thời gian và bộ nhớ.',
            'Tìm kiếm O(n); tối đa 3n/2 phép so sánh ký tự trong trường hợp xấu nhất.',
            'So sánh theo thứ tự xác định: noholes từ trái sang phải, rồi holes từ phải sang trái.',
        ],
        'tien_xu_ly': 'colussi',
        'vet': 'grid',
        'dien_giai_vet': [
            'Với x = GCAGAGAG: noholes = {1, 2, 4, 6} và holes = {7, 5, 3, 0} (nd = 3), nên thứ tự so sánh '
            'là x[1], x[2], x[4], x[6], x[7], x[5], x[3], x[0] — có thể thấy rõ qua các số thứ tự ở lần '
            'thử j = 5. Ở j = 0, x[4] không khớp nên dịch shift[2] = 3; ở j = 3, x[2] không khớp nên dịch '
            'shift[1] = 2 tới đúng lần xuất hiện. Tổng 20 phép so sánh.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m)', 'tot': 'O(n)', 'tb': 'O(n)', 'xau': 'O(n), ≤ 3n/2 so sánh', 'bo_nho': 'O(m)',
            'giai_thich': [
                'Phân tích của Colussi cho thấy mỗi phép so sánh với một nohole thành công/thất bại được '
                '"trả" bằng sự tiến của cửa sổ hoặc của last, và holes chỉ được so sánh khi mọi noholes đã '
                'khớp; tổng hợp lại tối đa 3n/2 phép so sánh — tốt hơn cận 2n − 1 của KMP.',
            ],
        },
        'nhan_xet': 'Trên văn bản ngẫu nhiên, Colussi tốn khoảng 0,73–1,0 phép so sánh/ký tự, ổn định '
                    'và không bao giờ kém KMP; ở kịch bản y = aⁿ chỉ đúng 1 phép so sánh/ký tự nhờ biến last.',
    },
    {
        'id': '14_galil_giancarlo', 'nhom': 3, 'ten': 'Thuật toán Galil-Giancarlo',
        'nguon': 'Galil và Giancarlo, 1992',
        'y_tuong': [
            'Galil-Giancarlo cải tiến Colussi cho trường hợp mẫu bắt đầu bằng một dãy ký tự giống nhau: '
            'x = c^(ell+1) d …, với d ≠ c. Khi cửa sổ hiện tại nằm chồng lên một đoạn văn bản đã biết là '
            'khớp (trạng thái "heavy"), thay vì so sánh theo thứ tự Colussi, thuật toán quét tiếp dãy ký '
            'tự c bắt đầu từ last + 1 để biết ngay vị trí khả dĩ tiếp theo.',
            'Trường hợp đặc biệt mẫu là lũy thừa của một ký tự (x = cᵐ) được xử lý riêng bằng một vòng '
            'đếm độ dài dãy c liên tiếp trong văn bản.',
        ],
        'co_che': [
            ('b', 'Dùng lại toàn bộ bảng h, next, shift của Colussi; thêm ell = (độ dài dãy ký tự đầu giống '
                  'nhau) − 1.'),
            ('b', 'Khi heavy và i = 0: đếm k ký tự c liên tiếp từ last + 1. Nếu k ≤ ell hoặc ký tự tiếp '
                  'theo khác x[ell+1] thì dịch qua cả đoạn; ngược lại căn mẫu để x[ell+1] trùng vị trí vừa '
                  'tìm thấy và tiếp tục từ i = 1.'),
            ('b', 'Các trường hợp khác xử lý như Colussi.'),
        ],
        'dac_diem': [
            'Tinh chỉnh của Colussi; tiền xử lý O(m) thời gian và bộ nhớ.',
            'Tìm kiếm O(n); tối đa 4n/3 phép so sánh ký tự trong trường hợp xấu nhất.',
        ],
        'tien_xu_ly': 'colussi',
        'vet': 'grid',
        'dien_giai_vet': [
            'Với x = GCAGAGAG, ell = 0 (x[0] ≠ x[1]). Các lần thử giống hệt Colussi, trừ lần thử tại j = 12: '
            'cửa sổ chồng lên đoạn vừa khớp (j ≤ last) nên thuật toán vào chế độ heavy, so sánh x[0] rồi '
            'x[1] với y[13] = T; cả hai đều không khớp nên cửa sổ nhảy thẳng tới j = 14, bỏ qua lần thử '
            'j = 13. Tổng số phép so sánh vẫn là 20.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m)', 'tot': 'O(n)', 'tb': 'O(n)', 'xau': 'O(n), ≤ 4n/3 so sánh', 'bo_nho': 'O(m)',
            'giai_thich': [
                'Việc xử lý riêng tiền tố cᵉˡˡ⁺¹ loại bỏ các tình huống xấu nhất của Colussi (khi văn bản '
                'chứa các dãy dài ký tự c), hạ cận xấu nhất từ 3n/2 xuống 4n/3 phép so sánh.',
            ],
        },
        'nhan_xet': 'Trên các bộ dữ liệu ngẫu nhiên kết quả trùng với Colussi vì mẫu lấy ngẫu nhiên hiếm khi '
                    'bắt đầu bằng dãy ký tự lặp và chế độ heavy ít khi kích hoạt. Ở kịch bản y = aⁿ, x = a⁸ '
                    'thuật toán chạy nhánh đặc biệt "lũy thừa một ký tự": đúng 1 phép so sánh/ký tự.',
    },
    {
        'id': '15_optimal_mismatch', 'nhom': 3, 'ten': 'Thuật toán Optimal Mismatch',
        'nguon': 'Sunday, 1990',
        'y_tuong': [
            'Nếu biết phân bố tần suất ký tự của văn bản, ta nên so sánh **ký tự hiếm nhất** của mẫu trước: '
            'xác suất ký tự đó khớp là thấp nhất, nên sự không khớp được phát hiện sớm nhất và số phép so '
            'sánh trung bình mỗi lần thử nhỏ nhất. Optimal Mismatch sắp xếp các vị trí của mẫu theo tần '
            'suất ký tự tăng dần và so sánh theo thứ tự đó.',
        ],
        'co_che': [
            ('b', '**Thứ tự so sánh:** sắp xếp các vị trí i của mẫu theo freq[x[i]] tăng dần; cùng tần '
                  'suất thì vị trí lớn hơn đứng trước. Trong cài đặt này freq được đếm trực tiếp trên văn '
                  'bản (trong ứng dụng thực tế có thể dùng bảng tần suất của ngôn ngữ).'),
            ('b', '**adaptedGs[k]:** bảng hậu tố tốt "thích nghi" với thứ tự so sánh — độ dịch nhỏ nhất '
                  'sao cho k vị trí đầu tiên (theo thứ tự) đã khớp vẫn nhất quán với mẫu sau khi dịch và '
                  'vị trí thứ k (không khớp) mang ký tự khác.'),
            ('b', '**Độ dịch:** max(adaptedGs[k], qsBc[y[j+m]]) với qsBc là bảng của Quick Search.'),
        ],
        'dac_diem': [
            'Biến thể của Quick Search; cần biết tần suất ký tự.',
            'Tiền xử lý O(m² + σ) thời gian và O(m + σ) bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất.',
        ],
        'tien_xu_ly': 'om',
        'vet': 'grid',
        'dien_giai_vet': [
            'Trong văn bản ví dụ, C là ký tự hiếm nhất trong các ký tự của mẫu nên x[1] = C được so sánh '
            'đầu tiên, tiếp theo là các G (từ phải sang trái) rồi tới các A. Ở j = 0, x[1] khớp nhưng x[7] '
            'không khớp: dịch max(adaptedGs[1], qsBc[G]) = 3. Ở j = 14, x[1] = C không khớp ngay phép so '
            'sánh đầu tiên.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m² + σ)', 'tot': 'O(n/m)', 'tb': 'dưới tuyến tính', 'xau': 'O(m·n)',
            'bo_nho': 'O(m + σ)',
            'giai_thich': [
                'Bảng adaptedGs được tính bằng cách thử các độ dịch tăng dần với từng tiền tố của thứ tự so '
                'sánh, tốn O(m²). Pha tìm kiếm không có cơ chế nhớ nên xấu nhất O(m·n); tốt nhất mỗi lần '
                'thử 1 phép so sánh và dịch m + 1 như Quick Search.',
            ],
        },
        'nhan_xet': 'Trên văn bản ngẫu nhiên phân bố đều, mọi ký tự có tần suất xấp xỉ nhau nên lợi thế '
                    '"ký tự hiếm" không rõ rệt; kết quả tương đương Quick Search và tốt hơn đôi chút trên '
                    'DNA (0,353 so với 0,394 phép so sánh/ký tự với m = 8).',
    },
    {
        'id': '16_maximal_shift', 'nhom': 3, 'ten': 'Thuật toán Maximal Shift',
        'nguon': 'Sunday, 1990',
        'y_tuong': [
            'Cùng khung với Optimal Mismatch nhưng chọn thứ tự so sánh nhằm **tối đa hóa độ dịch** khi '
            'gặp không khớp. Với mỗi vị trí i, minShift[i] là khoảng cách từ x[i] tới lần xuất hiện gần '
            'nhất bên trái của cùng ký tự (hoặc i + 1 nếu không có). Nếu x[i] không khớp thì mẫu phải '
            'dịch ít nhất minShift[i]; vì vậy các vị trí có minShift lớn được so sánh trước.',
        ],
        'co_che': [
            ('b', 'Sắp xếp các vị trí theo minShift giảm dần, cùng giá trị thì vị trí lớn hơn trước.'),
            ('b', 'Dùng bảng adaptedGs (tính theo thứ tự mới) và qsBc như Optimal Mismatch; độ dịch là '
                  'max(adaptedGs[k], qsBc[y[j+m]]).'),
        ],
        'dac_diem': [
            'Biến thể của Quick Search.',
            'Tiền xử lý O(m² + σ) thời gian và O(m + σ) bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất.',
        ],
        'tien_xu_ly': 'ms',
        'vet': 'grid',
        'dien_giai_vet': [
            'minShift = [1, 2, 3, 3, 2, 2, 2, 2] nên x[3] (minShift = 3, vị trí lớn hơn x[2]) được so sánh '
            'đầu tiên. Ở các lần thử j = 0, 1, 3 và 14, x[3] = G lần lượt gặp T, C, C và C nên mỗi lần chỉ tốn '
            '1 phép so sánh. Tổng chỉ 12 phép so sánh — ít nhất trong các thuật toán có so sánh ký tự trên '
            'ví dụ này (trừ Skip Search và Tuned BM).',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m² + σ)', 'tot': 'O(n/m)', 'tb': 'dưới tuyến tính', 'xau': 'O(m·n)',
            'bo_nho': 'O(m + σ)',
            'giai_thich': [
                'Tính minShift tốn O(m²) với cài đặt trực tiếp (có thể O(m + σ) bằng bảng lần xuất hiện '
                'cuối); bảng adaptedGs tốn O(m²). Phân tích pha tìm kiếm như Optimal Mismatch.',
            ],
        },
        'nhan_xet': 'Maximal Shift nhỉnh hơn Optimal Mismatch một chút trên mọi kịch bản ngẫu nhiên '
                    '(ví dụ DNA, m = 8: 0,341 so với 0,353), cho thấy chiến lược ưu tiên độ dịch hiệu quả '
                    'khi phân bố ký tự đều.',
    },
    {
        'id': '17_skip_search', 'nhom': 3, 'ten': 'Thuật toán Skip Search',
        'nguon': 'Charras, Lecroq và Pehoushek, 1998',
        'y_tuong': [
            'Mọi lần xuất hiện của x (độ dài m) trong y phải chứa đúng một trong các ký tự y[m−1], '
            'y[2m−1], y[3m−1], … Do đó chỉ cần "nhìn" các ký tự cách nhau m vị trí này. Với mỗi ký tự '
            'c = y[j] được nhìn, các lần xuất hiện khả dĩ chỉ có thể là những cửa sổ đặt một ký tự c của '
            'mẫu trùng với y[j]. Các vị trí của từng ký tự trong mẫu được lưu sẵn trong các **thùng** '
            '(bucket) z[c].',
        ],
        'co_che': [
            ('b', '**Pha tiền xử lý:** z[c] = danh sách các vị trí i của mẫu có x[i] = c — O(m + σ).'),
            ('b', '**Pha tìm kiếm:** với j = m − 1, 2m − 1, …: với mỗi i ∈ z[y[j]], kiểm tra cửa sổ '
                  'y[j−i..j−i+m−1] bằng so sánh trực tiếp với x.'),
        ],
        'dac_diem': [
            'Dùng các thùng vị trí ký tự; tiền xử lý O(m + σ) thời gian và bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất; kỳ vọng O(n) phép so sánh ký tự.',
            'Thứ tự xét cửa sổ không phải trái sang phải đơn thuần mà theo từng nhóm m vị trí.',
        ],
        'tien_xu_ly': 'skip',
        'vet': 'grid',
        'dien_giai_vet': [
            'Chỉ ba ký tự văn bản được "nhìn": y[7] = A, y[15] = T và y[23] = G. Với y[7] = A, thùng '
            'z[A] = {6, 4, 2} cho ba cửa sổ j = 1, 3, 5 — cửa sổ thứ ba là lần xuất hiện. Thùng z[T] rỗng nên '
            'y[15] không sinh cửa sổ nào. Với y[23] = G chỉ cửa sổ j = 16 nằm trong văn bản. Tổng 11 phép so '
            'sánh và 3 lần tra thùng.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ)', 'tot': 'O(n/m)', 'tb': 'O(n)', 'xau': 'O(m·n)', 'bo_nho': 'O(m + σ)',
            'giai_thich': [
                'Có n/m ký tự được nhìn; mỗi ký tự sinh trung bình m/σ cửa sổ, mỗi cửa sổ trung bình O(1) '
                'phép so sánh khi văn bản ngẫu nhiên, cho kỳ vọng O(n/σ)·O(1) ⊆ O(n). Xấu nhất (y = aⁿ, '
                'x = aᵐ) mỗi ký tự được nhìn sinh m cửa sổ, mỗi cửa sổ m phép so sánh: O(m·n).',
            ],
        },
        'thao_tac': 'số lần tra thùng z[y[j]] (đúng ⌊n/m⌋)',
        'nhan_xet': 'Với bảng chữ cái 26 ký tự, Skip Search chỉ tốn 0,045 phép so sánh/ký tự (m = 8) — '
                    'thấp hơn hầu hết các thuật toán khác — vì thùng của mỗi ký tự rất nhỏ. Ngược lại trên '
                    'DNA, mỗi thùng chứa khoảng m/4 vị trí nên lợi thế giảm (0,343 với m = 32).',
    },
    # ------------------------------------------------------------------ NHÓM 4
    {
        'id': '18_horspool', 'nhom': 4, 'ten': 'Thuật toán Horspool',
        'nguon': 'Horspool, 1980',
        'y_tuong': [
            'Horspool đơn giản hóa Boyer-Moore: bỏ hàm hậu tố tốt (phức tạp, ít tác dụng với bảng chữ cái '
            'lớn) và dùng hàm ký tự tồi theo **ký tự cuối cửa sổ** y[j+m−1], bất kể sự không khớp xảy ra ở '
            'đâu. Vì độ dịch chỉ phụ thuộc y[j+m−1], các ký tự bên trong cửa sổ có thể được so sánh theo '
            'thứ tự bất kỳ.',
        ],
        'co_che': [
            ('b', '**bmBc[c]** = m − 1 − i với i là vị trí xuất hiện cuối cùng của c trong x[0..m−2]; '
                  'bằng m nếu c không xuất hiện.'),
            ('b', 'Ở mỗi lần thử: so sánh ký tự cuối x[m−1] với y[j+m−1] trước; nếu khớp mới so sánh '
                  'x[0..m−2] (từ trái sang phải). Sau đó dịch bmBc[y[j+m−1]].'),
        ],
        'dac_diem': [
            'Đơn giản hóa Boyer-Moore; dễ cài đặt.',
            'Tiền xử lý O(m + σ) thời gian, O(σ) bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất; số phép so sánh trung bình cho mỗi ký tự văn bản '
            'nằm giữa 1/σ và 2/(σ + 1).',
        ],
        'tien_xu_ly': 'horspool',
        'vet': 'grid',
        'dien_giai_vet': [
            'Ở j = 0, ký tự cuối y[7] = A ≠ G nên dịch bmBc[A] = 1. Ở j = 1 và j = 3, ký tự cuối là G (khớp) '
            'nhưng x[0] không khớp; dịch bmBc[G] = 2. Lần thử j = 5 khớp: so sánh x[7] trước rồi '
            'x[0..6]. Ở j = 8, ký tự cuối T không có trong mẫu nên mẫu dịch trọn m = 8 vị trí. Tổng 17 phép '
            'so sánh.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ)', 'tot': 'O(n/m)', 'tb': 'dưới tuyến tính', 'xau': 'O(m·n)', 'bo_nho': 'O(σ)',
            'giai_thich': [
                'Tốt nhất: ký tự cuối mọi cửa sổ không có trong mẫu, mỗi lần thử 1 phép so sánh và dịch m: '
                'O(n/m). Xấu nhất: y = aⁿ, x = aᵐ hoặc baᵐ⁻¹, mỗi cửa sổ so sánh m ký tự và dịch 1: O(m·n).',
            ],
        },
        'nhan_xet': 'Với bảng chữ cái lớn và mẫu dài (σ = 26, m = 32) chỉ cần 0,055 phép so sánh/ký tự — '
                    'nghĩa là chưa tới 1/18 số ký tự văn bản bị đọc. Trên DNA, các ký tự đều xuất hiện '
                    'trong mẫu nên độ dịch nhỏ và hiệu quả giảm (0,483 với m = 8).',
    },
    {
        'id': '19_quick_search', 'nhom': 4, 'ten': 'Thuật toán Quick Search',
        'nguon': 'Sunday, 1990',
        'y_tuong': [
            'Quick Search (còn gọi là thuật toán Sunday) nhận xét rằng sau mỗi lần thử, ký tự **ngay sau '
            'cửa sổ** y[j+m] chắc chắn sẽ nằm trong cửa sổ tiếp theo. Vì vậy dùng y[j+m] để tính độ dịch '
            'theo kiểu ký tự tồi; nếu ký tự này không có trong mẫu thì có thể dịch tới m + 1 vị trí.',
        ],
        'co_che': [
            ('b', '**qsBc[c]** = m − i với i là vị trí xuất hiện cuối cùng của c trong x; bằng m + 1 nếu '
                  'c không xuất hiện.'),
            ('b', 'Ở mỗi lần thử, cửa sổ được so sánh theo thứ tự bất kỳ (ở đây từ trái sang phải, tương '
                  'đương memcmp); sau đó dịch qsBc[y[j+m]].'),
        ],
        'dac_diem': [
            'Đơn giản hóa Boyer-Moore, chỉ dùng bảng ký tự tồi.',
            'Tiền xử lý O(m + σ) thời gian, O(σ) bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất; rất nhanh trong thực tế với mẫu ngắn và bảng '
            'chữ cái lớn.',
        ],
        'tien_xu_ly': 'qs',
        'vet': 'grid',
        'dien_giai_vet': [
            'Lần thử j = 0 so sánh từ trái sang phải, thất bại tại x[3]; ký tự sau cửa sổ y[8] = G nên dịch '
            'qsBc[G] = 1. Tại j = 1 và j = 3, ký tự sau cửa sổ là A, dịch qsBc[A] = 2. Sau lần xuất hiện tại '
            'j = 5, ký tự sau cửa sổ y[13] = T không có trong mẫu: dịch m + 1 = 9 tới j = 14. Tổng 15 phép '
            'so sánh.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ)', 'tot': 'O(n/(m + 1))', 'tb': 'dưới tuyến tính', 'xau': 'O(m·n)',
            'bo_nho': 'O(σ)',
            'giai_thich': [
                'Phân tích giống Horspool; độ dịch tối đa m + 1 thay vì m. Xấu nhất O(m·n) khi mọi cửa sổ '
                'khớp gần hết mà độ dịch chỉ là 1.',
            ],
        },
        'nhan_xet': 'Quick Search tốt hơn Horspool trên mọi kịch bản ngẫu nhiên (DNA m = 8: 0,394 so với '
                    '0,483) nhờ độ dịch tối đa m + 1 và việc ký tự dùng để dịch không bị "ràng buộc" với kết '
                    'quả so sánh trong cửa sổ.',
    },
    {
        'id': '20_tuned_bm', 'nhom': 4, 'ten': 'Thuật toán Tuned Boyer-Moore',
        'nguon': 'Hume và Sunday, 1991',
        'y_tuong': [
            'Tuned Boyer-Moore là một cài đặt rất hiệu quả của Horspool. Phần lớn thời gian của Horspool '
            'là các lần thử mà ký tự cuối cửa sổ không khớp; Tuned BM gom các lần dịch đó vào một **vòng '
            'lặp nhanh** (*fast loop*) không so sánh ký tự, được "trải" 3 lần mỗi vòng, chỉ dừng lại khi '
            'ký tự cuối cửa sổ bằng x[m−1].',
        ],
        'co_che': [
            ('b', 'Tính bmBc như Horspool, lưu shift = bmBc[x[m−1]] rồi gán bmBc[x[m−1]] = 0. Khi đó tra '
                  'bảng cho giá trị 0 nghĩa là ký tự cuối cửa sổ khớp.'),
            ('b', 'Đặt m bản sao của x[m−1] sau cuối văn bản làm **lính canh** để vòng lặp nhanh luôn dừng '
                  'mà không cần kiểm tra biên.'),
            ('b', 'Khi vòng lặp nhanh dừng, chỉ cần so sánh x[0..m−2] với cửa sổ (ký tự cuối đã chắc khớp), '
                  'sau đó dịch shift.'),
        ],
        'dac_diem': [
            'Biến thể (cài đặt tối ưu) của Horspool với vòng lặp nhanh và lính canh.',
            'Tiền xử lý O(m + σ) thời gian, O(σ) bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất; rất nhanh trong thực tế.',
        ],
        'tien_xu_ly': 'tuned',
        'vet': 'grid',
        'dien_giai_vet': [
            'Bảng mô phỏng chỉ hiển thị các cửa sổ có so sánh ký tự. Từ j = 0, vòng lặp nhanh tra bmBc[A] = 1 '
            'rồi dừng tại j = 1 vì y[8] = G (giá trị 0). Tại j = 7, vòng lặp nhanh tra bmBc[A] = 1 tới j = 8 '
            'rồi bmBc[T] = 8 tới j = 16 mà không có phép so sánh ký tự nào. Tổng cộng chỉ 10 phép so sánh ký '
            'tự và 13 lần tra bảng.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ)', 'tot': 'O(n/m)', 'tb': 'dưới tuyến tính', 'xau': 'O(m·n)', 'bo_nho': 'O(σ)',
            'giai_thich': [
                'Về mặt tiệm cận giống Horspool. Lợi ích nằm ở hằng số: vòng lặp nhanh chỉ gồm phép tra '
                'bảng và cộng, không có rẽ nhánh so sánh, nên rất thân thiện với bộ xử lý hiện đại.',
            ],
        },
        'thao_tac': 'số lần tra bảng bmBc để dịch (kể cả trong vòng lặp nhanh)',
        'nhan_xet': 'Trong các thuật toán dựa trên so sánh ký tự trực tiếp, Tuned BM có số phép so sánh thấp '
                    'nhất (0,006 phép so sánh/ký tự với σ = 26, m = 8) vì phần "lọc" đã được chuyển sang các lần tra bảng; tổng '
                    'chi phí (so sánh + tra bảng) vẫn ngang Horspool nhưng mỗi thao tác rẻ hơn.',
    },
    {
        'id': '21_raita', 'nhom': 4, 'ten': 'Thuật toán Raita',
        'nguon': 'Raita, 1992',
        'y_tuong': [
            'Raita quan sát rằng trong văn bản thực tế, các ký tự liền kề có sự phụ thuộc lẫn nhau, nên '
            'nếu ký tự cuối khớp thì ký tự kề nó cũng nhiều khả năng khớp. Vì thế, sau ký tự cuối, thuật '
            'toán so sánh ký tự **giữa** rồi ký tự **đầu** của mẫu — các vị trí "xa nhau" — trước khi so '
            'sánh phần còn lại. Độ dịch giống Horspool.',
        ],
        'co_che': [
            ('b', 'Thứ tự so sánh: x[m−1], x[⌊m/2⌋], x[0], sau đó x[1..m−2] (phần này có thể dùng memcmp '
                  'và sẽ so sánh lại x[⌊m/2⌋]).'),
            ('b', 'Độ dịch: bmBc[y[j+m−1]] như Horspool.'),
        ],
        'dac_diem': [
            'Biến thể của Horspool, thứ tự so sánh: cuối — giữa — đầu — còn lại.',
            'Tiền xử lý O(m + σ) thời gian, O(σ) bộ nhớ.',
            'Tìm kiếm O(m·n) trong trường hợp xấu nhất.',
        ],
        'tien_xu_ly': 'horspool',
        'vet': 'grid',
        'dien_giai_vet': [
            'Ở j = 1, ký tự cuối khớp nhưng ký tự giữa x[4] = A ≠ y[5] = G nên dừng sau 2 phép so sánh. Ở '
            'j = 3, ký tự cuối và giữa đều khớp, ký tự đầu không khớp. Ở lần xuất hiện j = 5, x[4] được '
            'so sánh hai lần (thứ tự 2 và 7) do phần x[1..m−2] được kiểm tra trọn vẹn. Tổng 19 phép so sánh.',
        ],
        'phuc_tap': {
            'tien_xu_ly': 'O(m + σ)', 'tot': 'O(n/m)', 'tb': 'dưới tuyến tính', 'xau': 'O(m·n)', 'bo_nho': 'O(σ)',
            'giai_thich': [
                'Giống Horspool. Riêng trường hợp xấu nhất có hằng số lớn hơn một chút vì ký tự giữa có thể '
                'bị so sánh hai lần ở mỗi cửa sổ khớp.',
            ],
        },
        'nhan_xet': 'Trên văn bản ngẫu nhiên (các ký tự độc lập), giả thiết phụ thuộc của Raita không đúng nên '
                    'kết quả xấp xỉ Horspool; ở kịch bản y = aⁿ, việc so sánh lại ký tự giữa làm chi phí tăng '
                    'lên ≈ 9 phép so sánh/ký tự (= m + 1).',
    },
]
