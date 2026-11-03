# Analisis Kebutuhan Transformasi

**Tanggal audit:** 3 November 2026  
**Status:** VERIFIED untuk representasi yang terlihat pada laporan; transformasi final UNKNOWN.

Dokumen ini mengidentifikasi hal yang perlu diperiksa. Ini bukan Migration Data Dictionary, bukan mapping final, dan tidak mengubah data sumber.

| Indikasi konkret | Potensi kebutuhan | Status / bukti yang diperlukan |
|---|---|---|
| Nilai tanggal laporan muncul sebagai serial Excel (mis. `46031`) | Konversi tanggal dari serial workbook hanya bila benar-benar field tanggal; tentukan kalender, zona waktu, dan format target | ASSUMED; cek style sel, definisi source, contoh transaksi, dan tipe kolom target |
| Histori menampilkan referensi dokumen tahun 2025 meski periode laporan 2026 | Mempertahankan referensi historis atau menyertakan dokumen induk yang dirujuk | VERIFIED adanya referensi; cakupan dan strategi UNKNOWN |
| Worksheet memiliki sel kosong, baris lanjutan, dan metadata berulang | Rekonstruksi header/grup dokumen dan penanganan blank presentasional sebelum parsing | VERIFIED sebagai format workbook; aturan rekonstruksi UNKNOWN |
| PO/PI menampilkan subtotal/biaya/total; jurnal menampilkan debit/kredit | Rekonsiliasi nilai dan pembulatan pada level dokumen/detail; jangan menghitung ulang sebelum aturan biaya/pajak diketahui | UNKNOWN untuk aturan bisnis, presisi, dan formula |
| Pembayaran menunjukkan faktur, total faktur, bayar, diskon, dan pembayaran | Validasi alokasi pembayaran parsial/berganda, diskon, serta relasi ke invoice | UNKNOWN; identitas transaksi dan lifecycle belum dikonfirmasi |
| Histori proses menghubungkan jenis dokumen yang berbeda | Resolusi referensi antar dokumen dan penanganan dokumen induk yang tidak ada | ASSUMED perlu; belum ada candidate key source terverifikasi |
| Target mempunyai constraint FK dan kolom wajib/default (lihat `target-audit.md`) | Transformasi/penyediaan nilai target dan urutan parent-detail mungkin diperlukan | VERIFIED struktur target; kecocokan source UNKNOWN |
| Kode aplikasi mendefinisikan status PR 0–5 dan alur persetujuan PO; abstraksi jurnal memiliki operasi approve/post/unposting | Jangan mengubah nilai status atau menulis transaksi langsung sebelum aturan lifecycle, audit trail, dan efek posting dipahami | VERIFIED keberadaan aturan di `app/Abstracts/Inventory/PurchaseRequest.php`, `app/Abstracts/PurchaseOrder.php`, dan `app/Abstracts/Journal.php`; pemetaan status source UNKNOWN |

Belum ada keputusan penanganan NULL, duplikat, primary key, foreign key, status, atau nilai default. Semua itu tetap UNKNOWN hingga schema dan business rules kedua sisi ditinjau. Jangan melakukan normalisasi, penggabungan, pemisahan, atau perubahan ID pada sumber asli.
