# Perbandingan Schema Source dan Target

**Tanggal pembaruan:** 3 November 2026  
**Status:** VERIFIED untuk schema/isi target; UNKNOWN untuk schema sumber; perbandingan kolom belum dapat dilakukan.

## Ringkasan

| Ukuran | Temuan |
|---|---|
| Source | 8 workbook laporan `.xlsx`; jumlah tabel database UNKNOWN |
| Target | 359 tabel, 18 view; rincian schema pada [target-audit.md](target-audit.md) |
| Pasangan tabel terverifikasi | 0. Tidak tersedia definisi tabel source untuk dibandingkan |
| Tabel source tanpa pasangan | UNKNOWN; source table inventory belum tersedia |
| Tabel target tanpa sumber | UNKNOWN; tidak ada source schema untuk menguji cakupan |
| Kolom/tipedata/nullability/key yang berbeda | UNKNOWN; tidak dapat dibandingkan dari label laporan |

## Kandidat area yang perlu dibandingkan (belum mapping)

Nama dan proses berikut hanya petunjuk pencarian untuk review, bukan pasangan yang disetujui:

| Ekspor laporan | Area target yang perlu diperiksa | Status |
|---|---|---|
| Permintaan barang (PR) | `purchase_requests`, `purchase_request_details` | ASSUMED sebagai kandidat area; semantik dan granularitas belum dibuktikan setara |
| Pesanan pembelian (PO) | `purchase_orders`, `purchase_order_details` | ASSUMED sebagai kandidat area |
| Penerimaan barang (RI/GRN) | `warehouse_receipts`, `warehouse_receipt_details`, kemungkinan `receipts`/detail | ASSUMED; pemilihan pasangan UNKNOWN |
| Uang muka pembelian (PID) | Belum dapat ditetapkan dari nama tabel saja | UNKNOWN |
| Faktur pembelian (PI) | `invoice_vendors`/detail dan/atau `payables`/detail | ASSUMED sebagai area kandidat; lifecycle/accounting UNKNOWN |
| Pembayaran pembelian (SAP) | `payables`, `payable_details`, tabel transaksi kas terkait | ASSUMED sebagai area kandidat; relasi dan makna UNKNOWN |
| Retur pembelian | `purchase_order_returns`, detail | ASSUMED sebagai area kandidat; README menyebut tanpa transaksi periode |
| Histori pembelian | Tidak ditemukan bukti tabel pasangan langsung | UNKNOWN |
| Jurnal | `journals`, `journal_details` | ASSUMED sebagai area kandidat; akun, transaksi, posting, dan histori UNKNOWN |

Nama target di atas diverifikasi dari schema target dan migrasi aplikasi. Kesamaan istilah tidak membuktikan kesamaan makna, cakupan record, aturan status, atau relasi. Tidak ada mapping kolom yang ditetapkan dalam audit ini.

## Dampak dan kebutuhan bukti

Perbandingan struktur kolom, tipe/panjang, NULL/default, PK/FK, unique/index, auto increment, serta kolom wajib target belum bisa dinilai. Dapatkan schema source (SQL/metadata read-only) atau definisi struktur resmi untuk masing-masing ekspor dan dokumentasikan makna serta grain record. Setelah itu bandingkan dengan schema target yang terlampir, termasuk business rules/model aplikasi. Jangan mengubah schema target untuk menyamakan source.
