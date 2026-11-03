# Solog OLI Migration Importer

Fondasi aplikasi web lokal untuk menyiapkan dan meninjau migrasi. Project ini terpisah dari repository Laravel Solog OLI.

## Status dan batas keselamatan

- Python yang didukung: `>=3.11,<3.14` (konfigurasi lokal saat dibuat: Python 3.13.3).
- Backend: FastAPI; template: Jinja2; HTMX disiapkan untuk interaksi halaman.
- Fitur Stage 4.2.2: upload beberapa workbook `.xlsx`, penyimpanan salinan read-only, SHA-256, serta inspeksi worksheet/cell/merged ranges dan preview read-only.
- Belum ada target database, konfigurasi database, SQL, mapping bisnis, atau Import Executor.
- Tidak ada koneksi ke database Solog OLI.
- Migration batch, business mapping dan validation report tetap belum tersedia.

## Persyaratan

- Python 3.11 atau 3.12 direkomendasikan; Python 3.13 dapat digunakan dengan dependency versions yang memenuhi batas di `pyproject.toml`.
- `pip` dan `venv`.

## Instalasi di Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Jika menggunakan Python 3.13, ganti `py -3.11` dengan `py -3.13`.

## Menjalankan aplikasi

```powershell
uvicorn app.main:app --reload
```

Buka `http://127.0.0.1:8000/`. Health check tersedia di `http://127.0.0.1:8000/health`.

Untuk mengubah nama aplikasi atau environment, gunakan environment variables opsional `SOLOG_IMPORTER_APP_NAME` dan `SOLOG_IMPORTER_ENVIRONMENT`. Logging level dapat diatur dengan `SOLOG_IMPORTER_LOG_LEVEL`. Jangan menaruh secret pada config/log. Aplikasi belum membaca `.env`.

## Workbook (Stage 4.2.2)

Buka `/workbooks` untuk mengunggah satu atau beberapa file `.xlsx`. Setiap file divalidasi sebagai paket XLSX sebelum disimpan, diberi nama internal unik, dan memiliki metadata nama asli serta SHA-256. Ukuran maksimum default adalah **100 MiB per file** dan dapat diubah melalui `SOLOG_IMPORTER_MAX_UPLOAD_SIZE_BYTES` (jumlah byte positif).

Salinan dan metadata disimpan lokal di `data/uploads/`, terpisah dari kode aplikasi, sampai dihapus manual. Direktori `data/` dikecualikan dari version control. Daftar dan detail workbook menampilkan status baca; detail mencakup urutan/status/dimensi worksheet, preview terbatas, formula, tipe/nilai cell, format angka, style, merged ranges, serta locator dengan nomor baris fisik. Workbook dibuka tanpa menyimpan perubahan dan formula tidak dihitung atau diganti dengan cached result.

Unggahan ditolak jika ekstensi/struktur XLSX tidak valid, file rusak/terenkripsi, ZIP/XML mencurigakan, atau batas keamanan paket terlampaui. Fitur ini tidak melakukan mapping, normalisasi, database access, atau impor.

## Menjalankan test

```powershell
python -m pytest
```

Test memakai workbook dummy sintetis dan FastAPI TestClient; tidak mengakses database atau workbook sumber dalam `docs-migrate/`.

## Struktur saat ini dan ekstensi mendatang

`app/` memuat entry point, config, logging, router health dan workbook, service upload/reader, model Pydantic, template Jinja2, dan static CSS. `tests/` mencakup endpoint dan workbook sintetis. Layout Detector, Data Normalizer, Mapping Engine, Transformation Engine, Master Resolver, Validation Engine, Preview lanjutan, Dry-Run, dan Reconciliation tetap untuk tahap berikutnya setelah mapping/aturan disetujui. Import Executor secara eksplisit belum dibuat.

## Keputusan teknis yang belum ditentukan

- Versi Python/runtime final dan strategi environment deployment lokal.
- Sumber/hosting HTMX untuk penggunaan offline (fitur upload memakai HTMX dari CDN; form tetap dapat dikirim tanpa HTMX).
- Kebijakan autentikasi lokal, CORS, host binding dan CSRF sebelum fitur menerima file.
- Retensi ditetapkan untuk Stage 4.2.2: simpan sampai dihapus manual; autentikasi/CSRF dan kebijakan akses lokal tetap perlu review sebelum penggunaan multi-user atau jaringan.
- Crosswalk dan batch state store belum dibuat; metadata upload saja disimpan sebagai JSON lokal, tanpa database.
- Target database import, credential mechanism, privilege, schema version, backup dan rollback.
- Format mapping JSON final serta approval workflow.
- Kebijakan logging dan perlindungan data workbook untuk penggunaan multi-user/jaringan.

Semua keputusan bisnis dan mapping tetap tunduk pada dokumen Stage 3.2 dan Stage 4.1 di repository Solog OLI.
