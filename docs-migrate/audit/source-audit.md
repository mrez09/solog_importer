# Audit Database Source

**Tanggal audit:** 3 November 2026  
**Status umum:** VERIFIED untuk inventaris berkas dan isi yang terbaca; UNKNOWN untuk schema database relasional sumber.

## Cakupan dan metode

Membaca `docs-migrate/README.md` dan seluruh berkas di `docs-migrate/`. Ditemukan delapan workbook Excel (`.xlsx`), masing-masing dengan satu worksheet. Workbook dibaca secara read-only dari kontainer XML; tidak ada berkas sumber yang diubah. Tidak ditemukan berkas CSV, SQL, dump database, atau format database lain.

Berkas berada pada folder `2026-01-01_sd_2026-10-26/Unduh 2026-10-27/`. README menyebut perusahaan PT Ono Logistik Indonesia dan periode 1 Januari–26 Oktober 2026. Worksheet adalah ekspor laporan bertingkat dengan metadata dokumen, rincian, baris lanjutan, dan sel kosong/penggabungan. Ekspor tersebut bukan bukti schema database atau tabel sumber.

## Inventaris sumber

| Berkas / worksheet | Kolom berlabel yang teramati | Referensi dokumen unik dalam laporan* |
|---|---|---:|
| `OLI_PR_Rincian Permintaan Barang…xlsx` / Rincian Permintaan Barang | Nomor, Tanggal, Kode #, Nama Barang, Kuantitas | 736 PR |
| `OLI_PO_Rincian Pesanan Pembelian…xlsx` / Rincian Pesanan Pembelian | Nomor, Tanggal, Pemasok, Kode #, Nama Barang, Kuantitas, @Harga, Total Harga, Mata Uang, Sub Total, Total Biaya, Total | 588 PO |
| `OLI_GRN_Rincian Penerimaan Barang…xlsx` / Rincian Penerimaan Barang | Nomor, Tanggal, Pemasok, Kode #, Nama Barang, Kuantitas, Satuan | 584 RI |
| `OLI_DP_Uang Muka Pembelian…xlsx` / Uang Muka Pembelian | Nomor, Tanggal, Total, Terpakai/Retur (per Tgl), Sisa Uang Muka (per Tgl), No Pesanan # | 15 PID; 13 PO yang direferensikan |
| `OLI_PI_Rincian Faktur Pembelian…xlsx` / Rincian Faktur Pembelian | Nomor, Tanggal, Pemasok, Kode #, Nama Barang, Kuantitas, @Harga, Total Harga, Mata Uang, Sub Total, Total Biaya, Total | 597 PI |
| `OLI_BAYAR_Rincian Pembayaran Pembelian…xlsx` / Rincian Pembayaran Pembelian | Pemasok, No Bukti #, Tgl Bayar, Nama Bank, Metode Bayar, No. Faktur, Tgl Faktur, Total Faktur, Bayar, Diskon, Pembayaran | 287 SAP; referensi lain juga ada |
| `OLI_RETUR_Rincian Retur Pembelian…xlsx` / Rincian Retur Pembelian | Nomor, Tanggal, Pemasok, Kode #, Nama Barang, Kuantitas, @Harga, Total Harga | 0 referensi nomor terdeteksi; README menyatakan tidak ada transaksi pada periode |
| `OLI_HISTORI_Histori Proses Pembelian…xlsx` / Histori Proses Pembelian | Permintaan Barang, Pesanan Pembelian, Penerimaan Barang, Uang Muka Pembelian, Faktur Pembelian, Retur Pembelian, Pembayaran Pembelian | Referensi lintas dokumen; bukan hitungan record |
| `OLI_JURNAL_Keseluruhan Jurnal…xlsx` / Keseluruhan Jurnal | Tanggal, Tipe Transaksi, No. Trans #, Deskripsi, Kode Perkiraan, Nama Perkiraan, Debit, Kredit | Referensi transaksi jurnal; bukan hitungan record |

\*Hitungan referensi didapat dari nomor dokumen unik yang cocok dengan pola nomor OLI pada workbook. Untuk file pembayaran, uang muka, histori, dan jurnal workbook berisi referensi beberapa jenis dokumen; angka tersebut bukan jumlah baris atau jumlah seluruh record sumber. Nilai harus divalidasi terhadap pemilik data sebelum dijadikan kontrol migrasi.

## Struktur, record, dan kualitas yang dapat diverifikasi

- **Jumlah tabel sumber:** UNKNOWN. Berkas yang tersedia adalah laporan Excel, bukan definisi tabel/database.
- **Jumlah kolom database dan tipe data:** UNKNOWN. Label kolom laporan bukan nama kolom database; Excel tidak menetapkan tipe database. Sel numerik, teks, dan tanggal yang tersimpan sebagai serial adalah representasi workbook saja.
- **Jumlah record sumber:** UNKNOWN. Baris berisi header/metadata, rincian berulang, pemisah, dan kelanjutan dokumen; satu baris workbook tidak sama dengan satu record relasional.
- **Primary key / foreign key / constraint / index:** UNKNOWN. Tidak ada bukti schema SQL atau dokumentasi constraint.
- **Relasi bisnis yang tampak pada laporan:** worksheet histori menyajikan tahapan PR, PO, penerimaan, uang muka, faktur, retur, pembayaran; ini bukti jejak referensi dokumen, bukan FK database yang terverifikasi.
- **Periode di luar rentang laporan:** README memperingatkan histori, pembayaran, dan jurnal dapat mereferensikan dokumen tahun sebelumnya. Workbook histori memang menampilkan referensi tahun 2025. Jangan membatasi migrasi hanya pada dokumen tahun 2026 tanpa menelusuri referensi historis tersebut.
- **Duplikat / NULL / inkonsistensi:** UNKNOWN sebagai kualitas data. Sel kosong dapat berasal dari penggabungan/format laporan dan tidak dapat diklasifikasikan sebagai NULL. Baris rincian berulang bukan bukti duplikat tanpa identitas record dan aturan bisnis.

## Kesimpulan

Sumber yang dapat diaudit saat ini adalah delapan ekspor laporan untuk pembelian dan jurnal. Inventaris dan label yang terlihat VERIFIED; schema relasional, tipe kolom database, record count, candidate key, serta kualitas data masih UNKNOWN. Diperlukan schema/dump read-only atau dokumentasi sistem lama dan definisi record dari pemilik proses sebelum menyimpulkan mapping atau jumlah migrasi.
