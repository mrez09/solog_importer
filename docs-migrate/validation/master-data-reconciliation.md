# Rekonsiliasi Master Data Target

**Tanggal pemeriksaan:** 3 November 2026  
**Mode:** READ-ONLY consistent snapshot; target dikonfirmasi dengan `SELECT DATABASE()` sebagai `db_solog_oli_initial`. Kredensial dan isi record tidak dicatat atau ditampilkan.

## Metode

Pada snapshot yang sama, dihitung jumlah record, nilai non-NULL/distinct, dan kelompok duplikat exact pada kolom key kandidat. Nilai master dibaca hanya untuk normalisasi/hash dan perbandingan internal terhadap key workbook; laporan hanya menampilkan hitungan. Tidak ada update, insert, delete, atau operasi schema. Source `supplier` dan `account` hanya berisi label/kode dari laporan, bukan internal ID.

## Hasil per master

| Master target | Record saat snapshot | Key target | Profil source dan hasil perbandingan | Status / tindak lanjut |
|---|---:|---|---|---|
| `companies` | 4 | 4 kode distinct; 0 kelompok duplicate | Workbook tidak menyediakan company code. README mengidentifikasi perusahaan sumber; relasi kode/ID ke salah satu dari empat company belum dapat dibuktikan dari laporan. | NEEDS REVIEW; perusahaan transaksi tidak boleh dipilih berdasar kemiripan nama saja. |
| `contacts` | 8 | 8 kode distinct dan 8 nama distinct; 3 record berflag supplier/vendor | 62 nama pemasok source distinct; exact normalized name overlap terhadap semua kontak = 0 dan terhadap kontak supplier/vendor = 0. Source tidak menyediakan supplier code. | NEEDS REVIEW; rekonsiliasi butuh identifier resmi (kode, NPWP, atau bukti pemilik data); nama tidak cocok exact dan tidak memadai sebagai key. |
| `items` | 0 | Tidak ada key terisi | 61 kode item source distinct; exact code overlap = 0 karena tabel target kosong pada snapshot. | VERIFIED tabel kosong; item target/master tidak tersedia untuk lookup. Minta master item yang berwenang; jangan membuat item atau ID. |
| `warehouses` | 0 | Tidak ada key terisi | Tidak ditemukan kolom warehouse/gudang eksplisit pada workbook yang diprofilkan. | VERIFIED tabel kosong dan field source tidak tersedia; pilihan gudang UNKNOWN/NEEDS REVIEW. |
| `accounts` | 8 | 8 kode distinct; 0 kelompok duplicate | 88 kode akun source distinct; 4 exact normalized code match terhadap target. | ASSUMED candidate match saja. Company scope, hierarchy, status akun, tujuan debit/kredit, dan asal delapan record perlu review sebelum relasi `account_id`. |
| `type_transactions` | 49 | 49 slug distinct, 49 nama distinct; 0 kelompok duplicate per key | 11 label tipe transaksi source distinct; 1 exact normalized match ke `name`, 0 ke `slug`. | NEEDS REVIEW; label tidak membuktikan semantik slug/type target. Perlu approval pemilik aplikasi/finance. |
| `company_numberings` | 441 | 147 pasangan company/type distinct; tiap pasangan memiliki 3 baris | Workbook menyimpan nomor dokumen, tetapi tidak memberikan konfigurasi prefix/counter yang setara. Tidak ada pembandingan counter yang disetujui. | NEEDS REVIEW; tiga baris per pasangan bukan otomatis duplikat karena konfigurasi lain (`urut`, `type`, prefix, counter) menentukan arti. Jangan ubah sequence. |

“Exact normalized match” hanya perbandingan teks yang dipangkas spasi dan dinormalisasi huruf besar/kecil. Itu bukan verifikasi identitas bisnis.

## Konflik terhadap record transaksi target

| Tabel target kandidat | Baris saat snapshot | Source document code exact match | Interpretasi |
|---|---:|---:|---|
| `purchase_requests` | 0 | 0 dari 736 PR | Tidak ditemukan konflik kode saat ini; source mapping dan semua FK tetap perlu disetujui. |
| `purchase_orders` | 0 | 0 dari 588 PO | Sama; `company_numberings` tetap dapat berbenturan saat generator nomor dipakai. |
| `warehouse_receipts` | 0 | 0 dari 584 GRN/RI | Tidak membuktikan ketersediaan master warehouse/item atau detail link. |
| `um_suppliers` | 0 | 0 dari 15 PID | Tidak membuktikan relasi PID/PO/payable. |
| `invoice_vendors` | 1 | 0 dari 597 PI | Satu record yang ada tetap harus dipertahankan dan provenance-nya belum diketahui. |
| `debts` | 0 | 0 dari 287 SAP | Tidak membuktikan SAP dapat dipetakan tanpa payable/detail allocation. |
| `purchase_order_returns`, `returs` | 0 / 0 | Tidak ada key retur source terdeteksi | Tidak ada transaksi retur pada workbook periode; lifecycle target tetap belum dipilih. |
| `payables`, `payable_details` | 1 / 1 | Tidak digunakan sebagai padanan langsung kode PI | Provenance dan link invoice/detail existing UNKNOWN. Pertahankan dan rekonsiliasi. |
| `journals`, `journal_details` | 2 / 4 | Kode jurnal target tidak dibandingkan ke nomor transaksi source (semantik berbeda) | Risiko duplikasi tetap ada karena beberapa nomor transaksi source muncul kembali di workbook jurnal. |

Tidak ada code exact match bukan bukti bahwa target kosong secara keseluruhan, bahwa record yang ada dummy, atau bahwa import aman. Audit Tahap 2 mencatat total target 3.858 baris (naik dari 2.376); total keseluruhan tidak dihitung ulang pada pemeriksaan master terbatas ini. Record target yang ada dipertahankan.

## Keputusan dan langkah rekonsiliasi

1. Data owner menetapkan company, supplier, item, warehouse, account, serta transaction type berdasarkan sumber identitas authoritative, bukan nama semata.
2. Master kosong (`items`, `warehouses`) memerlukan keputusan bagaimana memenuhi FK/kolom wajib; tidak diisi dengan nilai tebakan.
3. Review 4 code akun yang cocok dan 1 label transaction type yang cocok bersama company, hierarki, serta business meaning sebelum status berubah dari kandidat.
4. Periksa konfigurasi 441 baris `company_numberings` dan counter setelah keputusan tentang mempertahankan nomor historis; jangan jalankan generator selama profiling.
5. Ambil snapshot read-only baru pada tahap implementasi/staging karena database dapat berubah sejak audit ini.

## Bukti

Query metadata dan `SELECT COUNT`, `COUNT(DISTINCT)`, pengelompokan duplikat pada target terkonfirmasi, dijalankan dalam transaksi `READ ONLY` consistent snapshot. Nilai source diambil dari kolom `Kode #`, `Pemasok`, dan `Kode Perkiraan` pada workbook di `docs-migrate`; nilai aktual tidak dicantumkan. Schema target: [target-audit.md](../audit/target-audit.md). Klasifikasi dan provenance: [target-data-classification.md](../audit/target-data-classification.md).
