# Migration Plan — Draft Terkendali

**Tanggal pembaruan:** 3 November 2026  
**Status:** **PROPOSED** untuk perencanaan; migrasi belum disetujui. Keputusan bisnis yang belum diselesaikan berstatus **NEEDS EVIDENCE** atau **BLOCKED**. Dokumen ini bukan izin mengakses/mengubah database atau menjalankan import.

## 1. Tujuan dan ruang lingkup

Rencana ini menyiapkan pemindahan histori pembelian dari sembilan laporan XLSX Accurate OLI ke aplikasi Laravel Solog OLI. Tujuannya mempertahankan histori dan relasi sejauh dapat dibuktikan, menyesuaikan data ke schema/business rules target, serta menghasilkan crosswalk dan rekonsiliasi yang dapat diaudit.

**IN SCOPE (PROPOSED):** profiling dan normalisasi salinan kerja; resolusi master; transaksi PR, PO, GRN, PID, PI, pembayaran, jurnal dan histori yang memenuhi bukti; preview, dry-run, rekonsiliasi dan laporan.

**OUT OF SCOPE:** mengubah schema/source application; mengedit workbook asli; membuat master sintetis; menghapus record target existing; mengimpor baris unresolved; memilih strategi accounting tanpa Accounting Owner; pemuatan production sebelum persetujuan, backup terverifikasi dan sign-off.

## 2. Workbook sumber dan periode

README menyebut PT Ono Logistik Indonesia, periode **1 Januari–26 Oktober 2026**; beberapa workbook relasi/finance dapat memuat referensi tahun 2025. Inventaris aktual saat audit berisi sembilan file. Catatan awal 8 vs 9 tetap discrepancy yang perlu konfirmasi kelengkapan oleh Data Owner.

| Modul | Workbook relatif di bawah `docs-migrate/2026-01-01_sd_2026-10-26/Unduh 2026-10-27/` |
|---|---|
| PR | `01 Pengadaan/OLI_PR_Rincian Permintaan Barang_2026-01-01_2026-10-26.xlsx` |
| PO | `01 Pengadaan/OLI_PO_Rincian Pesanan Pembelian_2026-01-01_2026-10-26.xlsx` |
| GRN/RI | `01 Pengadaan/OLI_GRN_Rincian Penerimaan Barang_2026-01-01_2026-10-26.xlsx` |
| PID | `02 Finance Pembelian/OLI_DP_Uang Muka Pembelian_2026-01-01_2026-10-26.xlsx` |
| PI | `02 Finance Pembelian/OLI_PI_Rincian Faktur Pembelian_2026-01-01_2026-10-26.xlsx` |
| SAP | `02 Finance Pembelian/OLI_BAYAR_Rincian Pembayaran Pembelian_2026-01-01_2026-10-26.xlsx` |
| Retur | `02 Finance Pembelian/OLI_RETUR_Rincian Retur Pembelian_2026-01-01_2026-10-26.xlsx` (README menyatakan tidak ada transaksi pada periode laporan) |
| Histori | `03 Jurnal dan Relasi/OLI_HISTORI_Histori Proses Pembelian_2026-01-01_2026-10-26.xlsx` |
| Jurnal | `03 Jurnal dan Relasi/OLI_JURNAL_Keseluruhan Jurnal_2026-01-01_2026-10-26.xlsx` |

Workbook adalah laporan, bukan database dump; key source dan FK tidak dianggap terverifikasi. Detail struktur per file berada pada `../audit/source-workbook-analysis.md` dan `../validation/source-data-profiling.md`.

## 3. Target dan pemisahan database

Schema/bukti aplikasi ditelaah dari `db_solog_oli_initial`. Rencana pengguna menyebut database migrasi nantinya terpisah dan bersih; identitas, provisioning, credential, lokasi dan owner database tersebut masih **NEEDS EVIDENCE**. Jangan menunjuk `db_solog_oli_initial` sebagai target import hanya karena schema-nya digunakan sebagai referensi.

Target migrasi harus database/environment terpisah yang disahkan, schema-nya sesuai versi aplikasi yang direview, dan terisolasi dari production serta `db_solog_oli_initial`. Sebelum koneksi, validasi identitas database melalui mekanisme aman tanpa mencetak credential. Perubahan data hanya dapat dilakukan pada tahap implementasi setelah otorisasi spesifik, review PREVIEW/DRY-RUN, dan prosedur keselamatan disetujui. Tahap dokumen ini seluruhnya read-only.

## 4. Baseline existing data

Stage 2 snapshot melaporkan 3.858 row di 104 tabel populated, dibanding 2.376 di snapshot terdahulu. Stage 3.1 memeriksa subset master/transaksi; sebagian record transaksi ada dan asal seluruh row belum diketahui. Angka tersebut snapshot terdokumentasi, bukan hitung ulang terkini.

**PROPOSED:** jangan hapus, ubah, atau tandai existing rows sebagai dummy. Simpan baseline counts/provenance dan konflik natural reference. Gunakan target migrasi terpisah yang disiapkan dan disahkan untuk uji/pemuatan. Jika target terpisah belum terverifikasi bersih dan cocok schema, status pemuatan **BLOCKED**. Record `invoice_vendors`, payables dan journals yang sudah ditemukan membutuhkan pemeriksaan provenance sebelum nomor/relasi dipakai.

## 5. Urutan dependensi yang diusulkan

Urutan berikut **PROPOSED**, bukan persetujuan business rule atau importer executable:

1. Konfirmasi source inventory, periode, versi target schema, baseline dan target terisolasi.
2. Sahkan/resolve master dan konfigurasi yang dibutuhkan: company, supplier/contact, item, unit/conversion, warehouse, account, transaction type, numbering. Jangan membuat master sintetis.
3. Buat crosswalk source document/line locator ke target internal ID; validasi duplikasi dan uniqueness sebelum transaksi.
4. PR header/detail, jika termasuk scope dan required fields serta status terbukti.
5. PO header/detail; tautkan ke PR hanya jika ref detail unik. Aplikasi mendukung PO tanpa PR (lihat `audit/business-rules.md`), tetapi histori sumber tetap perlu direkonsiliasi.
6. GRN header/detail dan relasi PO detail hanya setelah kasus multi-PO, unit, warehouse dan quantity diselesaikan.
7. PI header/detail/tax, lalu payable sesuai workflow dan keputusan field/status.
8. PID dan alokasi ke payable/payment hanya setelah nilai, sisi saldo, pemakaian dan sisa direkonsiliasi.
9. SAP/payment evidence dan allocation ke payable detail sesuai grain pembayaran yang disetujui.
10. Retur hanya bila ada sumber dalam scope dan workflow/efeknya disahkan. Laporan saat ini tidak memuat kandidat retur.
11. Jurnal mengikuti satu strategi ledger yang disetujui Accounting Owner; urutan dapat berubah sesuai strategi auto-journal vs historical ledger.
12. Rekonsiliasi keseluruhan dan sign-off sebelum tahap produksi.

**BLOCKED:** langkah 2, 6–11 belum bisa ditetapkan sebagai urutan pemuatan final tanpa keputusan terkait. Urutan FK yang tepat harus diperiksa kembali pada schema target versi yang akan digunakan.

## 6. Mapping dan crosswalk

Kandidat tabel berdasarkan `mapping/migration-data-dictionary.md`, schema/business rules dan `mapping/source-target-id-mapping.md`:

| Source report | Kandidat tabel target | Kondisi |
|---|---|---|
| PR | `purchase_requests`, `purchase_request_details` | Candidate; company, user/status/date_needed/item dan stable line grain belum lengkap. |
| PO | `purchase_orders`, `purchase_order_details` | Candidate; supplier/company/status/tax/required fields dan link PR perlu bukti. |
| GRN | `warehouse_receipts`, `warehouse_receipt_details`, `purchase_order_receipt_details` | Candidate; warehouse, unit pada 873 detail dan relasi 28 multi-PO RI belum terselesaikan. |
| PID | `um_suppliers`, `um_supplier_details`, `um_supplier_paids` | Candidate; saldo, tipe transaksi, supplier dan allocation belum dikonfirmasi. |
| PI | `invoice_vendors`, `invoice_vendor_details`, `invoice_vendor_taxes`, payable structures | Candidate; reff receipt, partial invoice, tax/discount, required fields dan posting perlu persetujuan. |
| SAP | `debts`, `debt_details`, `debt_payments`, `payables`, `payable_details` | Candidate; grain payment dan allocation/voucher belum dibuktikan. |
| Retur | `purchase_order_returns` + detail atau `returs` + `retur_details` | **BLOCKED/UNKNOWN:** dua workflow target berbeda; workbook periode ini menyatakan nihil. |
| Histori | Tidak diasumsikan menjadi transaksi target | Referensi relasi untuk validasi saja sampai grain/semantik dikonfirmasi. |
| Jurnal | `journals`, `journal_details`, `accounts`, `type_transactions` | **BLOCKED:** strategi ledger, grouping, status, accounts dan balance belum disetujui. |

Header dan detail harus tetap terpisah menurut grain report; nilai header merged/continuation tidak boleh diduplikasi sebagai detail. Nomor dokumen source disimpan sebagai business reference/crosswalk, bukan PK internal. Rancangan crosswalk konseptual: workbook path, sheet, doc type/no, stable line locator, parent reference, target table/internal ID, match method, evidence, review status dan import batch. Stable locator perlu divalidasi; nomor baris Excel bukan key final secara otomatis.

Semua kandidat kolom dan aturan null/transformasi merujuk pada Data Dictionary draft. Tidak ada kandidat yang dinaikkan menjadi VERIFIED hanya karena nama mirip.

## 7. Duplikat, incomplete records dan relasi parsial

- Duplikat dokumen/baris: deteksi dengan source file, sheet, doc ref dan locator yang disahkan; jangan auto-deduplicate. Repeated identifier occurrences di PR/PO/RI/PI perlu dibedakan antara pagination/repeated report row dan duplikasi transaksi.
- Empty/merged/continuation: normalisasi hanya dalam representasi kerja dengan aturan layout yang terdokumentasi. Bedakan nilai inherited presentasional dari NULL transaksi.
- Master unmatched/ambiguous, required target value yang tidak ada, unit kosong, FK unresolved, atau relasi multi-valued: status **HOLD** atau **NEEDS REVIEW**; tidak diberi default buatan.
- Relasi PO→GRN: 28 RI tampak terhubung ke >1 PO pada Histori sedangkan header GRN target memiliki satu `purchase_order_id`; tahan kelompok ini sampai dokumen penerimaan memutuskan grain.
- GRN→PI: aturan receipt reuse dan partial quantity belum diketahui. Wajib rekonsiliasi billed-vs-received per item/receipt sebelum membuat relasi.
- PI→SAP: satu SAP bisa melibatkan banyak PI dan satu PI banyak SAP menurut Histori. Crosswalk harus membedakan bukti pembayaran dari allocation; jangan match nominal/tanggal saja.
- PID: 15 PID, 13 PO refs, 4 PID–PI co-occurrences; co-occurrence bukan nilai allocation. Rekonsiliasi pemakaian/refund/sisa sebelum menyusun payable/payment.
- 2025 refs: pertahankan dan cari parent/source support; jangan buang hanya karena laporan utama 2026.

## 8. Payable, payment, deposit dan jurnal

Payable/PI dan pembayarannya harus direkonsiliasi per supplier, invoice, voucher, alokasi, potongan dan saldo. Formula pajak/diskon/rounding belum disahkan. Jangan mengarang akun potongan, metode bayar, status paid atau posting date.

**Journal strategy: BLOCKED.** Opsi yang menunggu Accounting Owner: (1) impor transaksi operasional dan gunakan auto-journal aplikasi; (2) impor jurnal historis authoritative tanpa membuat jurnal otomatis; (3) impor operasi disertai rekonsiliasi jurnal terpisah dengan mekanisme anti-double-posting. Workbook journal memiliki 5.645 kandidat account-detail rows dan ID overlap dengan SAP (234), PI (36), RI (32), PID (2); overlap tidak membuktikan duplikasi. Tidak membuat maupun mengimpor jurnal sampai ledger of record, grouping, account mapping, status posting, reversal, presisi dan balance debit=kredit disetujui.

## 9. Validasi dan rekonsiliasi

Kriteria validasi kandidat (toleransi/aturan wajib disahkan dahulu):

- jumlah header/detail source → accepted/held/rejected per workbook, dengan alasan setiap exception;
- crosswalk lengkap, unik sesuai kebijakan dan tidak ada target orphan/FK invalid;
- PR/PO/GRN qty dan unit; PO ordered vs received dan GRN received vs invoiced per item/receipt;
- invoice gross/tax/discount/net dan payable open/paid balance berdasarkan formula resmi;
- pembayaran: voucher total = allocation + komponen potongan/selisih sesuai policy; saldo payable dan PID tersisa tie-out;
- stok per item/unit/warehouse serta transaksi stock effect hanya setelah unit/location/valuation disahkan;
- jurnal per document/group, periode dan akun: debit=kredit dengan precision/tolerance resmi, status serta hubungan ke modul operasional;
- bandingkan hasil dengan workbook sumber, laporan saldo/control totals yang disetujui, dan baseline target; selisih harus memiliki disposition bisnis.

Tidak ada tolerance, tax formula, saldo awal, nilai default atau status yang ditetapkan di dokumen ini.

## 10. Logging, audit trail, rollback, idempotency

**PROPOSED untuk desain importer, belum implementasi:** tiap batch memiliki ID, waktu, operator, source file hash, sheet, config/mapping version, app/schema version, mode, target identity (tanpa secret), counts, exception report, crosswalk dan reconciliation outcome. Log tidak boleh mencatat credential atau seluruh data sensitif workbook.

Idempotency harus berdasarkan batch + source fingerprint + stable source locator + target entity, dengan conflict detection; jangan memakai nomor dokumen semata. Rerun harus berhenti/menyajikan diff pada existing crosswalk atau natural reference conflict; overwrite/upsert tidak dilakukan tanpa kebijakan dan otorisasi eksplisit.

Rollback proposal: hanya batch pada database migrasi terisolasi, melalui mekanisme batch-scoped yang diuji dan disetujui sebelum mode import. Jangan menjanjikan rollback pada production; wajib backup yang tervalidasi, maintenance/cutover procedure dan owner sign-off sebelum production. Tahap ini tidak menjalankan write atau membuat script rollback.

## 11. Blocker dan approval manusia

| Blocker | Status | Pemilik keputusan |
|---|---|---|
| Kelengkapan 9 workbook, beda audit 8 vs 9, cakupan 2025 | NEEDS EVIDENCE | Data Owner |
| Company/entity, supplier, item/unit, warehouse dan source master resmi | BLOCKED | Data Owner, Procurement, Application Reviewer |
| Chart of accounts, 4 candidate matches, tipe transaksi dan numbering | BLOCKED | Accounting, Application Reviewer |
| 873 unit GRN kosong dan 28 RI multi-PO | BLOCKED | Procurement, Data Owner |
| GRN reuse/partial invoice dan billed-vs-received | NEEDS EVIDENCE | Finance, Procurement, Application Reviewer |
| Grain SAP, pembayaran, potongan dan alokasi PI | BLOCKED | Finance |
| PID allocation/refund/saldo | BLOCKED | Finance |
| Ledger strategy, auto-journal suppression, grouping/status/balance | BLOCKED | Accounting Owner, Application Reviewer |
| Provenance/baseline target, target migrasi terpisah dan schema version | NEEDS EVIDENCE | Data Owner, Application Reviewer |
| Required target fields yang tidak ada dalam workbook dan disposition hold | NEEDS REVIEW | Business Owner terkait, Application Reviewer |

Daftar keputusan rinci ada di `../decision/mapping-decision-register.md`; belum ada status APPROVED. Jangan menginterpretasikan **PROPOSED** sebagai otorisasi.

## 12. Kriteria sukses dan sign-off

Sukses bukan hanya “import command selesai”. Minimal: cakupan sumber disahkan; semua accepted row memiliki bukti/mapping; held rows terdaftar; tidak ada orphan/duplicate yang tidak ditangani; total kuantitas/nilai/payable/payment/stok/jurnal tie-out pada aturan yang disetujui; crosswalk dan audit log lengkap; hasil PREVIEW/DRY-RUN disetujui; test pada database staging terisolasi lulus; rollback/recovery dan backup diverifikasi; Accounting, Procurement, Data Owner dan Application Reviewer menandatangani domain masing-masing; persetujuan produksi spesifik diberikan sebelum production.

## 13. Status kesiapan

- **APPROVED:** belum ada keputusan atau pemuatan yang disetujui pada dokumen Stage 3.2.
- **PROPOSED:** urutan dependensi, pemisahan database, hold unresolved rows, audit trail dan kontrol idempotency di atas untuk review.
- **NEEDS EVIDENCE:** cakupan sumber, master, field wajib, relasi parsial, angka dan status bisnis.
- **BLOCKED:** mapping/pemuatan master yang tidak dikenal, unit/relasi ambiguous, pembayaran/deposit yang belum dialokasikan, serta jurnal sebelum keputusan Accounting.
- **OUT OF SCOPE:** implementasi importer, perubahan database/source/workbook, eksekusi migrasi, dan produksi.
