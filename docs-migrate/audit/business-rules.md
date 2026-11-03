# Audit Business Rules Solog OLI

**Tanggal audit:** 3 November 2026  
**Cakupan:** Telaah statis source code, migrations, model, dan schema live target. Tidak ada runtime transaksi yang dijalankan.

## Status dan batas bukti

- **VERIFIED** berarti implementasi langsung ditemukan pada source code/schema yang disebut.
- **ASSUMED** berarti indikasi struktur ada, tetapi aturan bisnis belum terbukti.
- **UNKNOWN** berarti bukti implementasi belum ditemukan atau tidak dapat dipastikan.
- **NEEDS REVIEW** berarti keputusan bisnis/akuntansi harus dikonfirmasi pemilik proses.

`composer.json` menunjukkan Laravel 5.6. Bootstrap aplikasi gagal pada PHP 8.2 karena kompatibilitas return type `ArrayAccess` (lihat `target-audit.md`); analisis alur di bawah bersumber dari pembacaan kode, bukan eksekusi aplikasi. Definisi PK, tipe/null/default, FK deklaratif, index, dan auto increment seluruh tabel ada di [target-audit.md](target-audit.md). Controller yang ditelaah umumnya memakai validasi inline Laravel; tidak ditemukan Form Request terpisah untuk alur utama yang dibahas. Tidak ada observer/listener transaksi yang teridentifikasi dalam file yang ditelaah.

## Struktur transaksi dan relasi

Semua tabel transaksi menggunakan `id` sebagai identitas target sesuai schema live; header/detail biasanya menghubungkan detail melalui `header_id`. Jangan menyamakan ID target dengan nomor dokumen source.

| Modul | Header dan detail / subledger | Relasi yang terlihat |
|---|---|---|
| PR | `purchase_requests` → `purchase_request_details` | Perusahaan, gudang, pembuat/pemberi persetujuan, item; detail PO dapat merujuk `purchase_request_detail_id` |
| PO | `purchase_orders` → `purchase_order_details` | Supplier/contact, gudang, perusahaan, kendaraan; detail dapat merujuk PR detail |
| GRN | `warehouse_receipts` → `warehouse_receipt_details` → `purchase_order_receipt_details` | Header memuat `purchase_order_id` opsional; penghubung detail penerimaan–detail PO menyimpan kuantitas; detail juga masuk ke stock/quality |
| PI | `invoice_vendors` → `invoice_vendor_details` → `invoice_vendor_taxes` | Vendor/company; detail memuat referensi teks `reff_no`, akun/kategori, biaya/maintenance/GR, pajak; approval menghubungkan payable/journal |
| Deposit supplier / PID | `um_suppliers` → `um_supplier_details`, `um_supplier_paids` | Vendor/company, journal, opsional payable; pembayaran rinci dapat menunjuk akun kas/bank, giro, atau payable |
| Hutang / Payable | `payables` → `payable_details` | Contact/company, type transaction, journal; `relation_id` digunakan sebagai relasi transaksi yang bersifat polymorphic pada beberapa alur |
| Pembayaran supplier | `debts` → `debt_details`/`debt_payments` dan mutasi `payable_details` | Pembayaran dapat membuat journal, `cash_transactions`, detail kas, serta memakai deposit supplier/giro |
| Retur | `purchase_order_returns` → `purchase_order_return_details`; juga `returs` → `retur_details` | Dua alur implementasi berbeda; satu merujuk PO dan stock transaction, satu merujuk receipt detail/stock serta jurnal kondisional |
| Journal | `journals` → `journal_details` | Company, transaction type, creator/approver/poster, akun; banyak modul dapat membuat journal |

Relasi pada kode aplikasi dapat berupa `join` atau `relation_id` tanpa FK database deklaratif. Contoh: kode GRN mencari PO melalui `warehouse_receipts.purchase_order_id`; relasi bisnis tersebut tidak boleh dianggap tervalidasi FK bila tidak tercantum pada metadata FK di target audit.

## Aturan per modul

### 1. Purchase Request (PR)

- **Penyimpanan/validasi — VERIFIED:** `PurchaseRequestController::store` memerlukan gudang, tanggal permintaan, dan tanggal kebutuhan; setiap detail memerlukan item dan kuantitas. Company diambil dari gudang. Bila PR berasal dari Customer Order, controller memeriksa available quantity dan menguranginya.
- **Approval — VERIFIED:** `approve` menerima detail dengan ID dan kuantitas numerik positif, menolak kuantitas disetujui yang melebihi permintaan, mencatat approver/tanggal, lalu mengubah status.
- **Status — VERIFIED:** `PurchaseRequest` mendefinisikan 0 ditolak, 1 menunggu persetujuan, 2 disetujui, 3 sudah menjadi PO, 4 menunggu CO, 5 PO sebagian. `updateStatus` membandingkan jumlah PO dengan jumlah approved.
- **Ke PO — VERIFIED:** `create_po` mengambil detail PR berdasarkan ID, harga/PPN, lalu membuat PO dan menghubungkan detail PO ke `purchase_request_detail_id`.
- **Nomor — VERIFIED:** kode dibuat melalui `TransactionCode` dengan tipe transaksi `purchaseRequest`.
- **Kolom/relasi yang belum pasti:** validasi lengkap input saat store dan aturan approval di semua endpoint/API belum dibandingkan; status source belum memiliki pasangan yang disetujui (**UNKNOWN**).

### 2. Purchase Order (PO)

- **Penyimpanan/validasi — VERIFIED:** `PurchaseOrderController::store` mewajibkan company, gudang, supplier, tanggal PO, payment type (`0/1/2`), dan minimal satu detail item dengan kuantitas positif serta harga tidak negatif. Kendaraan dan flag/nominal PPN opsional menurut validator tersebut.
- **PO tanpa PR — VERIFIED untuk endpoint langsung:** `purchase_request_id` tidak diwajibkan oleh validator PO langsung; `PurchaseOrder::fetch` dan `insert` pada jalur ini tidak mengisi header `purchase_request_id` (baris pengisian bahkan dikomentari). PO detail dapat terhubung ke PR detail. Dengan demikian aplikasi menyediakan jalur PO langsung tanpa PR.
- **Approval — VERIFIED:** terdapat tahap `approve_pimpinan` (slug `approved2`) dan `approve` (slug `approved`); approval akhir memeriksa status batal/parsial dan limit hutang supplier. Slug status lain yang dibaca kode meliputi requested, cancelled, partially-cancelled, finished, outstanding.
- **Kuantitas/nilai — VERIFIED:** `PurchaseOrderDetail::getPriceTotal` menghitung `qty × price`; PPN disimpan terpisah pada detail. Nilai total ini belum membuktikan perlakuan pajak/biaya final.
- **Nomor — VERIFIED:** `TransactionCode` memakai konfigurasi company/type transaksi dan counter.
- **Jurnal — VERIFIED sebagian:** ada helper jurnal pembelian yang membulatkan total detail dengan `round()`, tetapi pada approval PO terdapat komentar bahwa jurnal pembelian disembunyikan. Kapan helper tersebut dipanggil untuk seluruh jenis PO **UNKNOWN**.
- **Pembayaran — VERIFIED sebagian:** source membedakan `payment_type`; GRN memakai payment type untuk proses kas/accrual. Makna kode payment type perlu review business owner (**NEEDS REVIEW**).

### 3. Warehouse Receipt / GRN

- **Penyimpanan — VERIFIED:** `ReceiptController::store` memerlukan company, gudang, tanggal dan waktu penerimaan; PO tidak diwajibkan. Header dapat dibuat dengan `purchase_order_id` kosong. Status draft dapat memakai kode sementara; jalur yang ditandai terlihat memakai `TransactionCode`.
- **Relasi — VERIFIED:** header memiliki satu field `purchase_order_id`; detail penerimaan dipasangkan ke detail PO melalui `purchase_order_receipt_details`. Satu receipt header karenanya merujuk paling banyak satu PO pada jalur ini. Tidak ditemukan unique constraint yang membatasi satu PO ke satu receipt; kode menyimpan kumulatif `receive`, sehingga satu PO dapat direalisasikan melalui beberapa receipt.
- **Partial receipt — VERIFIED sebagai model data, batas maksimum NEEDS REVIEW:** jumlah per receipt direkam dan ditambahkan ke kuantitas received PO saat approval. Validator `validasiLimitPO` menghitung total order vs receipt, tetapi pemanggilan pada jalur detail yang ditelaah tampak dikomentari; belum terbukti semua endpoint mencegah penerimaan melebihi PO.
- **Approval/stock — VERIFIED:** approval menolak receipt tanpa detail atau lampiran, menjalankan pemeriksaan kapasitas/pallet, mengubah status, memperbarui dimensi item dan kuantitas terima PO. Kode stok menjalankan efek persediaan.
- **Kas/jurnal/hutang — VERIFIED bersyarat:** untuk PO payment type accrual, finance aktif dapat membuat jurnal receipt dan payable accrual; payment type cash membuat cash transaction. Cost item memiliki jalur journal khusus. Perlakuan bergantung setting, PPN, akun, dan jenis item.
- **Nomor — VERIFIED:** `TransactionCode` bertipe `warehouseReceipt` pada jalur receipt bernomor.

### 4. Invoice Vendor (PI)

- **Header/detail — VERIFIED:** `InvoiceVendorController::store` mewajibkan company, tanggal invoice/terima/jatuh tempo, vendor, dan detail. Untuk finance vendor bills, akun dan kategori kas wajib per detail. Header menyimpan subtotal, total, PPN, PPh, diskon dan flag invoice; rincian menyimpan nilai/PPN/referensi dan tax detail.
- **Sumber tagihan — VERIFIED:** flag Good Receipt membuat kode mencari `warehouse_receipts` berdasarkan `reff_no` yang diinput sebagai kode receipt. Bila beberapa receipt dirangkum, tipe perlakuan PPN-nya harus sama. Detail dapat merujuk cost job/manifest, maintenance, finance bill, atau receipt. Direct FK PI→PO tidak terbukti.
- **Perhitungan — UNKNOWN/NEEDS REVIEW:** store menerima total/subtotal/diskon/PPN dari request dan menyimpannya; formula subtotal, pembulatan, dan rekonsiliasi terhadap semua detail tidak dihitung ulang secara konsisten pada potongan alur ini.
- **Approval/posting — VERIFIED:** approval membuat journal untuk sebagian jenis invoice, membuat `payables` dan `payable_details`, menghubungkan detail invoice ke payable detail, lalu mengubah `status_approve`. Maintenance memakai helper journal lain. Akun biaya/hutang diambil dari vendor/default account dan jenis biaya.
- **PPN — VERIFIED sebagian:** bila PPN faktur dipisah, jurnal membukukan PPN ke akun `ppn_in`; bila tidak, nilai total+PPN masuk ke akun biaya/aset yang dipilih. Perlakuan bisnis per jenis invoice perlu review.
- **Status pembayaran:** controller pembayaran dapat mengubah status invoice ketika payable lunas. Kode status penuh perlu validasi terhadap semua endpoint (**NEEDS REVIEW**).
- **Nomor — VERIFIED:** memakai sequence berbeda untuk maintenance, Good Receipt, finance bills, dan operational invoice.

### 5. Uang muka / PID (deposit supplier)

- **Penyimpanan — VERIFIED:** `UmSupplierController::store` memerlukan company, tanggal transaksi, nominal integer, dan contact/vendor. `Abstracts/Sales/UmSupplier::store` membuat header draft status 1, satu mutasi detail, dan detail cara bayar.
- **Cara bayar — VERIFIED:** `um_supplier_paids.type_paid` membedakan kas/bank (1), cek/giro (2), dan payable (3) pada kode/model yang ditelaah. Approval menandai giro digunakan atau mencatat cash transaction.
- **Approval — VERIFIED:** status 1 berubah ke 2, membuat journal, menjumlahkan debit/kredit detail ke header journal dan menyimpan `journal_id`. Bila deposit diterapkan ke payable, payable bertambah debit dan memperoleh mutasi payable detail.
- **Penggunaan saldo — VERIFIED:** alur pembayaran hutang membaca deposit supplier dan membuat mutasi credit saat deposit digunakan. `returnSisa` juga mencatat pengembalian saldo dan journal.
- **Batas:** hubungan langsung PID ke PI tidak ditetapkan sebagai FK; aplikasi menghubungkan deposit ke payable/vendor pada proses pembayaran. Aturan urutan pemakaian dan rekonsiliasi deposit lintas invoice **UNKNOWN**.

### 6. Payable dan 7. Pembayaran Supplier (SAP)

- **Payable — VERIFIED:** invoice vendor approval menghasilkan header `payables` dan detail kredit. `Model/Payable` menghitung total hutang sebagai jumlah credit detail, total bayar sebagai jumlah debit detail, dan sisa sebagai `max(hutang − bayar, 0)`.
- **Pembayaran — VERIFIED:** `DebtPayableController::store_payment` merekam payment per invoice/detail, menambah debit payable detail (pembayaran parsial dimungkinkan), membuat journal, serta menyimpan `debt_payments`. Kas/bank membentuk `cash_transactions` dan detailnya; giro diperbarui sebagai terpakai; bukti potong memiliki detail dan jurnal tersendiri.
- **Uang muka — VERIFIED:** pembayaran dapat memilih `um_supplier_id`; sistem menambah credit/mutasi pada deposit dan tidak menghitung nilainya sebagai pembayaran hutang biasa pada salah satu agregasi controller.
- **Status/nomor — VERIFIED sebagian:** pembayaran memberi status pada debt dan menghasilkan kode melalui `TransactionCode` tipe debt payable payment; status invoice/payable bergantung apakah saldo menjadi nol.
- **Pajak/diskon/pembulatan — UNKNOWN/NEEDS REVIEW:** controller mengelola bukti potong, sisa kurang/lebih bayar dan nilai yang dikirim. Konsistensi formula input client, pembulatan, dan rekonsiliasi lintas detail perlu review; tidak digeneralisasi dari satu controller.

### 8. Retur

- **Dua jalur — VERIFIED:** aplikasi memiliki `purchase_order_returns`/detail dan `returs`/detail. Keduanya tidak boleh dianggap satu tabel atau satu lifecycle.
- **Purchase Order Return — VERIFIED:** controller meminta PO, gudang, tanggal; detail menyimpan kuantitas retur. Approval mengubah status menjadi 2 dan membuat `stock_transactions` keluar per detail.
- **Retur inventory umum — VERIFIED:** `Abstracts/Inventory/Retur` membuat draft status 1 dan tipe item; approval mengubah status 2, mengurangi stock, memperbarui kuantitas/return qty pada receipt detail dan dapat membuat journal bila finance setting aktif.
- **Dampak hutang — UNKNOWN:** jalur PO return yang ditelaah tidak menunjukkan pembaruan payable langsung. Dampak kredit/hutang dan mapping ke laporan retur lama memerlukan review.

### 9. Journal

- **Pembuatan — VERIFIED:** jurnal dibuat manual melalui `Finance/JournalController` dan otomatis oleh modul receipt, invoice vendor, deposit, retur tertentu, dan pembayaran.
- **Status — VERIFIED:** abstraksi mendukung approve (status 2), posting (status 3), unposting, dan pengecekan periode closing. Detail memiliki akun/debit/kredit dan relasi header.
- **Keseimbangan — UNKNOWN/NEEDS REVIEW:** penyimpanan manual mengisi total header dari jumlah debit/kredit yang dikirim, dan approval/posting yang ditelaah memvalidasi status/periode. Tidak ditemukan pemeriksaan global bahwa total debit harus sama dengan total kredit di semua jalur. Tidak dapat menyatakan database selalu menjamin jurnal seimbang.
- **Pembulatan — VERIFIED terbatas:** helper tertentu menggunakan `round()`; deposit menjumlahkan nilai journal detail. Tidak ditemukan satu kebijakan rounding global lintas modul.

## Penomoran transaksi

`app/Utils/TransactionCode.php` menyusun kode berdasarkan `company_numberings`, `type_transaction_id`, urutan, prefix, dan komponen roman/date/counter/code. Counter biasa menaikkan `last_value`; Job Order khusus mengambil maksimum sequence bulan berjalan dari `job_orders`. Impor yang mempertahankan nomor historis perlu menghindari pemanggilan generator yang mengubah counter dan perlu merekonsiliasi sequence sesudah review (**NEEDS REVIEW**). Snapshot target berisi 441 baris `company_numberings`.

## Bukti yang belum tersedia

- Business rule source aplikasi lama, grain record source, dan pemetaan status source.
- Formula resmi pajak/diskon/rounding dan dokumentasi makna payment type.
- Semua jalur API/legacy dan kondisi runtime yang dapat mengubah approval/posting.
- Jaminan keseimbangan jurnal global serta dampak hutang untuk retur.
- Konfirmasi apakah data fixture Golden pada target harus dipisah/diabaikan dalam migrasi.
