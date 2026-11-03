# Ringkasan Tahap 3.2 — Mapping Decision & Approval

**Tanggal pembaruan:** 3 November 2026  
**Status:** analisis selesai untuk direview; belum ada persetujuan business owner.

## Temuan

- **VERIFIED:** dokumentasi/profiling saat ini memuat 9 workbook; audit awal pernah menyebut 8. Kelengkapan daftar tetap perlu disahkan Data Owner.
- **VERIFIED:** sumber berupa laporan Excel, bukan relational dump; identifier baris/dokumen tidak otomatis menjadi PK/FK.
- **VERIFIED:** master: 61 kode item vs 0 target items; 62 nama supplier vs 8 contacts (3 berflag supplier/vendor, exact normalized match 0); 88 kode account vs 8 target (4 exact-code candidates); 11 label tipe vs 49 target (1 exact-name candidate). Kandidat teks belum membuktikan makna/identitas.
- **VERIFIED:** 873/990 kandidat detail GRN tidak memiliki `Satuan`, bukan akibat vertical merge; unit default tidak boleh ditebak.
- **VERIFIED:** Histori menampilkan pola 28 RI multi-PO, 2 RI multi-PI, 1 PI multi-RI, 49 PI multi-SAP, 45 SAP multi-PI dan empat PID–PI pairs. Ini co-occurrence, bukan bukti FK atau alokasi nilai.
- **VERIFIED:** workbook jurnal memuat 5.645 kandidat baris detail; identifier overlap dengan SAP/PI/RI/PID. Aplikasi memiliki auto-journal dan jurnal manual. Keseimbangan jurnal global/identitas overlap belum terbukti.
- **VERIFIED:** snapshot Tahap 2 menyebut 3.858 target records, sebelumnya 2.376; asal semua record belum diketahui. Target harus dipertahankan, bukan dianggap dummy.

## Keputusan kritis belum ada

Master company/supplier/item/warehouse/account/type dan numbering; unit GRN; cardinality PO–GRN dan GRN–PI; grain serta alokasi PI/SAP/PID; perlakuan diskon/pajak/saldo; cakupan retur/2025; dan strategi ledger/journal. Semuanya berstatus OPEN atau NEEDS EVIDENCE di `mapping-decision-register.md`; tidak ada APPROVED.

## Risiko penghambat Tahap 4

1. Master belum teridentifikasi secara authoritative, berisiko FK dan transaksi salah pihak/item/lokasi.
2. Unit kosong pada mayoritas detail kandidat GRN menghalangi kuantitas dan stok yang dapat dipercaya.
3. Hubungan PO–RI/RI–PI/SAP/PID belum membuktikan kardinalitas, partial quantity, atau allocation; ada risiko receipt/invoice/payment ganda.
4. Saldo payable, potongan dan uang muka belum dapat direkonsiliasi tanpa voucher/alokasi.
5. Jurnal berisiko double posting karena approval workflow dapat membuat jurnal otomatis; accounting owner belum memilih ledger of record dan global debit=kredit belum dibuktikan.
6. Data target berubah dari 2.376 menjadi 3.858 dan provenance belum lengkap.

## Pertanyaan manusia

Jawaban spesifik dan bukti yang diminta dikelompokkan pada `business-owner-review.md` untuk Data Owner, Procurement, Finance, Accounting, dan Application Reviewer. Prioritas: master resmi dan cakupan, unit/receipt linkage, voucher dan alokasi pembayaran/deposit, serta keputusan Accounting Owner tentang strategi jurnal.

## Kesiapan Tahap 4

**Belum memenuhi syarat untuk Migration Plan final.** Gerbang review mapping pada `AGENTS.md` belum terpenuhi karena keputusan kritis dan bukti masih terbuka.

Syarat minimum: Data Owner mengesahkan workbook/periode; master resmi atau disposisi hold disetujui; unresolved unit dan relasi memiliki bukti/keputusan; PI/SAP/PID direkonsiliasi ke voucher dan saldo; Accounting memilih ledger, status posting dan kontrol balance/double posting; Application Reviewer mengonfirmasi required fields dan workflow; baseline target/provenance serta target migrasi terpisah disepakati; seluruh approver dan pengecualian tercatat tertulis.

## Berkas dibuat

- `docs-migrate/decision/mapping-decision-register.md`
- `docs-migrate/decision/business-owner-review.md`
- `docs-migrate/decision/mapping-decision-impact.md`
- `docs-migrate/decision/stage-3-2-summary.md`

Tidak ada database, source code, workbook, atau dokumen audit/mapping terdahulu yang diubah.
