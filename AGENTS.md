# Pedoman Migrasi Database

**Tanggal pembaruan:** 3 November 2026  
**Cakupan:** Seluruh pekerjaan migrasi data dari aplikasi lama ke aplikasi baru di proyek ini.

## 1. Tujuan dan prinsip

Migrasi bertujuan memindahkan data historis dari aplikasi lama yang tidak lagi digunakan ke aplikasi baru dengan menjaga integritas historis, konsistensi struktur, ketepatan relasi antartabel, konsistensi mapping, keamanan, serta kemampuan validasi dan audit.

Berkas sumber dan dokumentasi migrasi proyek berada di `docs-migrate`. Mulai setiap pekerjaan migrasi dengan membaca `docs-migrate/README.md` dan dokumen yang relevan dengan tugas. Dokumentasi migrasi adalah referensi utama. Jangan menganggap struktur sumber sama dengan struktur tujuan atau menyimpulkan isi berkas yang belum diperiksa.

## 2. Analisis dan bukti

- Bedakan dengan jelas fakta yang didukung bukti, asumsi sementara, rekomendasi, dan hal yang belum diketahui.
- Gunakan status **VERIFIED** untuk informasi yang telah dikonfirmasi dengan sumber yang disebutkan, **ASSUMED** untuk asumsi yang masih menunggu konfirmasi, dan **UNKNOWN** untuk informasi yang belum diketahui atau belum memiliki bukti cukup.
- Jangan mengarang struktur, makna kolom, relasi, aturan transformasi, atau keputusan mapping. Jangan menetapkan mapping tanpa bukti memadai.
- Catat sumber bukti untuk setiap temuan penting, termasuk nama dokumen/berkas dan lokasi yang cukup spesifik untuk ditinjau ulang.
- Bila informasi tidak tersedia atau sumber saling bertentangan, tandai **UNKNOWN**, jelaskan konflik atau kekurangannya, dan minta klarifikasi/review sebelum mengambil keputusan.
- Jangan mengubah keputusan mapping yang telah disetujui tanpa mencatat alasan, dampak, bukti, dan persetujuan perubahan.

## 3. Keamanan dan perlindungan data

- Audit database bersifat **READ-ONLY**. Batasi audit pada query baca dan akses yang diperlukan.
- Jangan mengubah berkas sumber asli. Perlakukan berkas sumber, termasuk CSV, sebagai data asli yang tidak boleh diedit. Simpan hasil olahan pada berkas turunan yang terpisah dan beri nama/lokasi yang jelas.
- Jangan menjalankan query atau skrip yang mengubah database tanpa persetujuan eksplisit untuk tindakan dan lingkungan yang dimaksud.
- Dilarang menjalankan `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, atau `TRUNCATE` pada database production.
- Jangan membaca, menyalin, mencatat, atau menampilkan kredensial database dalam laporan, dokumentasi, log, atau keluaran perintah. Rahasiakan nilai rahasia dari berkas konfigurasi dan variabel lingkungan.
- Pengujian migrasi wajib menggunakan database staging yang terpisah dari production.
- Sebelum migrasi production, pastikan backup tersedia dan dapat diidentifikasi. Migrasi production hanya boleh dilakukan setelah persetujuan eksplisit.
- Jika lingkungan, target, izin, atau status backup tidak jelas, hentikan tindakan yang dapat mengubah data dan tandai hal tersebut sebagai **UNKNOWN**.

## 4. Dokumentasi dan format berkas

Gunakan Markdown (`.md`) untuk dokumentasi proyek, audit, analisis struktur, perbandingan schema, aturan mapping, rencana migrasi, serta hasil validasi. Gunakan JSON (`.json`) bila aturan mapping, transformasi, atau konfigurasi migrasi perlu disimpan dalam format terstruktur. CSV dapat menjadi sumber data asli; jangan mengubah isi sumbernya.

Dokumentasi harus:

- Ditulis dalam bahasa Indonesia dengan judul dan susunan bagian yang jelas.
- Mencantumkan tanggal pembaruan.
- Menandai temuan menggunakan **VERIFIED**, **ASSUMED**, atau **UNKNOWN** sesuai bukti.
- Menyebutkan sumber bukti dan cakupan pemeriksaan yang diperlukan untuk audit ulang.
- Merujuk dokumen yang sudah ada alih-alih menggandakan isinya. Perbarui dokumen yang tepat bila memang diminta dan sesuai cakupan.

## 5. Persyaratan Migration Data Dictionary dan mapping

Migration Data Dictionary adalah referensi utama seluruh aturan transformasi data. Jika tersedia, semua analisis dan proses migrasi wajib mengacu padanya. Jangan membuat aturan yang bertentangan atau mengambil keputusan sepihak ketika menemukan konflik atau perubahan struktur; dokumentasikan konflik dan laporkan untuk review terlebih dahulu.

Setiap mapping wajib mencatat:

1. Tabel sumber dan kolom sumber.
2. Tabel tujuan dan kolom tujuan.
3. Aturan transformasi, termasuk konversi tipe atau normalisasi bila ada.
4. Penanganan nilai `NULL` dan nilai kosong.
5. Penanganan data duplikat.
6. Penanganan primary key, termasuk strategi nilai/identitas dan konflik.
7. Penanganan foreign key dan relasi yang tidak terpenuhi.
8. Status verifikasi (**VERIFIED**, **ASSUMED**, atau **UNKNOWN**) beserta bukti dan reviewer/persetujuan bila berlaku.

Tandai setiap unsur yang belum diketahui sebagai **UNKNOWN**. Mapping belum siap untuk migrasi sampai informasi wajib dan keputusan yang memerlukan persetujuan telah ditinjau dan disetujui.

## 6. Tahapan kerja dan gerbang persetujuan

Ikuti urutan berikut dan jangan melewati tahapan atau gerbang persetujuan:

1. Persiapan dokumentasi.
2. Audit database lama.
3. Audit database baru.
4. Perbandingan struktur database.
5. Analisis kualitas data.
6. Penyusunan Migration Data Dictionary.
7. Review dan persetujuan mapping.
8. Penyusunan migration plan.
9. Pembuatan migration script.
10. Pengujian di staging.
11. Validasi hasil migrasi.
12. Migrasi production setelah memperoleh persetujuan eksplisit dan memastikan backup tersedia.

Selesaikan dan dokumentasikan hasil setiap tahap sebelum lanjut. Minta persetujuan sebelum melewati gerbang review mapping, menjalankan perubahan database, memulai migrasi production, atau ketika sumber dan dokumentasi bertentangan. Persetujuan untuk satu lingkungan atau tindakan tidak berlaku otomatis untuk lingkungan atau tindakan lainnya.

## 7. Efisiensi pemeriksaan

- Baca hanya berkas yang relevan dengan tugas aktif dan jangan membaca ulang seluruh berkas besar tanpa kebutuhan.
- Gunakan skrip untuk menganalisis CSV berukuran besar; dokumentasikan metode, cakupan, dan ringkasan hasilnya.
- Gunakan ringkasan analisis untuk dokumentasi. Jangan memasukkan seluruh isi CSV ke prompt atau laporan.
- Hindari menghasilkan dokumentasi yang menduplikasi sumber yang sudah tersedia.

## 8. Pelaporan pekerjaan

Setiap laporan pekerjaan harus mencakup:

- Aktivitas yang dilakukan dan cakupannya.
- Berkas yang dibuat atau diubah.
- Temuan penting beserta status dan sumber buktinya.
- Masalah, konflik, atau risiko yang ditemukan.
- Informasi yang masih **UNKNOWN** atau **ASSUMED**.
- Rekomendasi dan langkah selanjutnya, termasuk gerbang persetujuan yang masih diperlukan.

Jangan menyatakan audit, validasi, persetujuan, backup, atau migrasi berhasil kecuali ada bukti yang mendukungnya.