# Analisis Relasi Antar Sumber dan Target

**Tanggal audit:** 3 November 2026  
**Status:** VERIFIED untuk FK deklaratif target dan referensi proses yang terlihat; relasi source UNKNOWN.

## Source

Ekspor histori menampilkan tahap Permintaan Barang → Pesanan Pembelian → Penerimaan Barang → Uang Muka Pembelian → Faktur Pembelian → Retur Pembelian → Pembayaran Pembelian. Ekspor transaksi memuat nomor dokumen lintas proses; README menyatakan histori/pembayaran/jurnal mungkin merujuk dokumen tahun sebelumnya, dan pada workbook histori ditemukan nomor dokumen tahun 2025. Ini menunjukkan referensi alur kerja, tetapi bukan bukti foreign key atau kelengkapan seluruh rantai transaksi.

Source tidak menyertakan schema SQL/metadata relasional. Candidate PK/FK, kardinalitas, orphan, dan relasi yang wajib/opsional berstatus UNKNOWN.

## Target

Database `db_solog_oli_initial` diverifikasi aktif. Metadata target memiliki 840 referensi kolom FK deklaratif (rincian constraint tersedia di [target-audit.md](target-audit.md)). Target mencakup tabel pembelian, penerimaan, invoice vendor, payable, dan jurnal beserta tabel detail. Constraint FK adalah bukti relasi struktural target; relasi yang dijaga hanya oleh kode aplikasi belum tentu muncul sebagai FK.

Model `App\Model\PurchaseOrder` mendefinisikan relasi ke company, supplier/contact, warehouse, dan detail. Model `App\Model\Journal` mendefinisikan company, transaction type, dan details. Ini bukti relasi ORM pada kode saat ini; tidak menyatakan relasi source sepadan. `app/Abstracts/Inventory/PurchaseRequest.php` juga memuat status workflow (0–5), sehingga status PR membutuhkan validasi business rules sebelum pemindahan.

## Risiko dan tindak lanjut

- Jangan menyimpulkan relasi hanya dari nomor yang tampak serupa atau nama kolom.
- Pastikan dokumen tahun sebelumnya yang dirujuk ikut tersedia atau strategi preservasi referensinya disetujui.
- Telusuri pasangan parent/detail dan aturan status melalui schema, model, dan business rules sebelum menyusun mapping.
- Setelah definisi source tersedia, validasi orphan dan jumlah referensi lintas dokumen secara read-only.
