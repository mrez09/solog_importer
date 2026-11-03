# Strategi Source-to-Target ID Mapping

**Tanggal pembaruan:** 3 November 2026  
**Status:** RANCANGAN STRATEGI; belum ada ID source/target yang dialokasikan dan tidak ada data yang diubah.

## Prinsip identitas

1. Semua primary key transaksi target memakai internal auto-increment `id` (lihat `target-audit.md`). Nomor dokumen workbook seperti `OLI...` adalah business reference, bukan PK target.
2. Source adalah laporan Excel dan tidak menyediakan ID relasional database yang terverifikasi. Source primary key dan foreign key: **UNKNOWN**.
3. Sebelum menyusun record target, siapkan crosswalk per entitas: `(source_workbook, sheet, source_document_type, source_document_no, source_line_locator)` → `(target_table, target_id)`. Baris locator harus stabil dan dapat ditelusuri ke workbook asli; definisi locator masih perlu review.
4. Jangan menghubungkan hanya dengan nama barang, pemasok, tanggal, atau nominal. Gunakan identifier source yang unik dan telah dikonfirmasi, lalu bukti pendukung untuk mencegah salah match.
5. ID record target yang sudah ada tidak diubah. Konflik ID/natural key harus ditangani lewat keputusan review, bukan overwrite.

## Skema crosswalk yang direkomendasikan

| Field crosswalk | Makna | Status |
|---|---|---|
| `source_file` | Path relatif workbook asli | VERIFIED tersedia |
| `source_sheet` | Worksheet sumber | VERIFIED tersedia |
| `source_doc_type` | PR, PO, GRN, PID, PI, SAP, RETUR, JOURNAL | ASSUMED enum; perlu persetujuan |
| `source_doc_no` | Nomor dokumen persis sebagaimana diekspor | VERIFIED field untuk sebagian report; uniqueness UNKNOWN |
| `source_line_locator` | Identitas baris/detail stabil (mis. nomor baris workbook setelah validasi struktur) | NEEDS REVIEW; merge/continuation harus ditangani |
| `source_parent_doc_no` | Referensi parent bila tersedia | VERIFIED hanya jika tertulis; bukan ID |
| `target_table`, `target_id` | Record internal target hasil resolusi/import | Target ID wajib internal; belum dialokasikan |
| `match_method`, `evidence`, `review_status` | Cara resolusi, bukti, dan status keputusan | NEEDS REVIEW; wajib audit trail |

Skema ini adalah spesifikasi konseptual, bukan file mapping/import yang bisa dijalankan. Jangan memasukkan data sensitif workbook ke crosswalk tanpa kebijakan akses yang disetujui.

## Candidate natural references dan relasi

| Entitas/relasi | Candidate key source | Target relasi | Status / syarat |
|---|---|---|---|
| PR header | Nomor pada workbook PR | `purchase_requests.code` ↔ internal `purchase_requests.id` | ASSUMED; uji uniqueness dan duplikat. |
| PR detail | Locator baris + nomor PR + item code | `purchase_request_details.header_id`, `item_id` | UNKNOWN; tidak ada line ID source. Jangan pakai item+qty saja sebagai kunci karena item bisa berulang. |
| PO header | Nomor pada workbook PO | `purchase_orders.code` | ASSUMED; bedakan nomor internal dari nomor eksternal dan sequence. |
| PO detail | Locator baris + nomor PO | `purchase_order_details.header_id`; opsional `purchase_request_detail_id` | UNKNOWN tanpa nomor/ID PR detail yang bisa ditelusuri. PO tanpa PR didukung. |
| GRN header | Nomor penerimaan pada workbook | `warehouse_receipts.code` | ASSUMED; uniqueness perlu verifikasi. Tanggal/pemasok bukan pengganti. |
| PO → GRN | Referensi PO di workbook Histori dan/atau sumber pendukung | `warehouse_receipts.purchase_order_id` | NEEDS REVIEW; satu receipt header berisi maksimum satu PO pada jalur kode yang ditelaah; satu PO dapat memiliki beberapa GRN. |
| GRN detail → PO detail | Baris/ID detail PO/GRN | `purchase_order_receipt_details.warehouse_receipt_detail_id`, `purchase_order_detail_id` | UNKNOWN dari laporan ringkas; membutuhkan relasi baris yang eksplisit. |
| PID header | Nomor PID | `um_suppliers.code` | ASSUMED; nomor dan grain laporan harus diperiksa. |
| PID → PO | `No Pesanan #` di PID | Tidak ada FK PO langsung terverifikasi pada `um_suppliers`; aplikasi punya jalur PID/payable/pembayaran | NEEDS REVIEW; jangan tulis `relation_id` tanpa konfirmasi makna dan `type_transaction_id`. |
| PI header | Nomor faktur | `invoice_vendors.code` | NEEDS REVIEW; tentukan nomor internal vs nomor faktur supplier dan uniqueness. |
| GRN → PI | `reff_no`/nomor penerimaan bila muncul di detail sumber atau histori | `invoice_vendor_details.reff_no` (kode teks); approval juga membuat payable/journal | NEEDS REVIEW; penggunaan ulang GRN belum dipastikan. Field PI report yang diaudit tidak secara eksplisit menampilkan GRN. |
| PI → payable | Nomor PI yang sudah tervalidasi | `invoice_vendors.payable_id` dan `payable_details.relation_id` | VERIFIED bahwa aplikasi membuat relasi saat approval; source-to-target matching tetap butuh crosswalk unik. |
| SAP → payable detail | `No. Faktur` dan No Bukti # | `debt_details.payable_id`, `payable_detail_id`, `debt_payments.header_id` | NEEDS REVIEW; butuh grain alokasi per invoice dan validasi pembayaran parsial/berganda. |
| PID → SAP | Nomor PID atau referensi alokasi yang eksplisit | `debt_details.um_supplier_id`, payable/deposit detail | NEEDS REVIEW; bukti hanya bahwa aplikasi bisa memakai deposit pada pembayaran, bukan relasi workbook unik. |
| Retur → receipt/PO | Nomor retur dan referensi asal yang eksplisit | dua jalur: `purchase_order_returns`/detail atau `returs`/`retur_details` | UNKNOWN; kolom laporan periode tidak membuktikan lifecycle. Workbook menyatakan tidak ada transaksi periode. |
| Jurnal → dokumen bisnis | `Tipe Transaksi` + `No. Trans #` | `journals.type_transaction_id`, `relation_id`; modul memegang `journal_id` | NEEDS REVIEW; relasi polymorphic/otomatis/manual bervariasi. Pasangan harus satu-ke-satu/kelompok yang dibuktikan. |
| Jurnal detail → akun | Kode Perkiraan | `journal_details.account_id` lookup `accounts.code` | NEEDS REVIEW; kode akun harus dicocokkan bersama company dan struktur akun. Nama akun saja tidak cukup. |

## Master/lookup target yang ada dan konflik

Snapshot Tahap 2 mencatat `companies` 4, `contacts` 8, `accounts` 8, dan `company_numberings` 441. `items`, `warehouses`, serta banyak master relevan tidak tercatat sebagai tabel berisi pada ringkasan itu (berarti kosong pada snapshot tersebut), tetapi schema dan relasinya tetap diperlukan. Jangan menganggap kosong sebagai aman untuk mengisi tanpa kebijakan master data.

Beberapa record target berisi penanda fixture `%CODEX%` pada kolom kode tertentu; sebagian seeder Golden yang terlihat tidak otomatis dipanggil `DatabaseSeeder`. Ini bukan bukti asal setiap record. `invoice_vendors` (1), `payables` (1), `payable_details` (1), dan `journals` (2) telah berisi record pada snapshot, sehingga calon nomor/kode historis berpotensi konflik. Asal record target per baris UNKNOWN; semua record harus dipertahankan sampai provenance/review.

Natural-key yang perlu direkonsiliasi tanpa menampilkan/mengubah data: kode item, kode supplier/kontak, kode akun per company, kode company/gudang, nomor transaksi source, `company_numberings`/counter, serta pembayaran dan saldo yang mungkin sudah ada. Matching aktual belum dijalankan pada tahap ini.

## Urutan resolusi relasi yang direkomendasikan

1. Definisikan grain/header/detail dan locator stabil setiap workbook; tandai baris continuation/merged, subtotal, dan blank presentasional.
2. Validasi keunikan nomor dokumen per jenis, termasuk referensi tahun 2025.
3. Review alias/nomor supplier, item, akun, company, warehouse; buat daftar ambiguous/unmatched untuk keputusan manual.
4. Bentuk crosswalk source doc → target header ID, kemudian source line → target detail ID.
5. Bentuk relasi PO→GRN, GRN→PI, PI→payable, PID→payment, SAP→payable detail, dan transaksi→journal hanya jika bukti referensi unik tersedia.
6. Validasi setiap FK target, orphan, kardinalitas dan jumlah total terhadap source/rekonsiliasi sebelum menyetujui mapping.

Urutan ini adalah rekomendasi untuk perencanaan setelah review. Belum ada crosswalk ID aktual, query pencocokan data, maupun operasi database yang dilakukan.
