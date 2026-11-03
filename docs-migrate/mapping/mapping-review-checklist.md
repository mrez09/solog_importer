# Checklist Review Migration Mapping

**Tanggal pembaruan:** 3 November 2026  
**Status:** menunggu review bisnis, aplikasi, dan akuntansi. Semua item belum disetujui kecuali dinyatakan lain.

## Konflik/kondisi audit yang harus dipertahankan

- [ ] Audit awal menghitung 8 workbook; Tahap 2 menemukan 9 workbook XLSX. Inventaris lengkap dan sumber hitungan harus disepakati.
- [ ] Target bertambah dari 2.376 menjadi 3.858 baris (53 menjadi 104 tabel berisi). Konfirmasi snapshot baru dan provenance setiap kelompok data sebelum migrasi.
- [ ] Asal record target belum seluruhnya diketahui; jangan hapus, timpa, atau menandai semua sebagai seed/fixture.
- [ ] Referensi histori mencakup tahun 2025 meskipun workbook bertanggal periode 2026. Tentukan cakupan dan resolusi parent historis.
- [ ] Workbook retur menyebut tidak ada transaksi pada periode; ini tidak membuktikan tidak ada retur sebelum/sesudah periode.

## Keputusan bisnis yang memerlukan persetujuan

- [ ] Definisi grain, row locator, header/detail, merged cell, baris lanjutan, subtotal, dan empty cells per workbook.
- [ ] Unique natural key setiap nomor PR, PO, GRN, PID, PI, SAP, retur dan jurnal; nomor internal vs nomor eksternal.
- [ ] Company target untuk seluruh transaksi dan cara resolusi company.
- [ ] Supplier/item/akun/wilayah/gudang yang cocok; natural key authoritative dan prosedur manual untuk ambiguous/unmatched. Nama saja tidak cukup.
- [ ] PO yang tanpa PR: boleh diimpor langsung dan bagaimana mengisi `purchase_request_detail_id` / pivot jika referensi PR tak ada.
- [ ] Relasi PO → GRN dan GRN detail → PO detail; apakah GRN dapat menerima lebih, dan validasi kuantitas parsial.
- [ ] Relasi GRN → PI, kemungkinan penggunaan ulang GRN dalam invoice, dan cara mengidentifikasi GRN dari workbook PI/history.
- [ ] Tanggal receive, due date, tanggal kebutuhan PR, status, approval/posting, pembuat, dan metadata wajib yang tidak tersedia pada laporan.
- [ ] Definisi mata uang dan konversi FX; target currency field tidak teridentifikasi pada tabel transaksi kandidat.
- [ ] Formula subtotal/total, PPN, PPh, diskon, biaya tambahan, presisi dan pembulatan; tidak ada yang boleh ditebak.
- [ ] Makna `Terpakai/Retur`, `Sisa Uang Muka`, arah debit/kredit PID, metode bayar, dan alokasi PID ke payable/invoice.
- [ ] Grain pembayaran SAP per bukti/per invoice, perlakuan pembayaran parsial, diskon, bank/account, giro, bukti potong dan overpayment.
- [ ] Pemilihan lifecycle retur (`purchase_order_returns` vs `returs`), relasi receipt/PO, dampak stok, journal, payable/credit note.
- [ ] Kebijakan nomor dokumen target dan `company_numberings`; sequence/counter saat mempertahankan nomor historis.
- [ ] Strategi jurnal: laporan jurnal sebagai import authoritative, rekonsiliasi saja, atau jurnal dibentuk oleh transaksi aplikasi. Cegah double posting.
- [ ] Aturan akun per company, tipe transaksi, relasi jurnal ke source transaction, status posted/approved, dan toleransi balance/rounding.
- [ ] Kebijakan empty/null, duplicate, line ambiguity, unmatched reference, truncation field, dan penanganan orphan FK.

## Mapping UNKNOWN / NEEDS REVIEW per modul

| Modul | Mapping/aturan belum selesai |
|---|---|
| PR | company, warehouse, date_needed, creator, status/approval, `is_pallet`, approved qty/PO qty, item ID dan detail-line key. |
| PO | supplier/item FK, company/warehouse, creator/status/payment type, currency, PPN, total/header summary, `files`, PR detail link, due date. |
| GRN | warehouse/company/creator, timestamp jam/zona, PO header/detail links, unit, rack/storage/quality/pallet/stock dimensions dan wajib detail lain. |
| PID | arah saldo debit/kredit, supplier/company/type/status, pemecahan penggunaan/pengembalian, metode pembayaran, referensi PO/payable, akun dan journal. |
| PI | nomor eksternal vs internal, invoice receive/due dates, company/status/tax flags, detail quantity/price, account/category, formula nominal, GRN reff dan payable/journal link. |
| SAP | grain bukti vs alokasi invoice, pembayaran parsial, bank/account/payment type, diskon, overpayment, invoice payable detail, PID dan metadata required. |
| Retur | transaksi source tidak ditemukan untuk periode; pemilihan lifecycle, source receipt/PO detail, price/account, stok dan payable effect. |
| Histori | tipe/key tiap referensi, uniqueness, nomor lintas tahun, hubungan pada detail dan perlakuan dokumen yang hilang. |
| Jurnal | group/header-detail, tipe transaksi, company, account IDs, relasi source, keseimbangan, posting state dan duplicate terhadap jurnal otomatis. |

## Review konflik dengan data target

- [ ] Tinjau data target secara read-only dan ambil snapshot baru sebelum langkah selanjutnya; angka saat ini dapat berubah.
- [ ] Pertahankan semua record yang ada; tentukan provenance/fixture melalui bukti independen, bukan hanya `%CODEX%`.
- [ ] Rekonsiliasi master yang berisi data pada snapshot: `companies` (4), `contacts` (8), `accounts` (8), `company_numberings` (441); catat `invoice_vendors` (1), `payables` (1), `payable_details` (1), `journals` (2). Tidak ada record yang boleh dianggap milik source atau dihapus tanpa bukti.
- [ ] Tabel kandidat yang kosong pada snapshot tetap dianggap struktur aplikasi; cek ulang di staging/pada waktu implementasi.
- [ ] Cek konflik kode/natural key dan nomor transaksi dengan kontrol akses yang aman; jangan tampilkan kredensial atau data pribadi pada laporan.
- [ ] Pastikan tidak ada double-create journal/payable/stock saat memilih jalur import operasional vs accounting.

## Gerbang persetujuan

- [ ] Owner procurement menyetujui PR/PO/GRN, kuantitas, unit, dan relasi.
- [ ] Owner finance menyetujui PID/PI/SAP, pajak/diskon, saldo dan alokasi.
- [ ] Controller/accounting menyetujui jurnal, chart of accounts, balancing, posting state dan duplicate handling.
- [ ] Data owner menyetujui aturan master match, konflik, duplikasi, empty/null, dan histori 2025.
- [ ] Reviewer aplikasi menyetujui target column requirements, status, sequence, approval/posting dan efek side-effect.
- [ ] Setiap keputusan dicatat dengan tanggal, bukti, reviewer, alasan, dan dampak sebelum data dictionary ditetapkan sebagai final.

## Status keputusan

Belum ada persetujuan bisnis/akuntansi yang tercatat dalam sumber yang ditelaah. Sampai checklist yang relevan disetujui, dokumen ini adalah kandidat mapping tahap 3 dan belum menjadi otorisasi Migration Plan atau import.
