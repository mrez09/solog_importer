# Solog OLI Migration Importer

Fondasi aplikasi web lokal untuk menyiapkan dan meninjau migrasi. Project ini terpisah dari repository Laravel Solog OLI.

## Status dan batas keselamatan

- Python yang didukung: `>=3.11,<3.14` (konfigurasi lokal saat dibuat: Python 3.13.3).
- Backend: FastAPI; template: Jinja2; HTMX disiapkan untuk interaksi halaman.
- Fitur Stage 4.2.2: upload beberapa workbook `.xlsx`, penyimpanan salinan read-only, SHA-256, serta inspeksi worksheet/cell/merged ranges dan preview read-only.
- Fitur Stage 4.2.3: deteksi kandidat layout GRN/RI, normalisasi teknis tanpa mengubah makna, source locator, unresolved/HOLD, dan preview kandidat read-only.
- Fitur Stage 4.2.4: kandidat mapping dan validasi RI dengan profil JSON lokal non-database, target placeholder, status review, dan preview tanpa eksekusi transformasi.
- Fitur Stage 4.2.5: preview dan dry-run lokal dengan ringkasan status kandidat, payload raw per target entity placeholder, filter/paginasi, relasi UNKNOWN/HOLD, serta laporan audit JSON tanpa eksekusi transformasi.
- Fitur Stage 4.2.6: host allowlist localhost, CSRF token dan same-origin validation untuk POST, serta security headers.
- Fitur Stage 4.4.1: profil TARGET nonrahasia yang dapat dibuat, ditinjau, diedit, dipilih, dan dihapus secara lokal. Profil tidak menyimpan password; belum ada koneksi database atau SQL.
- Fitur Stage 4.4.2: verifikasi koneksi opsional hanya ke profil TARGET yang dipilih eksplisit, dengan password per-request, konfirmasi identitas, pemeriksaan grants least-privilege, dan pembacaan metadata schema read-only. Tidak ada baseline target yang disetujui.
- Database `db_solog_oli_initial` hanya referensi audit/schema dan dilindungi agar tidak diterima sebagai TARGET.
- Belum ada Import Executor atau mapping bisnis yang disetujui.
- Tidak ada koneksi database dilakukan selama implementasi Stage 4.4.2. Saat aplikasi dipakai, koneksi hanya dicoba setelah pengguna memilih TARGET, memasukkan ulang password, dan mengonfirmasi identitas; database referensi selalu ditolak.
- Belum ada mapping bisnis final atau validation report untuk persetujuan impor; Stage 4.2.4 menyediakan kandidat mapping dan hasil validasi awal untuk review.
- Stage 4.4.3 menyediakan halaman kandidat mapping master dari laporan PR/GRN yang diunggah. Semua evidence terikat pada ID upload dan SHA-256, setiap occurrence dipertahankan, target historis hanya referensi, dan mapping tetap REVIEW_REQUIRED. Fitur ini tidak membuat target ID, menggabungkan data, mengubah status, atau menjalankan impor.

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
uvicorn app.main:app --reload --host 127.0.0.1
```

Buka `http://127.0.0.1:8000/`. Health check tersedia di `http://127.0.0.1:8000/health`.
Jangan bind ke `0.0.0.0`, mempublikasikan port, atau menaruh aplikasi di belakang proxy/jaringan: aplikasi belum memiliki autentikasi dan tidak ditujukan untuk penggunaan multi-user atau deployment publik. Host allowlist bukan pengganti firewall atau kontrol akses jaringan.

Untuk mengubah nama aplikasi atau environment, gunakan environment variables opsional `SOLOG_IMPORTER_APP_NAME` dan `SOLOG_IMPORTER_ENVIRONMENT`. Logging level dapat diatur dengan `SOLOG_IMPORTER_LOG_LEVEL`. Jangan menaruh secret pada config/log. Aplikasi belum membaca `.env`.

## Workbook (Stage 4.2.2)

Buka `/workbooks` untuk mengunggah satu atau beberapa file `.xlsx`. Setiap file divalidasi sebagai paket XLSX sebelum disimpan, diberi nama internal unik, dan memiliki metadata nama asli serta SHA-256. Ukuran maksimum default adalah **100 MiB per file** dan dapat diubah melalui `SOLOG_IMPORTER_MAX_UPLOAD_SIZE_BYTES` (jumlah byte positif).

Salinan dan metadata disimpan lokal di `data/uploads/`, terpisah dari kode aplikasi, sampai dihapus manual. Direktori `data/` dikecualikan dari version control. Daftar dan detail workbook menampilkan status baca; detail mencakup urutan/status/dimensi worksheet, preview terbatas, formula, tipe/nilai cell, format angka, style, merged ranges, serta locator dengan nomor baris fisik. Workbook dibuka tanpa menyimpan perubahan dan formula tidak dihitung atau diganti dengan cached result.

Unggahan ditolak jika ekstensi/struktur XLSX tidak valid, file rusak/terenkripsi, ZIP/XML mencurigakan, atau batas keamanan paket terlampaui. Fitur ini tidak melakukan mapping, normalisasi, database access, atau impor.

## Layout Detector & Normalizer (Stage 4.2.3)

Pada halaman detail workbook GRN, pilih **Analisis kandidat RI** untuk memeriksa kandidat header/detil, confidence, bukti label/posisi/style/merged range, metadata halaman, baris unresolved, serta anomali HOLD. Setiap field kandidat membawa source locator yang memakai ID upload aktual dan tautan ke worksheet preview pada baris fisiknya.

Detector hanya membuat kandidat: nomor RI berulang tidak digabung, footer halaman tidak otomatis memulai dokumen baru, baris setelah footer tanpa header tidak mewarisi dokumen sebelumnya, baris kuantitas saja tetap unresolved, dan satuan kosong tetap NULL/HOLD. Nilai raw dipertahankan; normalisasi kode hanya memastikan representasi teks, sementara tipe dan nilai tanggal/kuantitas dipertahankan. Status hasil selalu `REVIEW_REQUIRED`; fitur ini bukan mapping final, database access, atau import.

Ringkasan metode, hasil pembacaan read-only, fixture, validasi, dan risiko Stage 4.2.3 tersedia di [laporan audit Stage 4.2.3](docs-migrate/audit/stage-4-2-3-layout-detector-normalizer.md).

## Mapping Engine & Validation (Stage 4.2.4)

Buka **Mapping & validation** dari dashboard untuk meninjau kandidat mapping hasil detector RI. Definisi yang belum disimpan berstatus `REVIEW_REQUIRED`; target entity/field tetap placeholder sampai schema target resmi disetujui. Profil perubahan reviewer disimpan sebagai JSON lokal di `data/mappings/`, terpisah dari metadata upload dan tanpa koneksi database. Profil terikat pada upload ID dan SHA-256 sumber.

Validasi memeriksa field target yang dikonfigurasi sebagai required, tipe target bila dipilih, nilai kosong, kandidat mapping ganda dengan locator/field yang sama, referensi hanya terhadap daftar lokal yang diberikan reviewer, serta mapping yang belum terselesaikan. Hasil HOLD/errors tidak mengubah status mapping. Transformation rule hanya dicatat dan ditampilkan—tidak dijalankan. Tidak ada deduplikasi data transaksi atau penautan otomatis PO–RI.

Detail arsitektur, batas, test, dan keputusan yang masih terbuka tersedia di [laporan Stage 4.2.4](docs-migrate/audit/stage-4-2-4-mapping-engine-validation.md).

## Preview & Dry-Run (Stage 4.2.5)

Buka **Preview & dry-run** dari dashboard untuk mengevaluasi kandidat RI Stage 4.2.3 menggunakan mapping profile lokal Stage 4.2.4. Halaman menampilkan workbook dan SHA-256, ringkasan valid/warning/error/HOLD, kandidat berpaginasi dengan filter status, raw source value dan locator, serta kelompok payload simulasi berdasarkan target entity placeholder. Laporan audit lengkap tersedia sebagai JSON read-only.

Dry-run tidak menjalankan SQL, membuka koneksi database, menjalankan migrasi, menulis workbook, mengeksekusi transformation rule, atau mengubah status mapping. Mapping yang belum berstatus `APPROVED` tidak diperlakukan sebagai approved dan kandidat tetap HOLD. Relasi PO–RI tetap `UNKNOWN/HOLD` karena keputusan `REL-01` belum memiliki bukti/approval. Status VALID dari evaluasi lokal bukan bukti data siap diimpor atau persetujuan schema target.

Detail arsitektur, implementasi, hasil test, dan UNKNOWN tersedia di [laporan Stage 4.2.5](docs-migrate/audit/stage-4-2-5-preview-dry-run.md).

## Master Data Mapping (Stage 4.4.3)

Buka **Master data mapping** dari dashboard untuk meninjau atribut pemasok, barang, dan satuan yang ditemukan pada workbook PR/GRN lokal. Tabel kandidat memuat nilai raw, nama/identitas workbook, SHA-256, locator worksheet/cell, fingerprint per occurrence, target kandidat dari snapshot historis (jika ada), confidence, dan concern kualitas. Filter mendukung entitas dan status; daftar dipaginasi dan tertaut ke preview worksheet.

Halaman ini hanya menghasilkan candidate crosswalk lokal. Status awal selalu `REVIEW_REQUIRED`, target ID tidak dibuat, blank tidak diberi default, nilai berulang tidak digabung, dan transformasi tidak dijalankan. `db_solog_oli_initial` serta snapshot schema historis bukan target terverifikasi; status schema target tetap UNKNOWN. Relasi belum memiliki crosswalk/FK yang disetujui dan ditampilkan sebagai UNKNOWN. Tidak ada koneksi database, query SQL, perubahan workbook, approval, atau Import Executor.

Temuan dan batas cakupan dirangkum di [laporan Stage 4.4.3](docs/stage-4-4-3-master-data-mapping.md).

## Konfigurasi Target Database (Stage 4.4.1)

Buka **Target database** dari dashboard untuk membuat dan mengelola profil TARGET. Profil hanya menyimpan label, environment, host, port, nama database, username, dan purpose `TARGET` sebagai metadata lokal di `data/target-databases.json`. Tidak ada profil yang dipilih otomatis; menghapus profil terpilih juga mengosongkan pilihan tanpa memilih profil lain.

Password dapat dimasukkan pada form bertipe password, tetapi hanya diterima sementara selama request dan tidak ditampilkan kembali atau disimpan. Masukkan ulang saat verifikasi. Identitas database referensi `db_solog_oli_initial` pada host yang dikenal dan port 3306 ditolak oleh konfigurasi; endpoint verifikasi juga menolak nama database referensi sebelum percobaan koneksi. Lihat [laporan Stage 4.4.1](reports/stage-4-4-1-target-database-configuration.md).

## Koneksi & Verifikasi Schema (Stage 4.4.2)

Buka **Koneksi & schema** dari dashboard atau `/target-databases/verify`. Hanya profil TARGET yang sudah dipilih eksplisit yang dapat diverifikasi. Halaman menampilkan identitas lengkap; POST memerlukan password ulang, token snapshot profil yang ditandatangani dan berumur terbatas, konfirmasi pengguna, serta konfirmasi teks tambahan jika environment `Production`.

Konektor MySQL/MariaDB memakai timeout. Setelah nama database, port, dan account cocok dengan profil serta hostname server berhasil dibaca, layanan membaca `SHOW GRANTS`; metadata schema hanya dikumpulkan jika grants dapat dibuktikan sebagai `SELECT` (opsional `SHOW VIEW`) yang terbatas pada database target. Hostname yang dilaporkan server ditampilkan sebagai bukti observasi; tidak ada hostname baseline otoritatif untuk dibandingkan. Hak tulis, grant yang lebih luas, role/grant yang tidak dapat dianalisis, mismatch identitas, atau kegagalan verifikasi memblokir pengumpulan schema. Query berikutnya hanya membaca `INFORMATION_SCHEMA`; data bisnis tidak dibaca. Password tidak disimpan/log/ditampilkan. Hasil metadata hanya berada sementara di memori proses dan diikat ke fingerprint profil.

Tidak ada baseline schema target yang otoritatif dan disetujui. Karena itu hasil sukses selalu mencakup `SCHEMA_BASELINE_UNAVAILABLE` dan `SCHEMA_REVIEW_REQUIRED`, bukan status kompatibilitas atau kesiapan impor. Implementasi Stage 4.4.2 dan batasnya dicatat di [dokumentasi Stage 4.4.2](docs/stage-4-4-2-connection-schema-verification.md).

## Security, Tests & Final Review (Stage 4.2.6)

Permintaan POST upload dan perubahan profil mapping wajib membawa token CSRF yang cocok dengan cookie host-only `SameSite=Strict`, serta Origin/Referer same-origin. Aplikasi hanya menerima `Host` `localhost`, `127.0.0.1`, atau `[::1]`. Response menggunakan CSP, `nosniff`, frame denial, `no-store`, Referrer-Policy, dan header pembatas browser lainnya. Validasi ini tidak menyediakan autentikasi dan tidak membuat aplikasi aman untuk akses jaringan.

Audit dependensi tidak melakukan upgrade otomatis. `pip check` memeriksa konsistensi dependensi yang terpasang, bukan audit CVE; jalankan pemindai advisory yang disetujui di lingkungan terkontrol sebelum rilis. Laporan review, cakupan kontrol, hasil test, serta keterbatasan tersedia di [laporan Stage 4.2.6](docs-migrate/audit/stage-4-2-6-security-tests-final-review.md).

## Menjalankan test

```powershell
python -m pytest
```

Test memakai workbook dummy sintetis dan FastAPI TestClient; tidak mengakses database atau workbook sumber dalam `docs-migrate/`.

## Struktur saat ini dan ekstensi mendatang

`app/` memuat entry point, config, logging, router health, workbook, mapping, dry-run, dan konfigurasi target, service lokal, model Pydantic, template Jinja2, dan static CSS. `tests/` mencakup endpoint dan workbook sintetis. Transformation Engine, Master Resolver, dan Reconciliation tetap untuk tahap berikutnya setelah mapping/aturan disetujui. Import Executor secara eksplisit belum dibuat.

## Keputusan teknis yang belum ditentukan

- Versi Python/runtime final dan strategi environment deployment lokal.
- Sumber/hosting HTMX untuk penggunaan offline (fitur upload memakai HTMX dari CDN; form tetap dapat dikirim tanpa HTMX).
- Autentikasi lokal, kontrol akses, retensi, dan proteksi operasional sebelum penggunaan multi-user/jaringan; CSRF dan host allowlist tidak menggantikan kontrol tersebut.
- Audit CVE dependency terotomasi dan proses pembaruan advisori terverifikasi.
- Crosswalk dan batch state store belum dibuat; metadata upload saja disimpan sebagai JSON lokal, tanpa database.
- Mekanisme secret storage jangka panjang belum dipilih. Stage 4.4.2 hanya menerima password per-request dan tidak menyimpannya; verifikasi privilege, schema version/baseline, backup, dan rollback tidak menyetujui proses impor.
- Format mapping JSON final serta approval workflow.
- Kebijakan logging dan perlindungan data workbook untuk penggunaan multi-user/jaringan.

Semua keputusan bisnis dan mapping tetap tunduk pada dokumen Stage 3.2 dan Stage 4.1 di repository Solog OLI.
