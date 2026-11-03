# Profiling Data Workbook Sumber

**Tanggal pemeriksaan:** 3 November 2026  
**Metode:** read-only parsing XML di dalam 9 file XLSX; tidak ada workbook diubah. Nilai identifier/nama transaksi tidak dicantumkan dalam laporan.

## Rekonsiliasi inventaris

**VERIFIED:** folder aktual `docs-migrate/2026-01-01_sd_2026-10-26/Unduh 2026-10-27/` berisi **9 file `.xlsx`**, masing-masing satu sheet. `docs-migrate/audit/source-audit.md` dan `schema-comparison.md` menyebut 8; ini bertentangan dengan direktori dan inventaris di [source-workbook-analysis.md](../audit/source-workbook-analysis.md), yang mencantumkan sembilan. Untuk pemeriksaan ini, jumlah fisik **9** terverifikasi. Dokumen audit lama tidak diubah.

## Hitungan struktur workbook

“Baris XML” menghitung elemen `<row>`; “baris berisi” berarti minimal satu sel berisi nilai atau formula. “Baris detail kandidat” dihitung dari nilai pada kolom identitas detail (mis. `Kode #`, `No. Faktur`, atau `Kode Perkiraan`), setelah header literal dikeluarkan. Angka detail ini **bukan** jumlah record relasional final.

| Workbook / sheet | Baris XML / berisi / kosong | Merged ranges | Baris detail kandidat | Referensi dokumen kandidat (kemunculan / unik / pengulangan) |
|---|---:|---:|---:|---:|
| `OLI_PR_Rincian Permintaan Barang_2026-01-01_2026-10-26.xlsx` / Rincian Permintaan Barang | 10.701 / 9.227 / 1.474 | 9.965 | 1.121 baris dengan kode item | 737 / 736 / 1 |
| `OLI_PO_Rincian Pesanan Pembelian_2026-01-01_2026-10-26.xlsx` / Rincian Pesanan Pembelian | 11.832 / 10.054 / 1.778 | 26.518 | 1.078 baris dengan kode item | 589 / 588 / 1 |
| `OLI_GRN_Rincian Penerimaan Barang_2026-01-01_2026-10-26.xlsx` / Rincian Penerimaan Barang | 8.636 / 7.457 / 1.179 | 11.981 | 990 baris dengan kode item | 585 / 584 / 1 |
| `OLI_DP_Uang Muka Pembelian_2026-01-01_2026-10-26.xlsx` / Uang Muka Pembelian | 48 / 44 / 4 | 67 | 15 nomor PID; 13 nomor PO teracu | 15 PID unik + 13 PO unik |
| `OLI_PI_Rincian Faktur Pembelian_2026-01-01_2026-10-26.xlsx` / Rincian Faktur Pembelian | 11.389 / 9.768 / 1.621 | 25.754 | 1.060 baris dengan kode item | 598 / 597 / 1 |
| `OLI_BAYAR_Rincian Pembayaran Pembelian_2026-01-01_2026-10-26.xlsx` / Rincian Pembayaran Pembelian | 6.466 / 5.536 / 930 | 15.094 | 664 baris kandidat berisi referensi faktur | 287 nomor SAP unik; tidak ada pengulangan nomor SAP terdeteksi |
| `OLI_RETUR_Rincian Retur Pembelian_2026-01-01_2026-10-26.xlsx` / Rincian Retur Pembelian | 14 / 11 / 3 | 28 | 0 baris detail dengan kode item | 0 nomor retur terdeteksi |
| `OLI_HISTORI_Histori Proses Pembelian_2026-01-01_2026-10-26.xlsx` / Histori Proses Pembelian | 1.438 / 1.306 / 132 | 1.480 | bukan tabel detail transaksi | 3.761 kemunculan token / 3.105 identifier unik lintas tipe; banyak pengulangan referensi |
| `OLI_JURNAL_Keseluruhan Jurnal_2026-01-01_2026-10-26.xlsx` / Keseluruhan Jurnal | 20.559 / 17.653 / 2.906 | 50.022 | 5.645 baris kandidat kode akun | 1.427 kemunculan / 777 identifier unik lintas tipe; bukan jumlah jurnal |

**Status:** VERIFIED sebagai hitungan struktur XML dan token berformat nomor OLI yang ditemukan oleh pola `TYPE.OLI.<tahun>.<periode>.<nomor>`. Ini bukan record count database. Baris berisi meliputi judul, header berulang, metadata halaman, dan baris detail.

## Header, detail, total, dan sel kosong

- **VERIFIED:** laporan transaksi memakai header berulang dan sel merge. Frekuensi label header: PR 737 set; PO 709 header tabel; GRN 588; PI 683; pembayaran 406; retur 1; jurnal 782 label tanggal dan 2.699 label kolom akun/debit/kredit. Jumlah header/page/section tidak sama dengan jumlah dokumen unik.
- **VERIFIED:** label ringkasan pada PO muncul `Sub Total` 709 kali, `Total Biaya` 589 kali, `Total` 709 kali; PI masing-masing 683, 598, 683; workbook retur masing-masing satu. Ini hitungan label laporan, bukan bukti semua dokumen memiliki baris subtotal terpisah.
- **VERIFIED:** tidak ditemukan formula cell di sembilan workbook. Angka total adalah nilai tersimpan/statis, bukan formula Excel yang dapat dipakai untuk merekonstruksi formula bisnis.
- **VERIFIED:** pada 990 baris detail kandidat GRN, kolom `Satuan` kosong mentah pada 873 baris. Kekosongan itu tidak ditutup oleh vertical merge di kolom tersebut. Makna blank dan unit default **NEEDS REVIEW**; jangan isi unit berdasarkan tebakan.
- **VERIFIED:** pada kandidat baris detail PR/PO/GRN/PI yang diperiksa, kolom kode item, nama, dan kuantitas memiliki nilai tersimpan; PO/PI juga memiliki harga dan total pada baris kandidat. Hal ini tidak memverifikasi tipe/unit/semantik nilainya.
- **VERIFIED:** format tanggal tersimpan numerik dan ditampilkan `dd MMM yyyy`: PR 737 sel, PO 709, GRN 588, PI 683, PID 15, SAP 1.070, jurnal 782. Tidak ada formula; validasi tanggal serial tetap diperlukan saat konversi.
- **VERIFIED:** format numeric yang dominan pada nilai kuantitas/harga/nominal adalah `#,##0.##;-#,##0.##`; tidak ada kebijakan rounding target yang dibuktikan oleh format Excel.
- **UNKNOWN:** blank dalam area merge/continuation tidak otomatis NULL database. Merged ranges yang sangat banyak di tabel di atas membuat inherited context mungkin; hanya nilai kosong `Satuan` GRN yang dikuantifikasi terhadap baris kandidat. Perlu review visual/aturan report sebelum normalisasi.

## Kandidat key, pengulangan, dan duplikasi

| Kandidat natural key | Profil sumber | Status / interpretasi |
|---|---|---|
| PR | 736 nomor unik; 737 kemunculan token (1 pengulangan) | NEEDS REVIEW: pengulangan dapat berupa header halaman/section atau dokumen duplikat; belum dinyatakan duplikat transaksi. |
| PO | 588 unik; 589 kemunculan (1 pengulangan) | NEEDS REVIEW dengan batas interpretasi yang sama. |
| GRN/RI | 584 unik; 585 kemunculan (1 pengulangan) | NEEDS REVIEW. |
| PID | 15 PID unik; 13 referensi PO unik | VERIFIED sebagai identifier terdeteksi; key constraint source UNKNOWN. |
| PI | 597 unik; 598 kemunculan (1 pengulangan) | NEEDS REVIEW. |
| SAP | 287 nomor SAP unik tanpa kemunculan SAP berulang; juga terdeteksi 5 referensi non-SAP (2 SBK, 2 PO, 1 BTL) | VERIFIED sebagai token; makna/relasi non-SAP perlu review. |
| Retur | Tidak ada nomor retur dan tidak ada baris detail kandidat | VERIFIED terhadap workbook periode; README juga menyatakan tanpa transaksi. Tidak membuktikan periode lain kosong. |
| Jurnal | 88 kode akun unik; 777 candidate transaction-reference identifiers lintas prefix | ASSUMED sebagai natural key; jumlah identifier bukan jumlah header jurnal. |
| Kode item lintas PR/PO/GRN/PI/retur | 61 nilai unik ternormalisasi | VERIFIED sebagai nilai kode berulang pada kolom `Kode #`; unique item/business key belum dibuktikan. |
| Nama pemasok | 62 nilai unik ternormalisasi dari label `Pemasok` | VERIFIED sebagai label/nilai laporan; tidak tersedia kode supplier pada kolom yang diprofilkan. |
| Kode akun jurnal | 88 nilai unik ternormalisasi | VERIFIED sebagai nilai report; hubungan ke target akun belum final. |

Pengulangan satu nomor pada laporan PR/PO/GRN/PI perlu ditinjau terhadap posisi section/halaman. Pengulangan alami pada histori atau lintas workbook bukan bukti transaksi source duplikat.

## Referensi Histori dan lintas tahun

Identifier di sheet Histori dihitung setelah menerapkan nilai visual yang diwariskan hanya untuk vertical merged cells, sehingga satu referensi yang secara tampilan membentang beberapa baris tidak dianggap hilang pada baris berikutnya. Ini tetap bukti **co-occurrence report**, bukan FK.

| Tipe | Kemunculan histori | Unik di histori | Cocok ke workbook transaksi | Hanya di histori | 2025 unik di histori |
|---|---:|---:|---:|---:|---:|
| PR | 829 | 746 | 736 | 10 | 9 |
| PO | 812 | 716 | 586 | 130 | 10 |
| GRN/RI | 739 | 597 | 584 | 13 | 10 |
| PID | 29 | 15 | 15 | 0 | 0 |
| PI | 800 | 692 | 597 | 95 | 10 |
| SAP | 549 | 336 | 287 | 49 | 0 |

Semua **only-in-history** berstatus NEEDS REVIEW: sebagian mungkin dokumen periode sebelumnya, di luar scope report, atau unmatched/format lain. PO juga memiliki 2 nomor export yang tidak ditemukan di sheet Histori. Jangan menghapus atau mengabaikan referensi tersebut.

## Kandidat stable row locator

Nomor baris Excel sendiri **bukan business key** dan dapat berubah saat workbook diekspor ulang. Kandidat locator audit untuk file sumber yang immutable adalah kombinasi: `SHA-256 workbook + nama sheet + nomor baris XML + jenis kolom/grain + nomor dokumen terdeteksi + ordinal detail dalam dokumen`. `SHA-256 + sheet + row` dapat menunjuk lokasi fisik pada artefak yang sama; nomor dokumen/ordinal membantu review, tetapi belum disahkan sebagai key migrasi. Jika file berubah, hash berubah dan locator perlu direkonsiliasi. **NEEDS REVIEW** sebelum disetujui sebagai `source_line_locator` resmi.

## Bukti

Workbook asli di bawah `docs-migrate/2026-01-01_sd_2026-10-26/Unduh 2026-10-27/`; parsing `xl/workbook.xml`, `xl/worksheets/sheet1.xml`, `xl/sharedStrings.xml`, `xl/styles.xml`, `mergeCells`, dan sel angka/formula. Ringkasan workbook terkait: `docs-migrate/audit/source-audit.md`, `source-workbook-analysis.md`, `data-quality.md`. Tidak ada konten workbook yang ditulis ulang.
