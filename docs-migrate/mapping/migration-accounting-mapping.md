# Rancangan Mapping Akuntansi

**Tanggal pembaruan:** 3 November 2026  
**Status:** DRAF UNTUK REVIEW; tidak mengimpor atau membentuk jurnal.

## Bukti dan prinsip

Workbook `OLI_JURNAL_Keseluruhan Jurnal_2026-01-01_2026-10-26.xlsx`, sheet `Keseluruhan Jurnal`, menampilkan Tanggal, Tipe Transaksi, No. Trans #, Deskripsi, Kode Perkiraan, Nama Perkiraan, Debit, Kredit. Target memiliki `journals` dan `journal_details`; `accounts` berisi 8 record dan `journals` 2 pada snapshot Tahap 2. Source code menunjukkan jurnal dibuat manual maupun otomatis oleh beberapa modul. Keseimbangan debit/kredit global belum terbukti; target record asalnya belum seluruhnya diketahui.

Jangan membentuk ulang jurnal dari modul yang sama sekaligus mengimpor laporan jurnal. Tentukan terlebih dahulu apakah jurnal source workbook adalah authoritative history, kontrol rekonsiliasi, atau duplikat hasil posting transaksi. Ini keputusan akuntansi **NEEDS REVIEW**.

## Kandidat mapping kolom

| Grain | Kolom source | Target kandidat | Transformasi dan kontrol | Status |
|---|---|---|---|---|
| Header | Tanggal | `journals.date_transaction` DATE NOT NULL | Serial Excel → kalender setelah validasi style; tidak menyamakan tanggal transaksi dengan posting date. | ASSUMED |
| Header | Tipe Transaksi | `journals.type_transaction_id` → lookup `type_transactions.slug` | Mapping nama/kode ke slug/domain harus disetujui; tidak infer dari label saja. | NEEDS REVIEW |
| Header | No. Trans # | `journals.relation_id` atau crosswalk dokumen; jenis transaksi terkait | Polymorphic semantics bervariasi; nomor tidak menjadi FK. Cocokkan dengan crosswalk transaksi yang unik. | NEEDS REVIEW |
| Header | Deskripsi | `journals.description` varchar(191) | Panjang/encoding perlu ukur; truncation dilarang tanpa keputusan. | NEEDS REVIEW |
| Detail | Kode Perkiraan | Lookup `accounts.code` → `journal_details.account_id` int NOT NULL | Validasi company, chart hierarchy, status akun dan natural-key collision. Tidak mengambil `accounts.id` dari laporan. | NEEDS REVIEW |
| Detail | Nama Perkiraan | Bandingkan `accounts.name` | Hanya validasi tambahan; bukan key. | ASSUMED |
| Detail | Debit | `journal_details.debet` double NOT NULL | Parse angka tanpa mengubah sisi; presisi/rounding disepakati. Nilai kosong dan negatif perlu review. | ASSUMED |
| Detail | Kredit | `journal_details.credit` double NOT NULL | Sama; tidak mengonversi debit menjadi kredit atau sebaliknya. | ASSUMED |
| Header total | Agregat Debit/Kredit per kelompok journal | Kandidat `journals.debet` dan `journals.credit` double NOT NULL | Hanya dapat dihitung setelah batas detail per header dan aturan total disahkan; harus direkonsiliasi dengan detail, bukan diperlakukan sebagai nilai source langsung. | NEEDS REVIEW |
| Header | Status approval/posting, creator, approver | `journals.status`, `posting_by`, `date_posting`, `created_by` | Tidak tersedia dalam kolom workbook. Jangan menandai posted/approved atau mengarang user. | UNKNOWN |
| Header/detail | PK/FK/journal grouping | `journals.id`, `journal_details.header_id` | Definisi awal/akhir kelompok journal pada report perlu diverifikasi dari seluruh row layout. | UNKNOWN |

## Kontrol akuntansi wajib sebelum persetujuan

1. Tetapkan grain satu journal header dan seluruh journal detail; klarifikasi baris lanjutan/subtotal/blank/merged.
2. Resolve seluruh tipe transaksi dan nomor transaksi ke entitas source melalui crosswalk; dokumen tahun 2025 jangan dihilangkan.
3. Resolve setiap kode akun pada company dan chart of accounts yang tepat. Delapan akun target yang ada berpotensi overlap; asal tiap akun belum diketahui.
4. Rekonsiliasi untuk setiap kelompok jurnal: jumlah debit = jumlah kredit pada presisi yang disetujui. Kebijakan tolerance/rounding harus disetujui akuntansi; jangan menciptakan tolerance sendiri.
5. Bandingkan jurnal laporan dengan jurnal yang akan dihasilkan oleh approval/posting aplikasi agar tidak terjadi penggandaan.
6. Tentukan apakah jurnal target berstatus draft, approved, atau posted berdasarkan bukti historis dan kebijakan aplikasi. Workbook tidak memuat status tersebut.
7. Pertahankan jumlah source/target per kelompok dan daftar unmatched/ambiguous untuk audit.

## Risiko dan UNKNOWN

- Tidak tersedia source account ID, company chart context, journal ID, detail ID, status posting, atau user audit trail.
- Belum terbukti bahwa `Tipe Transaksi` dan `No. Trans #` cukup untuk mengidentifikasi target `type_transaction_id` dan polymorphic `relation_id`.
- Aplikasi memiliki jurnal otomatis (invoice, receipt, deposit, pembayaran, retur tertentu) dan jurnal manual; pilihan strategy mustahil ditetapkan tanpa keputusan apakah import jurnal historis terpisah dari import operasional.
- Audit Tahap 2 mencatat 2 journal target dan total target berubah dari 2.376 menjadi 3.858 baris. Provenance dan potensi konflik nomor/duplicate harus diselesaikan sebelum ledger import.
- Aplikasi menghitung debit/kredit dari detail di sebagian alur, tetapi pemeriksaan global debit = kredit tidak ditemukan pada seluruh approve/post. Tidak boleh menganggap jurnal seimbang sebelum validasi independen.

**Keputusan yang diminta:** pemilik akuntansi menetapkan sumber ledger authoritative, perlakuan status posting, akun mapping, toleransi pembulatan, rekonsiliasi lintas tahun, dan apakah modul operasional akan membuat jurnal otomatis selama migrasi. Sampai itu diputuskan, seluruh jurnal hanya kandidat mapping dan tidak siap diimpor.
