# Migration Data Dictionary — Kandidat Mapping Tahap 3

**Tanggal pembaruan:** 3 November 2026  
**Status:** DRAF UNTUK REVIEW; bukan mapping final dan belum disetujui untuk impor.

## Dasar, batas, dan konvensi

Dokumen ini mengikuti `AGENTS.md`, `docs-migrate/README.md`, dokumen audit di `docs-migrate/audit/`, termasuk salinan DOCX di `audit/abc/`. Sumber transaksi ialah workbook laporan XLSX, bukan dump schema lama. Karena itu tipe kolom source database, grain record lengkap, aturan NULL, unique key, dan FK source **UNKNOWN**. Tipe source di bawah adalah interpretasi format sel yang terlihat, bukan tipe database.

Target yang dipakai ialah schema `db_solog_oli_initial` pada [target-audit.md](../audit/target-audit.md). Target berisi 3.858 baris pada snapshot Tahap 2 (sebelumnya 2.376); asal setiap record belum seluruhnya diketahui. Jangan menimpa atau menganggap master target cocok tanpa rekonsiliasi.

Arti status:

- **VERIFIED**: pemetaan semantik dan hubungan dibuktikan langsung oleh sumber dan implementasi.
- **ASSUMED**: kandidat berdasarkan label/format yang masuk akal, perlu konfirmasi.
- **UNKNOWN**: pasangan/aturan belum terbukti.
- **NEEDS REVIEW**: keputusan bisnis/akuntansi atau resolusi konflik diperlukan.

Semua tabel transaksi target mencantumkan `id` internal auto-increment. Jangan memakai nomor source sebagai `id`; strategi ada pada [source-target-id-mapping.md](source-target-id-mapping.md). Detail ditautkan melalui `header_id` kecuali ada struktur penghubung khusus.

**Kontrol wajib untuk setiap mapping di tabel dokumen ini:** penanganan duplicate business key = deteksi dan hold untuk review (key source belum terverifikasi; tidak ada dedup otomatis); PK target = internal auto-increment baru/yang sudah ada dan dicatat di crosswalk, tidak pernah nomor workbook; FK = hanya lewat crosswalk/master resolution yang disetujui dan validasi parent, selain itu unresolved/hold; NULL/empty = bedakan blank merged/continuation dari nilai kosong dan jangan mengisi kolom wajib dengan tebakan; default = hanya default schema atau business rule yang terverifikasi dan disetujui, bukan default script. Setiap kandidat per kolom tetap perlu review sebelum status VERIFIED/final.

## 1. Purchase Request (PR)

**Sumber:** `OLI_PR_Rincian Permintaan Barang_2026-01-01_2026-10-26.xlsx`, sheet `Rincian Permintaan Barang`. Kolom sumber: Nomor, Tanggal, Kode #, Nama Barang, Kuantitas. Grain laporan mengandung header dan rincian berulang; aturan baris masih perlu validasi.

| Bagian | Kolom sumber (tipe sel) | Kandidat target (tipe; wajib?) | Transformasi / NULL / bukti | Status |
|---|---|---|---|---|
| Header | Nomor (teks) | `purchase_requests.code` varchar(191), nullable | Pertahankan nomor sebagai natural reference setelah validasi duplikasi; jangan isi `id`. Blank: UNKNOWN. | ASSUMED |
| Header | Tanggal (Excel date serial/tampilan tanggal) | `purchase_requests.date_request` date, NOT NULL | Konversi serial Excel ke tanggal kalender setelah validasi style/epoch; zona waktu tidak tampak relevan bagi DATE tetapi perlu validasi. | ASSUMED |
| Header wajib target, tanpa sumber | — | `purchase_requests.company_id` int NOT NULL; `date_needed` date NOT NULL; `create_by` int NOT NULL; `status` int NOT NULL; `is_pallet` tinyint NOT NULL | Nilai tidak boleh diisi default/ID tebak. Konteks perusahaan, tanggal kebutuhan, pembuat, status lifecycle, dan flag pallet perlu sumber/keputusan. | NEEDS REVIEW |
| Detail | Kode # (teks/kode) | Lookup `items.id` int NOT NULL; `purchase_request_details.item_id` int NOT NULL | Resolve lewat kode barang yang disetujui; kode tidak sama dengan ID. Tidak cocok/duplikat => karantina review. | NEEDS REVIEW |
| Detail | Nama Barang (teks) | Kemungkinan `items.name` untuk lookup saja; bukan nilai transaksi target | Nama hanya atribut pencocokan sekunder, tidak cukup untuk resolve item. | UNKNOWN |
| Detail | Kuantitas (angka) | `purchase_request_details.qty` double NOT NULL; `qty_approve` double NOT NULL; `qty_po` int NOT NULL | Parse angka lokal sesuai isi cell; kuantitas approve/PO tidak tersedia dalam laporan. Jangan menyamakan qty diminta dengan qty disetujui/PO. | NEEDS REVIEW |
| Relasi | Nomor PR pada workbook PO/Histori (teks) | `purchase_order_details.purchase_request_detail_id` int NULL dan/atau pivot `purchase_order_purchase_request` | Butuh resolusi PR detail, bukan hanya header. Histori lintas proses bukan bukti uniqueness atau detail link. | NEEDS REVIEW |
| Metadata | status, approve/reject, creator, audit timestamps | `purchase_requests.status`, `approve_by`, `reject_by`, `date_approved`, `date_reject`, timestamps | Tidak tersedia lengkap pada ekspor. Jangan menyimpulkan status target dari keberadaan dokumen. | UNKNOWN |

Target PR/detail ditemukan kosong pada snapshot awal sebagaimana dijabarkan schema audit; status terkini perlu snapshot baru sebelum tahap migrasi.

## 2. Purchase Order (PO)

**Sumber:** `OLI_PO_Rincian Pesanan Pembelian_2026-01-01_2026-10-26.xlsx`, sheet `Rincian Pesanan Pembelian`.

| Bagian | Kolom sumber (tipe sel) | Kandidat target (tipe; wajib?) | Transformasi / NULL / bukti | Status |
|---|---|---|---|---|
| Header | Nomor (teks) | `purchase_orders.code` varchar(191), nullable | Simpan sebagai referensi source; nomor target tidak otomatis dihasilkan ulang. | ASSUMED |
| Header | Tanggal (date serial) | `purchase_orders.po_date` date NOT NULL | Konversi Excel setelah cek style dan tanggal valid. | ASSUMED |
| Header | Pemasok (teks) | Lookup `contacts.id` → `purchase_orders.supplier_id` int NOT NULL | Rekonsiliasi supplier melalui natural key yang disepakati (kode legal/pajak bila tersedia); nama saja tidak cukup. | NEEDS REVIEW |
| Detail | Kode # (teks) | Lookup `items.id` → `purchase_order_details.item_id` int NOT NULL | Pemetaan item; konflik kode perlu review. | NEEDS REVIEW |
| Detail | Nama Barang (teks) | `items.name` untuk pembanding, bukan FK | Tidak menjadi kunci tunggal. | UNKNOWN |
| Detail | Kuantitas (angka) | `purchase_order_details.qty` double NOT NULL | Parsing angka; unit dan presisi perlu konfirmasi. | ASSUMED |
| Detail | @Harga (angka) | `purchase_order_details.price` double NOT NULL | Parse nilai tanpa menerapkan pembulatan yang belum disepakati. Mata uang belum ada field terpetakan. | ASSUMED |
| Detail | Total Harga (angka) | Kandidat `purchase_order_details.total` double NOT NULL | Tidak diasumsikan sebagai qty × harga; rekonsiliasi sumber dan aturan kalkulasi diperlukan. | NEEDS REVIEW |
| Header/summary | Sub Total (angka) | Kandidat agregat target; `purchase_orders` tidak menunjukkan field subtotal pada schema yang diaudit | Jangan dipindah ke kolom lain atau direkonstruksi tanpa definisi. | UNKNOWN |
| Header/summary | Total Biaya (angka) | Kandidat agregat/biaya target tidak teridentifikasi langsung | Definisi komponen dan target field perlu pemilik proses. | UNKNOWN |
| Header/summary | Total (angka) | `purchase_orders` tidak memiliki field total pada schema yang diaudit | Rekonsiliasi terhadap detail; tidak membuat field baru. | UNKNOWN |
| Header | Mata Uang (teks/kode) | Tidak ada field currency yang teridentifikasi di `purchase_orders`/detail | Konversi/penyimpanan mata uang perlu keputusan dan bukti konfigurasi. | NEEDS REVIEW |
| Header wajib target, tanpa sumber | — | `company_id`, `supplier_id`, `po_by`, `po_date`, `po_status`, `payment_type`, `ppn_is_faktur` | Perusahaan, pembuat, status, tipe pembayaran, perlakuan pajak wajib disediakan melalui sumber tepercaya/approval; jangan isi nilai default tebakan. | NEEDS REVIEW |
| Detail wajib target, tanpa sumber | — | `files` varchar(191) NOT NULL; `ppn` dan `total` double NOT NULL | `files` tidak memiliki sumber; `ppn` hanya jika dapat dibuktikan dari workbook/aturan lain. `receive` merupakan status kuantitas operasional, bukan sumber PO. | NEEDS REVIEW |
| Relasi PR | Nomor PR mungkin di Histori | `purchase_request_detail_id` nullable; pivot PO-PR | PO langsung tanpa PR didukung aplikasi. Hanya tautkan jika histori dapat mengidentifikasi detail secara unik. | NEEDS REVIEW |

Sumber code: `PurchaseOrderController`, model `PurchaseOrder`, `PurchaseOrderDetail`; business rules menyebut `qty × price` sebagai helper total, tetapi itu bukan bukti formula keseluruhan biaya/pajak.

## 3. Goods Receipt Note (GRN/RI)

**Sumber:** `OLI_GRN_Rincian Penerimaan Barang_2026-01-01_2026-10-26.xlsx`, sheet `Rincian Penerimaan Barang`.

| Bagian | Kolom sumber (tipe sel) | Kandidat target (tipe; wajib?) | Transformasi / NULL / bukti | Status |
|---|---|---|---|---|
| Header | Nomor (teks) | `warehouse_receipts.code` varchar(191), nullable | Nomor source sebagai cross-reference; unique/duplikasi harus diuji. | ASSUMED |
| Header | Tanggal (date serial) | `warehouse_receipts.receive_date` timestamp NOT NULL | Kolom target memuat timestamp; jam/zona tidak dibuktikan, jadi konversi tanggal ke jam tidak boleh dipilih tanpa persetujuan. | NEEDS REVIEW |
| Header | Pemasok (teks) | Tidak ada supplier FK pada header `warehouse_receipts` yang teridentifikasi | Jangan paksa menjadi `customer_id`; makna itu tidak setara. Mungkin hanya atribut laporan/PO. | UNKNOWN |
| Detail | Kode # (teks) | Lookup `items.id` → kemungkinan `warehouse_receipt_details.item_id` nullable | Kode harus resolve ke item target; FK detail GRN aktual terkait item perlu diperiksa pada schema/model dan jalur transaksi. | NEEDS REVIEW |
| Detail | Nama Barang (teks) | Kandidat `warehouse_receipt_details.item_name` varchar(191), nullable | Hanya snapshot label jika business rule mengizinkan; jangan gunakan sebagai identitas. | ASSUMED |
| Detail | Kuantitas (angka) | `warehouse_receipt_details.qty` double NOT NULL | Parse angka; konfirmasi apakah quantity laporan sama dengan qty fisik, qty stok, atau unit kemasan. | NEEDS REVIEW |
| Detail | Satuan (teks) | Tidak ada satuan detail GRN yang teridentifikasi langsung | Konversi ke unit target belum diketahui. | UNKNOWN |
| Relasi PO | Tidak ada kolom PO langsung pada sheet ini | `warehouse_receipts.purchase_order_id` int nullable; `purchase_order_receipt_details` menghubungkan detail | Bisa ditautkan hanya dari histori/referensi yang unik dan detail item yang dapat dibuktikan; PO per header satu, satu PO dapat beberapa GRN menurut kode. | NEEDS REVIEW |
| Header wajib target, tanpa sumber | — | `warehouse_id`, `create_by`, `total_qty`, `status`, `company_id`, `is_seen` | Gudang, pengguna, total/status dan flag wajib tidak tampak jelas di laporan; jangan mengarang. | NEEDS REVIEW |
| Detail wajib target, tanpa sumber | — | `rack_id`, `create_by`, `weight`, `volume`, `long`, `wide`, `high`, `barcode`, `imposition`, `leftover_warehouse`, `leftover_stuffing`, `weight_per_kg`, `volume_per_meter`, `storage_type`, `is_exists`, `is_use_pallet`, `pallet_qty`, `is_good`, `qty_2`, `return_qty`, `return_receipt_qty` | Field operasional/stock/quality berstatus UNKNOWN atau NEEDS REVIEW; beberapa tidak dapat diturunkan dari laporan. Jangan gunakan default schema sebagai fakta bisnis. | NEEDS REVIEW |

Sumber code: `ReceiptController`; target header `warehouse_receipts`, detail `warehouse_receipt_details`, penghubung `purchase_order_receipt_details`. Laporan hanya memuat satuan generik dan bukan data rak/quality lengkap.

## 4. Uang Muka Pembelian (PID)

**Sumber:** `OLI_DP_Uang Muka Pembelian_2026-01-01_2026-10-26.xlsx`, sheet `Uang Muka Pembelian`.

| Bagian | Kolom sumber (tipe sel) | Kandidat target (tipe; wajib?) | Transformasi / NULL / bukti | Status |
|---|---|---|---|---|
| Header | Nomor (teks) | `um_suppliers.code` varchar(191), nullable | Pertahankan sebagai referensi source; uniqueness belum dibuktikan. | ASSUMED |
| Header | Tanggal (date serial) | `um_suppliers.date_transaction` date NOT NULL | Konversi date serial tervalidasi. | ASSUMED |
| Header | Total (angka) | Kandidat saldo awal transaksi ke `um_suppliers.debet`/`credit` atau detail | Makna sisi debit/kredit dan saldo awal harus disahkan; jangan pilih sisi berdasar label “uang muka”. | NEEDS REVIEW |
| Header/rekap | Terpakai/Retur (per Tgl) (angka/tanggal atau label gabungan) | Tidak ada pasangan langsung tunggal pada header `um_suppliers` | Perlu parsing grain dan pemisahan pemakaian vs pengembalian; detail sumber/struktur report wajib diverifikasi. | UNKNOWN |
| Header/rekap | Sisa Uang Muka (per Tgl) (angka/tanggal atau label gabungan) | Tidak ada pasangan langsung sebagai transaksi; saldo dihitung dari mutasi | Jangan impor sebagai mutasi tambahan tanpa memastikan tidak menggandakan saldo. | NEEDS REVIEW |
| Relasi | No Pesanan # (teks) | Kemungkinan `relation_id` atau relasi PO/payable; tidak ada FK PO tegas pada `um_suppliers` | Workbook audit menyebut 13 PO teracu; relasi operasional PID di aplikasi dipakai via pembayaran/payable. Semantik langsung PID→PO UNKNOWN. | NEEDS REVIEW |
| Header wajib target, tanpa sumber | — | `company_id`, `contact_id`, `type_transaction_id`, `date_transaction`, `status`, `debet`, `credit` | Supplier lookup, jenis transaksi, status approval dan arah saldo perlu keputusan/source tambahan. | NEEDS REVIEW |
| Detail pembayaran | Tidak ada metode rinci yang cukup pada daftar kolom | `um_supplier_paids.type_paid`, `type_transaction_id`, `amount` NOT NULL; `reff_id` nullable | Jangan mengarang cash/bank/giro/payable maupun akun/referensi dari total ringkasan. | UNKNOWN |

Target kandidat: `um_suppliers`, `um_supplier_details`, `um_supplier_paids`. Source code `UmSupplierController`/abstraksi dan pembayaran supplier menunjukkan PID digunakan pada alur pembayaran; itu tidak membuktikan bentuk transaksi source.

## 5. Purchase Invoice (PI)

**Sumber:** `OLI_PI_Rincian Faktur Pembelian_2026-01-01_2026-10-26.xlsx`, sheet `Rincian Faktur Pembelian`.

| Bagian | Kolom sumber (tipe sel) | Kandidat target (tipe; wajib?) | Transformasi / NULL / bukti | Status |
|---|---|---|---|---|
| Header | Nomor (teks) | `invoice_vendors.code` varchar(191), nullable | Referensi source, bukan `id`; nomor invoice vendor eksternal vs kode internal perlu dibedakan. | NEEDS REVIEW |
| Header | Tanggal (date serial) | Kandidat `date_invoice` date NOT NULL | Semantik “Tanggal” perlu dikonfirmasi sebagai tanggal faktur. | ASSUMED |
| Header | Pemasok (teks) | Lookup `contacts.id` → `invoice_vendors.vendor_id` int NOT NULL | Match lewat identitas supplier tepercaya, nama tidak cukup. | NEEDS REVIEW |
| Detail | Kode # (teks) | Lookup `items.id` → `invoice_vendor_details.item_id` int NOT NULL | PI dapat memuat berbagai tipe biaya; kecocokan item dan `is_finance_vendor_bills` perlu review. | NEEDS REVIEW |
| Detail | Nama Barang (teks) | Kandidat `invoice_vendor_details.item_name` nullable | Label snapshot tidak boleh menggantikan FK. | ASSUMED |
| Detail | Kuantitas (angka) | Tidak ada kuantitas pada `invoice_vendor_details` schema yang diaudit | Jangan mengasumsikan kuantitas dapat disimpan di `total_origin` atau field lain. | UNKNOWN |
| Detail | @Harga (angka) | Tidak ada unit-price column yang teridentifikasi | Mapping/transformasi tidak diketahui. | UNKNOWN |
| Detail | Total Harga (angka) | Kandidat `invoice_vendor_details.total` double NOT NULL dan/atau `total_origin` | Makna total, diskon, PPN, dan unit tidak dibuktikan; rekonsiliasi perlu keputusan. | NEEDS REVIEW |
| Header/summary | Mata Uang (teks/kode) | Tidak ada field currency yang teridentifikasi di invoice target | Perlu keputusan/config currency. | NEEDS REVIEW |
| Header/summary | Sub Total, Total Biaya, Total (angka) | Kandidat `subtotal`, `total`, `ppn`, `total_discount`, `total_pph` di `invoice_vendors` | Jangan mengasumsikan definisi label atau menghitung ulang. Formula/pembulatan belum dikonfirmasi. | NEEDS REVIEW |
| Header wajib target, tanpa sumber | — | `company_id`, `date_receive`, `due_date`, `status`, `status_approve`, `ppn`, `ppn_is_faktur`, `total_discount`, `total_pph`, flag tipe invoice | Beberapa tanggal dan flag wajib tidak terlihat di laporan. Tentukan dari dokumen pendukung/approval, bukan default dugaan. | NEEDS REVIEW |
| Detail wajib target, tanpa sumber | — | `account_id`, `cash_categories_id`, `create_by`, `diskon`, `total`, `total_origin`, `ppn`, `item_id` | Akun/kategori/pembuat/PPN detail harus berasal dari referensi resmi. | NEEDS REVIEW |
| Relasi GRN | Tidak ada field GRN eksplisit pada kolom PI yang diaudit | `invoice_vendor_details.reff_no` varchar nullable → kode GRN melalui aplikasi; `payable_detail_id` nullable | Referensi GRN mungkin berada di histori. Reuse GRN belum dipastikan; jangan menghubungkan hanya karena item/vendor/tanggal cocok. | NEEDS REVIEW |
| Metadata | status approval/posting, journal/payable IDs | `status_approve`, `journal_id`, `payable_id` | Workbook tidak menyediakan lifecycle lengkap/target IDs. PI approval membuat payable/journal menurut code; status historis source UNKNOWN. | UNKNOWN |

Source code: `InvoiceVendorController`, `invoice_vendors`, `invoice_vendor_details`, `invoice_vendor_taxes`; approval membuat payable/jurnal pada tipe tertentu. Tidak ditemukan formula universal yang dapat dipakai untuk merekonstruksi total.

## 6. Pembayaran Supplier (SAP)

**Sumber:** `OLI_BAYAR_Rincian Pembayaran Pembelian_2026-01-01_2026-10-26.xlsx`, sheet `Rincian Pembayaran Pembelian`.

| Bagian | Kolom sumber (tipe sel) | Kandidat target (tipe; wajib?) | Transformasi / NULL / bukti | Status |
|---|---|---|---|---|
| Header | No Bukti # (teks) | Kandidat `debts.code` varchar(191), nullable | Konfirmasi nomor bukti vs kode pembayaran debt sebelum reuse. | ASSUMED |
| Header | Tgl Bayar (date serial) | `debts.date_request` date NOT NULL atau `debt_payments` tanggal/metadata yang tersedia | Semantik tanggal dan field aktual perlu dicek di model/controller/schema lengkap. | NEEDS REVIEW |
| Header | Pemasok (teks) | Lookup `contacts.id` untuk debt/payable | Resolusi supplier memakai identitas natural key yang disetujui. | NEEDS REVIEW |
| Header | Nama Bank (teks) | Lookup kandidat `accounts.id` / bank reference, `debt_payments.cash_account_id` | Label bank bukan account ID; cocokkan akun dan company. | NEEDS REVIEW |
| Detail/alokasi | No. Faktur (teks) | `debt_details.payable_id` + `payable_detail_id` melalui crosswalk invoice/payable | Nomor invoice bukan FK; alokasi per faktur perlu grain laporan dipastikan. | NEEDS REVIEW |
| Detail | Tgl Faktur (date serial) | Kandidat tanggal transaksi payable | Tidak dipetakan ulang tanpa jelas fungsi kolom; header PI lebih otoritatif setelah disetujui. | UNKNOWN |
| Detail | Total Faktur (angka) | Nilai payable saldo awal/credit details, bukan pembayaran | Hanya kontrol rekonsiliasi; hindari duplikasi hutang dari file pembayaran. | NEEDS REVIEW |
| Detail | Bayar (angka) | `debt_payments.total` double NOT NULL dan/atau `debt_details.debt` | Pembayaran per faktur vs total bukti bayar harus dipastikan. Partial payments didukung aplikasi, tetapi grain workbook belum dibuktikan. | NEEDS REVIEW |
| Detail | Diskon (angka) | Tidak ada pasangan langsung yang disetujui; kemungkinan penyesuaian payable/journal | Formula dan akun diskon tidak terkonfirmasi. | NEEDS REVIEW |
| Header/summary | Pembayaran (angka) | Kandidat total header `debts.total` / agregat pembayaran | Jangan jumlahkan/duplikasi jika field tersebut sudah total per bukti. Rekonsiliasi harus menetapkan grain. | UNKNOWN |
| Header wajib target, tanpa sumber | — | `debts.company_id`, `create_by`, `status`, `total`, `paid`, `overpayment`; `debt_payments.payment_type`, `valid`, `filename` | Nilai/status/metode/aktor/attachment diperlukan tetapi tidak tersedia secara memadai. | NEEDS REVIEW |
| Relasi | PI → payable detail, PID → pembayaran | `debt_details.payable_id`, `payable_detail_id`, `um_supplier_id`; `debt_payments.header_id` | Gunakan crosswalk faktur/payable dan PID yang tervalidasi. | NEEDS REVIEW |

Source code: `DebtPayableController`, model `Payable`; target `debts`, `debt_details`, `debt_payments`, `payable_details`. Struktur subledger tidak bisa direkonstruksi hanya dari agregat report.

## 7. Retur Pembelian

**Sumber:** `OLI_RETUR_Rincian Retur Pembelian_2026-01-01_2026-10-26.xlsx`, sheet `Rincian Retur Pembelian`. README menyatakan tidak ada transaksi pada periode; audit tidak mendeteksi nomor dokumen. Ini tidak membuktikan tidak ada histori di luar periode.

| Kolom sumber | Kandidat target | Aturan / NULL / bukti | Status |
|---|---|---|---|
| Nomor, Tanggal | `purchase_order_returns.code`, `date_transaction`, atau `returs.code`/`date_transaction` | Dua lifecycle retur target berbeda; nomor saja tidak membedakan. | NEEDS REVIEW |
| Pemasok | Lookup `contacts.id` → `returs.supplier_id`; PO return memperoleh supplier via PO | Nama tidak cukup; tabel/lifecycle belum dapat dipilih. | NEEDS REVIEW |
| Kode #, Nama Barang | Lookup item; kandidat detail `item_id` | Resolusi item wajib, nama hanya bantu. Target detail masing-masing mempunyai item FK. | NEEDS REVIEW |
| Kuantitas | `purchase_order_return_details.qty` atau `retur_details.qty_retur` | Tipe retur, sumber receipt/PO, stok, dan unit harus ditentukan. | NEEDS REVIEW |
| @Harga, Total Harga | Kemungkinan `purchase_order_return_details.price`; tidak ada pasangan pasti pada `retur_details` | Formula/efek payable tidak diketahui; jangan membuat jurnal atau credit note otomatis. | UNKNOWN |
| Wajib target tanpa sumber | Company, warehouse, actor, status, account/journal, `warehouse_receipt_detail_id`, rack | Tidak tersedia cukup bukti; tidak ada transaksi periode yang bisa dipakai sebagai contoh. | UNKNOWN |

Source code menunjukkan `purchase_order_returns` mengeluarkan stok; jalur `returs` mengurangi stok dan dapat membuat jurnal. Efek retur terhadap payable belum terbukti. Mapping ditahan sampai sumber transaksi/keputusan bisnis tersedia.

## 8. Histori Proses Pembelian

**Sumber:** `OLI_HISTORI_Histori Proses Pembelian_2026-01-01_2026-10-26.xlsx`, sheet `Histori Proses Pembelian`.

| Kolom sumber | Kandidat target / penggunaan | Aturan dan batas | Status |
|---|---|---|---|
| Permintaan Barang | `purchase_requests.code` sebagai cross-reference | Bukan otomatis kolom transaksi tambahan; resolusi PR dan detail masih diperlukan. | ASSUMED |
| Pesanan Pembelian | `purchase_orders.code` | Gunakan untuk kandidat relasi PO; unik dan lintas tahun harus divalidasi. | ASSUMED |
| Penerimaan Barang | `warehouse_receipts.code` | Candidate relasi, belum bukti unique/komplet. | ASSUMED |
| Uang Muka Pembelian | `um_suppliers.code` | Koneksi PID ke PO/payable perlu review; tidak menyimpulkan FK langsung. | NEEDS REVIEW |
| Faktur Pembelian | `invoice_vendors.code` atau nomor eksternal | Perlu membedakan nomor internal/eksternal dan mencocokkan histori pembayaran. | NEEDS REVIEW |
| Retur Pembelian | salah satu dari dua lifecycle return | Jenis target belum dapat ditetapkan. | UNKNOWN |
| Pembayaran Pembelian | `debts.code` atau referensi transaksi | Perlu identifikasi nomor transaksi dan grain pembayaran. | NEEDS REVIEW |

Workbook histori direkomendasikan sebagai **crosswalk/control evidence**, bukan tabel transaksi target yang sudah terbukti. Referensi tahun 2025 harus dipertahankan/di-resolve atau dibiarkan unresolved dengan persetujuan; jangan dibuang karena periode laporan 2026.

## 9. Jurnal

**Sumber:** `OLI_JURNAL_Keseluruhan Jurnal_2026-01-01_2026-10-26.xlsx`, sheet `Keseluruhan Jurnal`.

| Bagian | Kolom sumber (tipe sel) | Kandidat target | Transformasi / bukti | Status |
|---|---|---|---|---|
| Header | Tanggal (date serial) | `journals.date_transaction` date NOT NULL | Konversi serial tervalidasi; bukan `date_posting` tanpa bukti. | ASSUMED |
| Header | Tipe Transaksi (teks) | Lookup `type_transactions.slug`/id dan `journals.type_transaction_id` | Mapping domain slug/nama perlu tabel referensi dan persetujuan. | NEEDS REVIEW |
| Header | No. Trans # (teks) | Crosswalk ke PR/PO/GRN/PID/PI/SAP/retur; mungkin `journals.relation_id` | Tidak ada bukti bahwa seluruh tipe memakai relasi yang sama; nomor bukan FK. | NEEDS REVIEW |
| Header | Deskripsi (teks) | `journals.description` varchar(191) | Panjang target lebih sempit daripada deskripsi sumber yang belum diteliti; truncation dilarang tanpa keputusan. | NEEDS REVIEW |
| Detail | Kode Perkiraan (teks/kode) | Lookup `accounts.code` → `journal_details.account_id` | Cocokkan code dalam company/hierarchy dan pastikan akun aktif; jangan map berdasar nama saja. | NEEDS REVIEW |
| Detail | Nama Perkiraan (teks) | `accounts.name` hanya pembanding | Nama bukan kunci akun. | ASSUMED |
| Detail | Debit (angka) | `journal_details.debet` double NOT NULL | Parsing presisi/locale; tanda dan nilai negatif perlu kebijakan. | ASSUMED |
| Detail | Kredit (angka) | `journal_details.credit` double NOT NULL | Sama; jangan mengubah sisi debit/kredit. | ASSUMED |
| Header | Status approval/posting | `journals.status`, `date_posting`, `posting_by` | Workbook tidak menunjukkan status lifecycle. Tidak membuat jurnal seolah sudah posted. | UNKNOWN |
| Rekonsiliasi | Kelompok baris per transaksi | `journals` + `journal_details` | Batas header/detail dan keseimbangan per jurnal belum diketahui; validasi debit=kredit wajib sebelum persetujuan import. | NEEDS REVIEW |

Jurnal target dapat dibuat otomatis oleh proses transaksi dan juga manual (`JournalController`); **tidak** boleh membuat ulang jurnal historis dari modul sekaligus mengimpor workbook jurnal. Pilih satu strategi setelah duplicate/overlap review. Keseimbangan global belum dibuktikan oleh aplikasi.

## Aturan transformasi lintas modul

| Masalah | Aturan kandidat | Status |
|---|---|---|
| Excel serial date | Konversi hanya sel yang style/kolomnya terbukti tanggal; verifikasi epoch dan nilai kalender. Jangan infer dari angka saja. | ASSUMED |
| Angka, jumlah, harga | Parse numeric sesuai nilai sel dan format `#,##0.##;-#,##0.##`; simpan presisi penuh yang tersedia. Locale, skala kuantitas, pembulatan, dan unit harus disahkan. | NEEDS REVIEW |
| Mata uang | Jangan mengonversi FX atau menghilangkan kode mata uang; currency target tidak teridentifikasi. | NEEDS REVIEW |
| Subtotal, pajak, diskon, total | Pertahankan field source pada area rekonsiliasi; jangan hitung ulang atau tetapkan formula sampai pemilik proses menyetujui definisi dan urutannya. | NEEDS REVIEW |
| Nomor dokumen | Simpan sebagai source key/crosswalk; jangan ubah menjadi PK target, jangan generate nomor tanpa strategi sequence. Uji duplikasi dan nomor lintas tahun. | VERIFIED prinsip; konflik NEEDS REVIEW |
| Status | Tidak memetakan status source ke integer/slug target tanpa kamus status resmi dan aturan posting/approval. | UNKNOWN |
| Baris lanjutan/merge | Rekonstruksi hanya berdasarkan posisi/struktur workbook yang divalidasi; blank presentasional tidak otomatis NULL atau nilai inherited. | NEEDS REVIEW |
| Duplikat | Belum ada business key source terverifikasi. Deteksi, klasifikasi, dan putuskan secara manual; tidak menghapus/dedup otomatis. | UNKNOWN |
| NULL/empty | Bedakan sel kosong, merged blank, formula kosong, dan nilai kosong eksplisit; untuk target NOT NULL minta sumber/default bisnis terotorisasi. | UNKNOWN / NEEDS REVIEW |
| Header-detail | Pisahkan grain header dari item/alokasi detail; total laporan bukan detail tanpa bukti. | VERIFIED prinsip |
| Referensi 2025 | Pertahankan referensi dan cari dokumen induknya; unmatched harus ditandai unresolved, bukan dihapus. | VERIFIED adanya referensi; tindakan NEEDS REVIEW |

## Keputusan yang masih menahan finalisasi

Kolom wajib target yang tidak disediakan workbook (company, warehouse/rack, creator, approval/status, account/type transaction, quality/storage, invoice receive/due date, payment method/account, PID mutasi, dan detail allocation); resolusi master supplier/item/account; relasi per-detail dan nomor lintas tahun; grain workbook; konversi mata uang dan formula nominal; duplicate/blank policy; pemilihan dua jalur retur; dan strategi jurnal (import jurnal vs generate otomatis). Lihat [mapping-review-checklist.md](mapping-review-checklist.md) dan dokumen ID mapping untuk daftar persetujuan serta konflik target.
