# Pertanyaan Review Business Owner

**Tanggal pembaruan:** 3 November 2026  
**Status:** jawaban dan persetujuan belum tercatat.

Untuk tiap jawaban, catat keputusan, approver bernama/jabatan, tanggal, sumber bukti, cakupan waktu, dan pengecualian. Jawaban lisan perlu dituangkan dalam notulen/keputusan tertulis.

## Data Owner

1. Apakah sembilan workbook di `docs-migrate/README.md` lengkap untuk migrasi? Jika tidak, sebutkan file yang hilang/dikecualikan dan periode. **Bukti:** daftar ekspor resmi.
2. Apakah seluruh laporan hanya mewakili PT Ono Logistik Indonesia? Berikan company code/legal entity dan identifier yang menghubungkannya ke company target. **Bukti:** master/crosswalk resmi.
3. Berikan master supplier authoritative untuk 62 nama: kode stabil, nama legal, alias, status, tanggal berlaku.
4. Berikan master item untuk 61 kode: deskripsi, unit dasar, konversi, tanggal berlaku, dan apakah kode pernah dipakai ulang.
5. Berikan warehouse resmi beserta kode/periode dan aturan lokasi penerimaan.
6. Apakah Histori/pembayaran/jurnal tahun 2025 termasuk cakupan? Tetapkan cut-off dan laporan pelengkap.
7. Siapa pemilik/provenance record target yang ditemukan? Konfirmasi target migrasi terpisah dan bersih serta kebijakan mempertahankan semua record yang ada.

## Procurement

1. Untuk 873/990 detail GRN tanpa `Satuan`, dokumen/master apa yang menentukan unit pada tanggal transaksi? Apakah unit dapat dipastikan per item/periode? Jika tidak, apakah detail harus ditahan?
2. Untuk 28 RI terkait >1 PO, apakah satu dokumen RI benar-benar mencakup beberapa PO, beberapa receipt digabung dalam laporan, atau kasus lain? Kirim RI asli dan rinci PO/item/qty per kasus.
3. Apakah PO dapat diterima dengan beberapa GRN dan secara parsial? Apa batas/toleransi over-receipt dan bukti SOP/contohnya?
4. Apakah satu GRN dapat menjadi dasar beberapa PI? Bagaimana kuantitas/nilai partial invoice dibatasi agar tidak melebihi receipt?
5. Apakah Histori merupakan event log lengkap atau laporan ringkas/co-occurrence? Jelaskan definisi kolom dan aturan ekspornya.
6. Apakah ada laporan retur di luar laporan periode ini yang menyatakan nihil?

## Finance

1. Apakah satu SAP adalah bukti kas/bank, satu alokasi invoice, atau dapat memuat banyak alokasi? Berikan voucher, bukti bank, dan detail alokasi untuk kasus SAP–PI multi-link.
2. Bagaimana pembayaran parsial/gabungan, diskon, pajak/potongan, selisih, overpayment, dan saldo belum teralokasi dicatat pada periode sumber?
3. Untuk setiap 15 PID, berikan bukti pencairan, supplier, nilai/mata uang, penggunaan per PI, refund, dan saldo akhir. Apakah referensi PO hanya narasi atau relasi bisnis?
4. Bisakah nilai alokasi disahkan untuk empat pasangan PID–PI di Histori? Jika tidak, sumber apa yang membuktikan saldo PID?
5. Berikan contoh invoice resmi yang merekalkulasi pajak, diskon, pembulatan dan total; apakah formula berubah menurut periode/jenis?
6. Tetapkan cut-off dan apakah migrasi mencakup semua invoice/payment atau hanya saldo terbuka; berikan sumber rekonsiliasi payable.

## Accounting

1. Pilih ledger of record: operasi dengan auto-journal, jurnal historis authoritative tanpa auto-journal, atau operasi plus rekonsiliasi jurnal terpisah dengan pencegahan posting ganda. Jelaskan kontrol posting yang diperlukan.
2. Sahkan crosswalk chart of accounts: dari empat exact-code candidates, mana yang cocok secara makna, company, hierarchy dan tanggal berlaku? Berikan mapping resmi akun lain.
3. Untuk tiap tipe transaksi sumber, tentukan debit/kredit, akun dan apakah posting manual/otomatis; sertakan kebijakan dan contoh jurnal.
4. Apakah workbook jurnal mencakup periode yang sama dan lengkap? Bagaimana membedakan jurnal auto, manual, reversal, accrual dan jurnal yang telah tercermin dalam transaksi?
5. Tetapkan balance debit=kredit per dokumen/periode, toleransi pembulatan, mata uang, status posted/approved, serta disposisi jurnal tak seimbang/tanpa referensi.
6. Untuk identifier overlap jurnal dengan SAP (234), PI (36), RI (32), PID (2), bukti apa yang mengidentifikasi sumber jurnal dan mencegah double posting?
7. Bagaimana retur memengaruhi stok, payable, pajak dan akun jurnal? Bukti saat ini belum menetapkan efek payable secara lengkap.

## Application Reviewer

1. Sahkan ID/identifier target untuk company, contacts, items, warehouses, accounts dan `type_transactions`; berikan bukti semantik dan relasi, bukan nama mirip.
2. Jelaskan fungsi tiga baris `company_numberings` pada tiap 147 pasangan company/type dan apakah prefix/counter aman untuk nomor historis.
3. Konfirmasi required fields/default untuk PR, PO, GRN, PID, PI, payable, SAP dan journal. Bagaimana mengatasi warehouse, user/approval, tanggal kebutuhan/jatuh tempo, rack/quality, metode bayar yang tidak tersedia di workbook?
4. Tunjukkan code path yang membuktikan relasi PO tanpa PR, PO–GRN, GRN–PI, partial invoice, PID–payable, SAP–payable detail, retur dan journal, termasuk batas yang belum diuji runtime.
5. Konfirmasi approval hook yang memicu stok/payable/jurnal dan cara mencegah auto-posting bila jurnal historis dimuat.
6. Apakah aplikasi membatasi billed qty terhadap received qty dan pembayaran terhadap payable? Tunjukkan validator dan representasi partial.
7. Apakah `purchase_order_returns` dan `returs` adalah workflow berbeda? Kapan digunakan dan bagaimana efek stok/accounting masing-masing?
8. Audit menyebut Laravel 5.6/PHP 8.2 compatibility issue. Konfirmasi apakah temuan business rules hanya inspeksi statis dan verifikasi staging apa yang masih diperlukan.

## Bukti minimum

Setiap jawaban ditautkan ke ID pada `mapping-decision-register.md`, menyebut bukti yang dapat ditinjau ulang dan approver berwenang. Pengecualian, baris unresolved, dan dampak saldo/stok/jurnal harus tercatat. Jangan ubah status menjadi APPROVED tanpa persetujuan tertulis.
