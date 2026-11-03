# Desain Teknis Importer Terpisah

**Tanggal pembaruan:** 3 November 2026  
**Status:** **PROPOSED**; desain saja. Tidak ada kode importer atau koneksi tulis yang dibuat.

## 1. Batas dan prinsip

Importer direncanakan sebagai aplikasi lokal terpisah dari repository Solog OLI. Ia membaca sembilan XLSX, menerapkan mapping/config yang disetujui, menghasilkan preview dan dry-run, lalu—hanya setelah approval terpisah—dapat mengirim data ke database migrasi terisolasi. `db_solog_oli_initial` adalah referensi audit/schema, bukan target import otomatis.

**BLOCKED:** tidak ada write mode sampai keputusan Stage 3.2, target environment/identity, schema version, master resolution, aturan transformasi dan Accounting strategy disetujui. Database/sumber aplikasi tetap read-only pada tahap desain ini.

## 2. Mode operasi dan gerbang

1. **INSPECT:** inventaris workbook, sheet, header, merged ranges, kandidat baris dan profil; tidak menyentuh DB.
2. **PREVIEW:** tampilkan planned source→target values, transformasi, referensi, master resolution, FK serta warning/hold. Tidak menulis.
3. **DRY-RUN:** jalankan pipeline validasi, urutan, crosswalk simulation dan reconciliation terhadap snapshot/sandbox read-only atau in-memory; tidak ada commit/SQL write. Bukti no-write perlu diverifikasi teknis sebelum dianggap aman.
4. **IMPORT:** mode terpisah, disabled by default, hanya database migrasi yang allowlisted dan setelah approval manusia spesifik, credential aman, PREVIEW/DRY-RUN disetujui dan backup/rollback disahkan. Production memerlukan approval dan gerbang tersendiri.

Tidak boleh ada flag implisit yang membuat PREVIEW/DRY-RUN melakukan write. UI/CLI harus menampilkan mode, target identity yang aman, jumlah record, mapping version dan konfirmasi batch sebelum import.

## 3. Pipeline logis

`Workbook bytes → Workbook Reader → layout/row candidates → Data Normalizer → Mapping Engine → Transformation Engine → Master Resolver → Validation Engine → Preview/hold report → Dry-run/reconciliation → (approval gate) Import Executor → Crosswalk + Import Logger → Post-import reconciliation`

Setiap record membawa lineage: source file relative path + SHA-256, sheet, cell/row range locator, source doc/line refs, mapping/config version, transformation notes, match evidence dan status. Locator harus stabil setelah layout diuji; row number saja belum ditetapkan sebagai key.

## 4. Komponen

| Komponen | Tanggung jawab dan batas |
|---|---|
| Workbook Reader | Membuka XLSX read-only; enumerasi sheet, dimensions, cell values/types/styles, date serials, merged ranges, formulas dan hidden/blank rows. Tidak menyimpan perubahan ke workbook. |
| Layout Detector | Mengidentifikasi header, repeated headers, section breaks, detail/header/subtotal/total, continuation dan merged-cell inheritance sebagai kandidat; hasil ambiguous diberi hold, bukan ditebak. |
| Data Normalizer | Membuat representation internal tanpa mengubah sumber; parse empty/null, whitespace, decimal/date display, merged continuation dan repeated labels sambil mempertahankan raw value/cell coordinates. |
| Mapping Engine | Membaca mapping JSON berversi yang telah direview; memetakan source sheet/field ke target candidate dan grain header/detail/relation. Reject unknown mapping keys/unsupported version. |
| Transformation Engine | Menjalankan hanya named/typed transform yang tercantum dan disetujui, misalnya Excel serial→date atau locale decimal parse. Tidak mengandung formula tax/rounding/status default yang belum disahkan. |
| Master Resolver | Resolve hanya lewat identifier/crosswalk authoritative dan validity context; hasil `MATCHED`, `AMBIGUOUS`, `UNMATCHED`, `HOLD`. Nama mirip tidak cukup dan tidak membuat master. |
| Validation Engine | Required field/type/length/domain, uniqueness policy, FK parent, amount/quantity controls, partial limits yang disahkan, status dan cross-document rules. UNKNOWN business rule tidak lulus sebagai pass. |
| Preview | Menampilkan perubahan yang direncanakan per record, source lineage, resolved IDs (aman), transformed values, blockers, warnings dan counts. Ekspor report terpisah tanpa secret. |
| Dry Run | Mengeksekusi plan tanpa persistent DB writes; simulasi FK/sequence/idempotency dan menyajikan expected counts/reconciliation. Menolak koneksi dengan privilege write atau memastikan mock/snapshot mode. |
| Import Executor | Terisolasi dari komponen preview; menerima hanya signed/approved batch plan, target database allowlisted, credentials dari secret store lokal, transactions/batches dan idempotency guard. Tidak digunakan pada tahap ini. |
| Crosswalk Manager | Menyimpan source document/line locator ↔ target table/internal ID, match evidence, batch, status dan version; PK target internal, nomor workbook business key saja. Konflik menghentikan proses. |
| Import Logger | Catat batch/operator/time, source fingerprint, config/schema/app version, mode, counts, row outcomes, errors, target identity non-secret dan approval reference. Hindari credential dan data sensitif berlebihan. |
| Reconciliation | Bandingkan counts, detail counts, quantity/value, payable/payment/deposit, stock dan journal balance dengan toleransi yang disetujui; exception wajib disposition. |

## 5. Konfigurasi mapping JSON

JSON adalah format konfigurasi usulan, bukan mapping final. Konfigurasi minimum yang perlu dikembangkan setelah approval:

```json
{
  "mapping_version": "draft-version-required",
  "source": {"workbook": "relative/path.xlsx", "sheet": "sheet-name"},
  "grain": {"header": "business-document", "detail": "source-line-locator"},
  "locator": {"strategy": "approved-stable-locator-required"},
  "fields": [],
  "relations": [],
  "transforms": [],
  "null_policy": "hold-required-or-unresolved",
  "duplicate_policy": "detect-and-hold",
  "status": "DRAFT_NOT_IMPORTABLE"
}
```

Ini placeholder schema konseptual—bukan file executable. Config harus memuat target table/column, source column/cell, target required flag, transform ID+version, null/empty policy, default provenance bila disetujui, duplicate/PK/FK handling, evidence, approver reference dan status VERIFIED/ASSUMED/UNKNOWN/NEEDS REVIEW. Parser menolak config yang statusnya bukan approved-for-import atau memiliki UNKNOWN/NEEDS REVIEW pada field wajib.

## 6. Required field dan unresolved handling

Validasi harus memisahkan errors (tidak valid), warnings (perlu review), dan holds (tidak boleh lanjut). Field target wajib yang tidak ada di workbook—company/user/status/warehouse/date needed/due date/payment method dan data operasi lainnya—tidak diisi default importer. Master/item/unit/FK tidak dikenal; ambiguous link; baris jurnal tak seimbang; atau field required kosong menghasilkan HOLD dengan reason code, source locator dan pertanyaan owner.

Target terkait: 873 unit kosong pada 990 detail GRN kandidat. Jika unit tetap tak terbukti, tahan detail itu dan dependent receipt/invoice allocation sesuai policy yang disetujui; jangan ubah menjadi unit dasar asumsi.

## 7. Crosswalk, idempotency dan konflik

Crosswalk konseptual memuat batch ID, source file hash/path, sheet, document type/no, stable line locator, parent reference, target table/id, match method, evidence reference, mapping version dan review state. Nomor dokumen tidak pernah menjadi target PK. Source row locator tidak disahkan sebelum uji stabilitas terhadap merged cells, repeated sections dan workbook revision.

Idempotency proposal: unique source fingerprint + mapping version + stable locator + target entity per batch policy. Rerun same batch menghasilkan no-op/report only bila crosswalk target match exactly; mismatch atau existing target conflict dihentikan dan dilaporkan. Jangan overwrite, auto-merge, atau upsert data existing tanpa kebijakan tertulis dan persetujuan. Idempotency final bergantung pada strategi target terpisah dan rerun/correction policy yang disetujui.

## 8. Keamanan teknis

- Default credentials tidak disimpan di JSON, command line, source code, log, atau laporan. Ambil dari secret store/environment process yang terlindungi.
- PREVIEW/DRY-RUN harus menolak koneksi write-capable atau memakai offline/mock/snapshot evaluation; database read-only user adalah defense-in-depth.
- Import Executor memvalidasi nama database/host/environment allowlist dan menampilkan target identity tanpa credential.
- XLSX diperlakukan sebagai input tidak tepercaya: batas ukuran, file type check, zip expansion limits, formula policy dan sanitasi output report.
- Raw source data dibatasi akses; report mencatat locator, bukan menyalin seluruh workbook.
- Batch isolation, transaction boundary, retry dan rollback harus diuji pada staging terisolasi sebelum write approval.

## 9. Keputusan/blocker sebelum implementasi write path

1. Business approvals pada `../decision/mapping-decision-register.md` (company/master, GRN unit, PO–GRN, GRN–PI, PI/SAP/PID, journal strategy).
2. Mapping Data Dictionary disetujui, stable locator, target schema/app version dan required-field disposition.
3. Target migration database terpisah: owner, environment, schema provisioning, access, backup dan baseline.
4. Resolved master crosswalk; target items dan warehouses saat audit kosong, sementara contacts/accounts candidate tidak cukup.
5. Payment/deposit allocation, tax/discount/rounding/status policy serta journal no-double-posting/balance rules.
6. Security review, operator authorization, batch retention, rollback/recovery dan approval gate.

## 10. Tahap implementasi setelah persetujuan

Urutan rekomendasi: (1) schema/config contract dan fixtures non-production; (2) XLSX reader/layout detector + profil; (3) normalizer dan stable locator; (4) mapping/transformation config dengan validator ketat; (5) master resolver dan crosswalk store; (6) validation/hold report; (7) PREVIEW UI/CLI; (8) DRY-RUN serta reconciliation; (9) security/idempotency review dan uji staging; (10) Import Executor hanya setelah approval spesifik; (11) rekonsiliasi batch dan sign-off. Tahap saat ini hanya mendokumentasikan desain.
