# Analisis Workbook Sumber

**Tanggal audit:** 3 November 2026  
**Status bukti:** VERIFIED / UNKNOWN / NEEDS REVIEW

## Inventaris

| Workbook di `docs-migrate/` | Sheet | Isi/kolom yang terlihat | Referensi teramati |
|---|---|---|---:|
| `OLI_PR_Rincian Permintaan Barang_2026-01-01_2026-10-26.xlsx` | Rincian Permintaan Barang | Nomor, Tanggal, Kode #, Nama Barang, Kuantitas | 736 nomor PR |
| `OLI_PO_Rincian Pesanan Pembelian_2026-01-01_2026-10-26.xlsx` | Rincian Pesanan Pembelian | Nomor, Tanggal, Pemasok, Kode #, Nama Barang, Kuantitas, @Harga, Total Harga, Mata Uang, Sub Total, Total Biaya, Total | 588 nomor PO |
| `OLI_GRN_Rincian Penerimaan Barang_2026-01-01_2026-10-26.xlsx` | Rincian Penerimaan Barang | Nomor, Tanggal, Pemasok, Kode #, Nama Barang, Kuantitas, Satuan | 584 nomor penerimaan |
| `OLI_DP_Uang Muka Pembelian_2026-01-01_2026-10-26.xlsx` | Uang Muka Pembelian | Nomor, Tanggal, Total, Terpakai/Retur (per Tgl), Sisa Uang Muka (per Tgl), No Pesanan # | 15 nomor PID; 13 nomor PO teracu |
| `OLI_PI_Rincian Faktur Pembelian_2026-01-01_2026-10-26.xlsx` | Rincian Faktur Pembelian | Nomor, Tanggal, Pemasok, Kode #, Nama Barang, Kuantitas, @Harga, Total Harga, Mata Uang, Sub Total, Total Biaya, Total | 597 nomor PI |
| `OLI_BAYAR_Rincian Pembayaran Pembelian_2026-01-01_2026-10-26.xlsx` | Rincian Pembayaran Pembelian | Pemasok, No Bukti #, Tgl Bayar, Nama Bank, Metode Bayar, No. Faktur, Tgl Faktur, Total Faktur, Bayar, Diskon, Pembayaran | 287 nomor pembayaran |
| `OLI_RETUR_Rincian Retur Pembelian_2026-01-01_2026-10-26.xlsx` | Rincian Retur Pembelian | Nomor, Tanggal, Pemasok, Kode #, Nama Barang, Kuantitas, @Harga, Total Harga | Nomor dokumen tidak terdeteksi; README sumber menyebut tidak ada transaksi dalam periode |
| `OLI_HISTORI_Histori Proses Pembelian_2026-01-01_2026-10-26.xlsx` | Histori Proses Pembelian | Permintaan Barang, Pesanan Pembelian, Penerimaan Barang, Uang Muka Pembelian, Faktur Pembelian, Retur Pembelian, Pembayaran Pembelian | Referensi lintas proses; beberapa bertanggal/periode 2025 |
| `OLI_JURNAL_Keseluruhan Jurnal_2026-01-01_2026-10-26.xlsx` | Keseluruhan Jurnal | Tanggal, Tipe Transaksi, No. Trans #, Deskripsi, Kode Perkiraan, Nama Perkiraan, Debit, Kredit | Nomor transaksi dan akun sebagai calon penghubung |

Nama workbook menunjukkan periode laporan 2026-01-01 sampai 2026-10-26. Semua workbook yang diinventarisasi berformat XLSX dan memiliki satu sheet. Nama file, sheet, serta kolom di atas diturunkan dari inventaris dan audit sumber sebelumnya (`source-audit.md`); bukan hasil pemetaan final.

## Format dan bentuk data

- **VERIFIED:** tanggal tersimpan sebagai serial tanggal Excel dan ditampilkan dengan format `dd MMM yyyy` pada sel bertipe tanggal. Contoh serial yang terlihat pada inspeksi XML: 46028, 46030, 46031.
- **VERIFIED:** kuantitas/nilai memakai format angka `#,##0.##;-#,##0.##`; nomor dokumen tersimpan sebagai teks pada contoh yang diperiksa.
- **VERIFIED:** workbook laporan berorientasi header/detail; beberapa baris menggunakan penggabungan/kelanjutan label atau sel kosong untuk meneruskan konteks. Karena itu hitungan baris Excel tidak serta-merta sama dengan hitungan dokumen atau detail transaksi.
- **UNKNOWN:** aturan lengkap untuk baris total, subtotal, pengulangan header, sel formula, baris lanjutan, duplikasi, dan sel kosong di seluruh workbook belum disertifikasi sebagai data rekaman. Laporan terdahulu memberi inventaris, bukan normalisasi baris final.
- **UNKNOWN:** kelengkapan histori sebelum periode laporan tidak dapat disimpulkan dari workbook periode terbatas. File histori proses menunjukkan sejumlah referensi 2025 yang dapat terkait dengan dokumen di periode laporan.

## Calon penghubung antardokumen

Nomor PR/PO/GRN/PI, `No Pesanan #` pada PID, `No. Faktur` pada pembayaran, serta `No. Trans #` dan `Tipe Transaksi` pada jurnal merupakan calon penghubung. Kode barang, nama barang, pemasok, tanggal, dan jumlah juga dapat membantu penelaahan. Kesamaan label atau nilai saja tidak membuktikan identitas yang sama; uniqueness, aturan pembentukan nomor, dan kecocokan seluruh baris tetap perlu diverifikasi sebelum mapping.

## Informasi aplikasi target yang tidak tampak pada laporan

Kolom yang diinventarisasi tidak menunjukkan ID internal target atau ID relasi foreign key, pembuat/pemeriksa/pemberi persetujuan, status workflow lengkap, gudang/lokasi rak, akun internal target, identitas pajak yang diperlukan per baris, seluruh dimensi stok, maupun seluruh detail alokasi pembayaran/PID. Informasi tersebut **tidak terlihat pada field laporan yang diaudit**; kemungkinan tidak tersedia pada data lama secara keseluruhan berstatus UNKNOWN sampai sumber tambahan ditemukan.

Akibatnya, rekonstruksi dapat membutuhkan lookup ke master target dan keputusan bisnis yang disetujui. Jangan mengisi field wajib dengan tebakan atau menjadikan nama/nomor laporan sebagai primary key target.

## Batas tahap ini

Tidak ada workbook sumber yang diubah. Dokumen ini tidak menetapkan pemetaan kolom final, transformasi final, atau kelayakan impor per dokumen. Rujuk [source-audit.md](source-audit.md) untuk inventaris dan rincian audit sumber tahap sebelumnya.
