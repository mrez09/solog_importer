# Validasi Relasi Sumber, Target, dan Kandidat Mapping

**Tanggal pemeriksaan:** 3 November 2026  
**Metode:** inspeksi read-only workbook/XML, co-occurrence identifier pada sheet Histori (dengan vertical merge inheritance), schema target, dan bukti source code yang dirangkum di `business-rules.md`. Co-occurrence workbook bukan FK.

## Hasil profil relasi di workbook Histori

Kolom tahapan Histori memuat PR (B), PO (D), RI/GRN (F), PID (H), PI (J), retur (L), dan SAP (N). Setelah referensi visual dari vertical merge diterapkan untuk analisis, pasangan dihitung dari identifier yang muncul bersama pada baris yang sama.

| Pasangan proses | Baris Histori dengan pasangan | Pasangan dokumen unik | Entitas sisi kiri/kanan | Kardinalitas yang terlihat |
|---|---:|---:|---:|---|
| PR → PO | 799 | 716 | 716 PR / 716 PO | Tidak ada PR atau PO yang berpasangan dengan lebih dari satu dokumen di pasangan teramati. |
| PO → RI/GRN | 737 | 654 | 654 PO / 596 RI | 28 nomor RI muncul terkait dengan lebih dari satu PO; perlu direkonsiliasi terhadap satu `purchase_order_id` per target receipt header. |
| RI/GRN → PI | 656 | 557 | 555 RI / 556 PI | 2 RI terhubung ke >1 PI; 1 PI terhubung ke >1 RI. Penggunaan ulang receipt belum diputuskan. |
| PI → SAP | 541 | 510 | 454 PI / 329 SAP | 49 PI terhubung ke >1 SAP; 45 SAP terhubung ke >1 PI. Granularitas alokasi perlu dikonfirmasi. |
| PID → PI | 4 | 4 | 4 PID / 4 PI | Co-occurrence 1:1 untuk pasangan teramati; belum membuktikan alokasi PID terhadap invoice atau pembayaran. |

**VERIFIED:** ini jumlah pasangan key dan baris co-occurrence pada workbook Histori sesuai struktur visual. **UNKNOWN/NEEDS REVIEW:** arti kardinalitas bisnis, kelengkapan referensi, apakah baris yang sama adalah dokumen benar-benar terhubung, dan apakah merged value harus diwariskan sebagai relasi. Validasi ini tidak mengarang FK source.

## Rekonsiliasi Histori dengan workbook transaksi

| Tipe | Export unik | Histori unik | Cocok exact identifier | Hanya Histori | Hanya export |
|---|---:|---:|---:|---:|---:|
| PR | 736 | 746 | 736 | 10 | 0 |
| PO | 588 | 716 | 586 | 130 | 2 |
| RI/GRN | 584 | 597 | 584 | 13 | 0 |
| PID | 15 | 15 | 15 | 0 | 0 |
| PI | 597 | 692 | 597 | 95 | 0 |
| SAP | 287 | 336 | 287 | 49 | 0 |

Histori memiliki referensi 2025: PR 9, PO 10, RI 10, PI 10 identifier unik. Referensi tersebut membantu menjelaskan kemungkinan sebagian dokumen hanya histori, tetapi tidak cukup untuk mengasumsikan semua unmatched adalah tahun 2025. Khusus PO terdapat 130 referensi Histori yang tidak ada di export PO serta 2 PO export tanpa pasangan di Histori. Semua unmatched **NEEDS REVIEW**, bukan dihapus.

## Validasi relasi terhadap aplikasi/schema target

| Relasi kandidat | Bukti aplikasi/schema target | Bukti source profiling | Status mapping |
|---|---|---|---|
| PR → PO | `purchase_order_details.purchase_request_detail_id` nullable dan tabel pivot `purchase_order_purchase_request`; controller mendukung PO langsung tanpa PR. | 716 pasangan unik di Histori, tetapi PR detail key tidak tersedia pada report. | VERIFIED sebagai kemampuan aplikasi dan pasangan report; pemetaan detail-to-detail UNKNOWN/NEEDS REVIEW. |
| PO → GRN | Kode receipt memakai field header `warehouse_receipts.purchase_order_id`; satu field header mengarah maksimum ke satu PO. Field ini tidak tercantum sebagai FK deklaratif pada target audit, meskipun code path menggunakannya. Relasi detail memakai `purchase_order_receipt_details`. | 654 pasangan unik; 28 nomor RI berkaitan dengan >1 PO. | NEEDS REVIEW: perlu menentukan apakah satu nomor RI mewakili banyak receipt, beberapa PO, atau artefak report sebelum memenuhi satu PO per target header. |
| GRN → PI | `InvoiceVendorController` mencari `warehouse_receipts.code` melalui `invoice_vendor_details.reff_no`; satu PI dapat memuat beberapa receipt. | 557 pasangan; 1 PI memiliki beberapa RI dan 2 RI memiliki beberapa PI pada Histori. | VERIFIED sebagai pola code path; reuse satu GRN pada PI berbeda UNKNOWN/NEEDS REVIEW. |
| PI → payable | Approval invoice membuat `payables`/`payable_details`; `invoice_vendors.payable_id` dan `invoice_vendor_details.payable_detail_id` tersedia dengan FK target. | Histori memuat PI→SAP, tetapi tidak berisi target payable ID. | VERIFIED alur aplikasi; source PI-to-payable target ID hanya dapat dibuat lewat crosswalk setelah PI resolve. |
| PID → pembayaran | `debt_details.um_supplier_id` berelasi ke `um_suppliers`; alur payment dapat menggunakan deposit. | 15 PID dan 13 PO teracu pada workbook PID; 4 PID-PI pair pada Histori. | VERIFIED kemampuan aplikasi; hubungan PID ke pembayaran/PI source-specific UNKNOWN. `No Pesanan #` tidak membuktikan FK langsung. |
| SAP → payable detail | Model/controller pembayaran menulis alokasi debit payable; target memiliki `debt_details.payable_id`, `payable_detail_id`, dan `um_supplier_id`. | 510 pasangan PI-SAP di Histori; 49 PI multi-SAP dan 45 SAP multi-PI. | NEEDS REVIEW: alokasi per invoice/detail dan pembayaran parsial harus direkonstruksi dengan bukti; nomor invoice bukan internal ID. |
| Transaksi → jurnal | Modul operasional menghasilkan jurnal otomatis pada kondisi tertentu; `journals` juga mendukung entri manual. | Identifier dalam workbook jurnal exact-match dengan transaksi source: SAP 234, PI 36, RI 32, PID 2; tidak ada PR/PO token yang cocok pada pola yang dipakai. | Risiko duplikasi VERIFIED sebagai overlap nomor; apakah tiap overlap merupakan jurnal otomatis dari transaksi itu UNKNOWN. Strategi perlu persetujuan akuntansi. |

## Risiko duplicate journal generation

Workbook `Keseluruhan Jurnal` berisi 5.645 baris kandidat detail kode akun dan nomor transaksi yang overlap dengan workbook operasional: sekurangnya 304 identifier transaksi unik lintas SAP/PI/RI/PID pada pola nomor yang cocok. Source code menunjukkan approval invoice, receipt, PID, payment, dan beberapa retur dapat membuat jurnal. Bila modul transaksi diposting melalui alur aplikasi dan jurnal lama juga diimpor, jurnal dapat tercatat dua kali. Jumlah exact line/journal duplicate belum dapat dihitung karena batas grup header jurnal, nomor journal source, status posting, dan linkage target belum dibuktikan.

**Rekomendasi:** sebelum memetakan jurnal, accounting owner menetapkan salah satu sumber authoritative dan aturan impor. Jangan mengimpor workbook jurnal bersamaan dengan regenerasi otomatis tanpa rekonsiliasi per transaksi dan validasi debit=kredit.

## Bukti

Workbook `OLI_HISTORI_Histori Proses Pembelian_2026-01-01_2026-10-26.xlsx`, `OLI_JURNAL_Keseluruhan Jurnal_2026-01-01_2026-10-26.xlsx`, workbook operasional PR/PO/GRN/PID/PI/SAP, dan schema/code diringkas di [business-rules.md](../audit/business-rules.md), [workflow-analysis.md](../audit/workflow-analysis.md), [target-audit.md](../audit/target-audit.md). ID target dan nilai record tidak diekspos.
