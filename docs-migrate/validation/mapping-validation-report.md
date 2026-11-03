# Laporan Validasi Kandidat Mapping — Tahap 3.1

**Tanggal pembaruan:** 3 November 2026  
**Status keseluruhan:** **BELUM SIAP** untuk gerbang persetujuan mapping/Tahap 4. Diperlukan keputusan bisnis, procurement, finance, accounting, dan reviewer aplikasi.

## Ringkasan pemeriksaan

- `AGENTS.md`, `docs-migrate/README.md`, audit Tahap 1/Tahap 2, empat dokumen mapping Tahap 3, dan versi dokumentasi relevan di `audit/abc/` telah ditelaah.
- Direktori sumber berisi **9 workbook XLSX**, bukan 8 seperti tertulis di sebagian audit awal. Selisih historis tetap didokumentasikan; dokumen lama tidak ditimpa.
- Profil XML memberi ukuran fisik, header/detail kandidat, merge, format, dan identifier untuk sembilan workbook. Baris fisik/detail laporan tidak disamakan dengan record database.
- Target dikonfirmasi `db_solog_oli_initial` dan diperiksa menggunakan transaksi consistent snapshot READ ONLY. Pemeriksaan ini hanya mencakup master yang diminta dan tabel transaksi terkait; total database tidak dihitung ulang. Audit Tahap 2 terakhir mencatat 3.858 baris, naik dari 2.376.
- Tidak ada database, source code, workbook sumber, atau dokumen audit/mapping Tahap 3 yang diubah. Empat laporan validasi ini merupakan output baru.

## Hasil per modul

| Modul | Kandidat struktur target | Bukti/profil terbaru | Status kandidat mapping dan hal yang belum selesai |
|---|---|---|---|
| PR | `purchase_requests` + `purchase_request_details` | 736 nomor unik; 1.121 baris detail kandidat; 10 nomor histori tambahan | **ASSUMED / NEEDS REVIEW**: nomor dan kuantitas terlihat, tetapi company, warehouse, date needed, actor/status, qty approve dan detail ID belum tersedia. Satu pengulangan nomor belum diklasifikasi. |
| PO | `purchase_orders` + `purchase_order_details`, optional PR detail/pivot | 588 nomor unik; 1.078 detail kandidat; Histori punya 130 PO-only dan 2 export-only; 654 pasangan PO-RI | **NEEDS REVIEW**: supplier/item/company, currency, PPN, total, status/payment type, due date dan `files` wajib belum dapat dipetakan. Co-occurrence menunjukkan 28 RI terkait >1 PO, tidak selaras langsung dengan satu PO per target receipt header. |
| GRN/RI | `warehouse_receipts`, `warehouse_receipt_details`, `purchase_order_receipt_details` | 584 nomor unik; 990 detail kandidat; 873 blank `Satuan`; 13 RI-only history; 28 RI berpasangan dengan >1 PO | **NEEDS REVIEW**: unit, warehouse, rack, quality, PO-detail link dan satu-PO-per-header perlu penyelesaian. `purchase_order_id` dipakai kode tetapi tidak tercatat sebagai FK deklaratif target. |
| PID | `um_suppliers`, `um_supplier_details`, `um_supplier_paids` | 15 PID unik, 13 PO refs, 15/15 ada di Histori; 4 PID-PI pairs | **NEEDS REVIEW**: arah saldo, pemisahan terpakai/retur, cara bayar, akun, status dan hubungan PID→payable/payment belum terdefinisi untuk report source. |
| PI | `invoice_vendors`, `invoice_vendor_details`, `invoice_vendor_taxes`, `payables`, `payable_details` | 597 nomor unik; 1.060 detail kandidat; 95 PI-only history; satu `invoice_vendors` target ada, tanpa exact source-code match | **NEEDS REVIEW**: kolom tanggal/nomor external, qty/unit price, pajak/diskon/total, account/category, GRN link dan status tidak lengkap atau belum disetujui. 1 RI→multiple PI terlihat untuk sebagian pasangan; reuse perlu review. |
| SAP | `debts`, `debt_details`, `debt_payments`, `payable_details` | 287 SAP unik; 664 detail kandidat invoice ref; 49 SAP-only history; 5 referensi non-SAP terdeteksi | **NEEDS REVIEW**: grain bukti vs alokasi, payable detail, payment type/account, partial payment, diskon, overpayment, PID dan required metadata belum dapat direkonstruksi penuh. |
| Retur | `purchase_order_returns` + detail **atau** `returs` + `retur_details` | 0 retur identifier dan 0 detail kandidat; README menyatakan tidak ada transaksi periode | **UNKNOWN**: tidak ada contoh transaksi untuk memilih dua lifecycle berbeda; tidak ada bukti cakupan luar periode atau efek payable. Jangan membuat record kosong. |
| Histori proses | Crosswalk bukti; tidak ada target transaction table direct yang terbukti | 3.761 reference occurrences/3.105 unique lintas tipe; several 2025 refs; perbedaan per tipe di laporan relasi | **VERIFIED** sebagai laporan referensi, **UNKNOWN** sebagai tabel transaksi/FK. 10 PR, 130 PO, 13 RI, 95 PI, 49 SAP hanya ada di Histori; review parent/period/format. |
| Jurnal | `journals`, `journal_details`, lookup `accounts`, `type_transactions` | 5.645 detail akun kandidat; 88 kode akun source (4 exact-code candidate match); nomor transaksi jurnal overlap 234 SAP, 36 PI, 32 RI, 2 PID | **NEEDS REVIEW**: grouping header/detail, akun/company/type, journal status, balance, posting, source relation dan strategi mencegah jurnal ganda belum selesai. |

## Rekonsiliasi master target

Read-only snapshot terbaru untuk tabel yang diminta mencatat: `companies` 4, `contacts` 8, `items` 0, `warehouses` 0, `accounts` 8, `type_transactions` 49, `company_numberings` 441. Key exact duplicate tidak ditemukan pada code/nama/slug individual yang diprofilkan. `company_numberings` memiliki 147 pasangan company/type, setiap pasangan berisi 3 baris; ini bukan otomatis duplikat, tapi struktur numbering perlu dikonfirmasi.

Perbandingan kandidat: 61 source item codes vs 0 target items; 62 nama pemasok vs 8 contacts (3 berflag supplier/vendor) dengan 0 exact normalized name overlap; 88 source account codes vs 8 target accounts, 4 exact normalized matches; 11 tipe transaksi source vs 49 target names, 1 exact name match dan 0 slug matches. Semua exact match hanya kandidat tekstual, bukan bukti identitas. Tidak ada company/warehouse code source untuk mapping langsung.

Tabel transaksi target terkait yang dihitung pada snapshot: PR 0, PO 0, warehouse receipt 0, PID 0, invoice vendor 1, debts/SAP 0, PO return 0, return 0, payable 1, payable detail 1, journal 2, journal detail 4. Exact source document code matches: 0 pada tabel PR/PO/receipt/PID/invoice/debt yang diperiksa. Satu invoice, satu payable, satu payable detail, dua journal, dan empat journal detail tetap dipertahankan; provenance record belum diketahui.

## Baris lanjutan, duplikasi, dan locator

- Empat workbook PR/PO/GRN/PI masing-masing mempunyai satu pengulangan token nomor; belum terbukti apakah halaman/section cetak ulang atau duplicate business document.
- Histori mengulang identifier antarbaris secara alami; perbedaan source-export vs histori ditandai unresolved, bukan di-deduplicate.
- Banyak merged ranges dan header berulang menyebabkan nomor baris bukan key stabil. Kandidat locator adalah hash file + sheet + physical row + tipe/grain + referensi dokumen + ordinal detail; perlu persetujuan dan pengujian repeatability sebelum dipakai sebagai ID mapping.
- GRN memiliki 873 blank `Satuan` pada 990 baris kode-item kandidat yang belum dijelaskan oleh vertical merge. Tidak diisi dengan default.

## Jurnal dan risiko double posting

Workbook jurnal memiliki 5.645 baris detail akun kandidat. Nomor transaksi yang sama juga ditemukan pada laporan transaksi operasional (234 SAP, 36 PI, 32 RI, 2 PID identifier unik). Source code membuat jurnal otomatis pada beberapa alur dan juga mendukung jurnal manual. Ini bukti risiko overlap; bukan bukti tiap pasangan pasti duplikat jurnal. Jumlah jurnal distinct/debit-credit balance tidak dapat dipastikan sebelum batas header/detail dan status posting tervalidasi. Jangan mengimpor jurnal historis bersamaan dengan generate otomatis sebelum accounting owner menentukan sumber authoritative dan rekonsiliasi.

## Keputusan yang masih diperlukan

1. Owner data mengonfirmasi grain, duplicate document occurrences, stable line locator, baris continuation/merged, dan unmatched reference—including 2025.
2. Procurement menyetujui relasi PR/PO/GRN, 28 RI multi-PO pada Histori, unit kosong, warehouse, qty, dan handling unmatched.
3. Finance menyetujui match supplier/item, mata uang, invoice receive/due date, formula subtotal/pajak/diskon/pembulatan, PID dan alokasi pembayaran.
4. Accounting menyetujui account/type mapping, sumber ledger authoritative, toleransi keseimbangan, posting status, dan pemisahan import jurnal dari generate otomatis.
5. Reviewer aplikasi menetapkan nilai wajib yang sumbernya tidak menyediakan, target numbering, status/approval, creator, warehouse/rack/quality, payment metadata, serta kebijakan master data kosong.
6. Provenance dan konflik record target yang sudah ada ditinjau tanpa menghapus atau menimpa data.

## Rekomendasi Tahap 4

**Belum siap masuk Tahap 4 — Migration Plan final.** Kandidat table areas dan sebagian kode alur aplikasi telah ditemukan, tetapi pemetaan master, FK/detail line, unit, nominal, status, target defaults, unmatched histori, retur, serta strategi jurnal belum disepakati. Sesuai gerbang `AGENTS.md`, lanjutkan ke Migration Plan setelah checklist mapping disetujui pihak bisnis/aplikasi/akuntansi dan semua mapping wajib yang belum diketahui memiliki keputusan atau jalur unresolved yang disahkan.

## Bukti dan dokumen pendukung

- [Profil workbook sumber](source-data-profiling.md)
- [Rekonsiliasi master data target](master-data-reconciliation.md)
- [Validasi relasi](relationship-validation.md)
- Kandidat mapping tahap sebelumnya: `docs-migrate/mapping/`.
- Audit business rules/schema: `docs-migrate/audit/business-rules.md`, `target-audit.md`, `workflow-analysis.md`, `target-data-classification.md`.
