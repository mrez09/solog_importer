# Audit Database Target

**Tanggal audit:** 3 November 2026  
**Status:** VERIFIED untuk koneksi, metadata, dan jumlah baris pada saat audit.  
**Target terverifikasi:** `db_solog_oli_initial` (driver `mysql`; identitas dikonfirmasi dengan `SELECT DATABASE()`).

## Metode dan cakupan

Audit dilakukan READ-ONLY menggunakan metadata `INFORMATION_SCHEMA` dan `SELECT COUNT(*)` pada setiap tabel. Tidak ada query perubahan. Kolom memuat tipe/panjang, NULL, default, primary key, dan auto increment; indeks/unique serta foreign key dicantumkan per tabel. Nilai baris tidak dibaca atau dicatat. View didata dari metadata dan tidak dihitung sebagai tabel data.

## Ringkasan

- Tabel: **359**.
- View: **18**.
- Total baris tabel: **2.376**.
- Tabel kosong: **306 dari 359**.
- Tabel berisi baris: **53 dari 359**.
- Database kosong: **Tidak**. Sejumlah data konfigurasi/master dan tabel aplikasi ditemukan; lihat jumlah per tabel di bawah.
- Engine/row estimate dari `INFORMATION_SCHEMA.TABLES` tidak dipakai sebagai jumlah pasti; hitungan memakai `COUNT(*)`.

## Inventaris tabel dan schema

### `accounts` — 8 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `deep` | `int(11)` | NO | `1` | — | — |
| `parent_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_base` | `tinyint(1)` | NO | `0` | — | — |
| `jenis` | `int(11)` | YES | `1` | — | — |
| `group_report` | `int(11)` | NO | `1` | — | — |
| `type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `no_cash_bank` | `int(11)` | YES | `0` | — | — |
| `is_freeze` | `tinyint(1)` | NO | `0` | — | — |
| `company_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_usd` | `tinyint(1)` | NO | `0` | — | — |
| `is_cash_count` | `smallint(6)` | NO | `0` | MUL | — |

**Indeks:** accounts_company_id_foreign: company_id; accounts_is_cash_count_index: is_cash_count; accounts_parent_id_foreign: parent_id; accounts_type_foreign: type_id; PRIMARY (UNIQUE): id.  
**Foreign key:** accounts_company_id_foreign (company_id → companies.id); accounts_parent_id_foreign (parent_id → accounts.id); accounts_type_foreign (type_id → account_types.id).

### `account_defaults` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `biaya_klaim` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cek_giro_keluar` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cek_giro_masuk` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `diskon_penjualan` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `hutang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `hutang_klaim` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `laba_bulan_berjalan` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `laba_ditahan` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `laba_tahun_berjalan` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `lebih_bayar_hutang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `lebih_bayar_piutang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `pendapatan_klaim` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `penjualan` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `piutang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `ppn_in` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `ppn_out` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `saldo_awal` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `account_kasbon_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `inventory` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `perawatan` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `bukti_potong` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `bukti_potong_hutang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `pendapatan_hibah` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `pendapatan_reimburse` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `piutang_reimburse` | `int(10) unsigned` | YES | `NULL` | — | — |
| `pembelian` | `int(10) unsigned` | YES | `NULL` | — | — |
| `retur_barang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_cash` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `selisih_timbang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `deposit_customer` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `deposit_vendor` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `persediaan` | `int(10) unsigned` | YES | `NULL` | — | — |
| `hutang_belum_tertagih` | `int(10) unsigned` | YES | `NULL` | — | — |
| `item_usage` | `int(11)` | YES | `NULL` | — | — |
| `penjualan_sementara` | `int(11)` | YES | `NULL` | — | — |
| `pendapatan` | `int(11)` | YES | `NULL` | — | — |
| `hutang_pph` | `int(11)` | YES | `NULL` | — | — |
| `hutang_ppn` | `int(11)` | YES | `NULL` | — | — |
| `biaya_penghapusan_asset_tidak_tetap` | `int(11)` | YES | `NULL` | — | — |
| `asset_tidak_tetap` | `int(11)` | YES | `NULL` | — | — |
| `depresiasi_asset_tidak_tetap` | `int(11)` | YES | `NULL` | — | — |
| `biaya_vulkanisir` | `int(11)` | YES | `NULL` | — | — |
| `piutang_sementara` | `int(11)` | YES | `NULL` | — | — |
| `hpp` | `int(11)` | YES | `NULL` | — | — |

**Indeks:** account_defaults_account_cash_foreign: account_cash; account_defaults_account_kasbon_id_foreign: account_kasbon_id; account_defaults_biaya_klaim_foreign: biaya_klaim; account_defaults_bukti_potong_foreign: bukti_potong; account_defaults_bukti_potong_hutang_foreign: bukti_potong_hutang; account_defaults_cek_giro_keluar_foreign: cek_giro_keluar; account_defaults_cek_giro_masuk_foreign: cek_giro_masuk; account_defaults_deposit_customer_foreign: deposit_customer; account_defaults_deposit_vendor_foreign: deposit_vendor; account_defaults_diskon_penjualan_foreign: diskon_penjualan; account_defaults_hutang_foreign: hutang; account_defaults_hutang_klaim_foreign: hutang_klaim; account_defaults_inventory_foreign: inventory; account_defaults_laba_bulan_berjalan_foreign: laba_bulan_berjalan; account_defaults_laba_ditahan_foreign: laba_ditahan; account_defaults_laba_tahun_berjalan_foreign: laba_tahun_berjalan; account_defaults_lebih_bayar_hutang_foreign: lebih_bayar_hutang; account_defaults_lebih_bayar_piutang_foreign: lebih_bayar_piutang; account_defaults_pendapatan_hibah_foreign: pendapatan_hibah; account_defaults_pendapatan_klaim_foreign: pendapatan_klaim; account_defaults_pendapatan_reimburse_foreign: pendapatan_reimburse; account_defaults_penjualan_foreign: penjualan; account_defaults_perawatan_foreign: perawatan; account_defaults_piutang_foreign: piutang; account_defaults_ppn_in_foreign: ppn_in; account_defaults_ppn_out_foreign: ppn_out; account_defaults_retur_barang_foreign: retur_barang; account_defaults_saldo_awal_foreign: saldo_awal; account_defaults_selisih_timbang_foreign: selisih_timbang; PRIMARY (UNIQUE): id.  
**Foreign key:** account_defaults_account_cash_foreign (account_cash → accounts.id); account_defaults_account_kasbon_id_foreign (account_kasbon_id → accounts.id); account_defaults_biaya_klaim_foreign (biaya_klaim → accounts.id); account_defaults_bukti_potong_foreign (bukti_potong → accounts.id); account_defaults_bukti_potong_hutang_foreign (bukti_potong_hutang → accounts.id); account_defaults_cek_giro_keluar_foreign (cek_giro_keluar → accounts.id); account_defaults_cek_giro_masuk_foreign (cek_giro_masuk → accounts.id); account_defaults_deposit_customer_foreign (deposit_customer → accounts.id); account_defaults_deposit_vendor_foreign (deposit_vendor → accounts.id); account_defaults_diskon_penjualan_foreign (diskon_penjualan → accounts.id); account_defaults_hutang_foreign (hutang → accounts.id); account_defaults_hutang_klaim_foreign (hutang_klaim → accounts.id); account_defaults_inventory_foreign (inventory → accounts.id); account_defaults_laba_bulan_berjalan_foreign (laba_bulan_berjalan → accounts.id); account_defaults_laba_ditahan_foreign (laba_ditahan → accounts.id); account_defaults_laba_tahun_berjalan_foreign (laba_tahun_berjalan → accounts.id); account_defaults_lebih_bayar_hutang_foreign (lebih_bayar_hutang → accounts.id); account_defaults_lebih_bayar_piutang_foreign (lebih_bayar_piutang → accounts.id); account_defaults_pendapatan_hibah_foreign (pendapatan_hibah → accounts.id); account_defaults_pendapatan_klaim_foreign (pendapatan_klaim → accounts.id); account_defaults_pendapatan_reimburse_foreign (pendapatan_reimburse → accounts.id); account_defaults_penjualan_foreign (penjualan → accounts.id); account_defaults_perawatan_foreign (perawatan → accounts.id); account_defaults_piutang_foreign (piutang → accounts.id); account_defaults_ppn_in_foreign (ppn_in → accounts.id); account_defaults_ppn_out_foreign (ppn_out → accounts.id); account_defaults_retur_barang_foreign (retur_barang → accounts.id); account_defaults_saldo_awal_foreign (saldo_awal → accounts.id); account_defaults_selisih_timbang_foreign (selisih_timbang → accounts.id).

### `account_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_payable` | `int(11)` | NO | `0` | MUL | — |

**Indeks:** account_types_is_payable_index: is_payable; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `additional_fields` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(30)` | NO | `—` | — | — |
| `field_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `show_in_job_order_summary` | `smallint(6)` | NO | `0` | MUL | — |
| `slug` | `varchar(100)` | YES | `NULL` | — | — |
| `show_in_operational_progress` | `smallint(6)` | NO | `0` | MUL | — |
| `show_in_manifest` | `smallint(6)` | NO | `0` | — | — |
| `show_in_index` | `smallint(6)` | NO | `0` | — | — |

**Indeks:** additional_fields_field_type_id_index: field_type_id; additional_fields_id_unique (UNIQUE): id; additional_fields_show_in_job_order_summary_index: show_in_job_order_summary; additional_fields_show_in_operational_progress_index: show_in_operational_progress; additional_fields_type_transaction_id_index: type_transaction_id; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `address_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `air_ports` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `island_name` | `varchar(191)` | NO | `—` | — | — |
| `latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `areas` — 1 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `assets` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `asset_group_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `asset_type` | `int(11)` | NO | `—` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_purchase` | `date` | NO | `—` | — | — |
| `purchase_price` | `double(20,2)` | NO | `0.00` | — | — |
| `residu_price` | `double(20,2)` | NO | `0.00` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `umur_ekonomis` | `double(20,2)` | NO | `0.00` | — | — |
| `method` | `int(11)` | NO | `1` | — | — |
| `account_asset_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_accumulation_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_depreciation_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `is_afkir` | `tinyint(1)` | NO | `0` | — | — |
| `is_revaluasi` | `tinyint(1)` | NO | `0` | — | — |
| `is_saldo` | `tinyint(1)` | NO | `0` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `beban_tahun` | `double(20,2)` | NO | `0.00` | — | — |
| `beban_bulan` | `double(20,2)` | NO | `0.00` | — | — |
| `beban_akumulasi` | `double(20,2)` | NO | `0.00` | — | — |
| `nilai_buku` | `double(20,2)` | NO | `0.00` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `terhitung_tanggal` | `date` | YES | `NULL` | — | — |

**Indeks:** assets_account_accumulation_id_foreign: account_accumulation_id; assets_account_asset_id_foreign: account_asset_id; assets_account_depreciation_id_foreign: account_depreciation_id; assets_asset_group_id_foreign: asset_group_id; assets_company_id_foreign: company_id; assets_create_by_foreign: create_by; assets_journal_id_foreign: journal_id; assets_vehicle_id_foreign: vehicle_id; PRIMARY (UNIQUE): id.  
**Foreign key:** assets_account_accumulation_id_foreign (account_accumulation_id → accounts.id); assets_account_asset_id_foreign (account_asset_id → accounts.id); assets_account_depreciation_id_foreign (account_depreciation_id → accounts.id); assets_asset_group_id_foreign (asset_group_id → asset_groups.id); assets_company_id_foreign (company_id → companies.id); assets_create_by_foreign (create_by → users.id); assets_journal_id_foreign (journal_id → journals.id); assets_vehicle_id_foreign (vehicle_id → vehicles.id).

### `asset_afkirs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `asset_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_loss_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `approve_date` | `date` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `loss_amount` | `double(20,2)` | NO | `0.00` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** asset_afkirs_account_loss_id_foreign: account_loss_id; asset_afkirs_approve_by_foreign: approve_by; asset_afkirs_asset_id_foreign: asset_id; asset_afkirs_company_id_foreign: company_id; asset_afkirs_create_by_foreign: create_by; asset_afkirs_journal_id_foreign: journal_id; PRIMARY (UNIQUE): id.  
**Foreign key:** asset_afkirs_account_loss_id_foreign (account_loss_id → accounts.id); asset_afkirs_approve_by_foreign (approve_by → users.id); asset_afkirs_asset_id_foreign (asset_id → assets.id); asset_afkirs_company_id_foreign (company_id → companies.id); asset_afkirs_create_by_foreign (create_by → users.id); asset_afkirs_journal_id_foreign (journal_id → journals.id).

### `asset_depreciations` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `date_utility` | `date` | NO | `—` | — | — |
| `depreciation_cost` | `double(20,2)` | NO | `0.00` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** asset_depreciations_approve_by_foreign: approve_by; asset_depreciations_header_id_foreign: header_id; asset_depreciations_journal_id_foreign: journal_id; PRIMARY (UNIQUE): id.  
**Foreign key:** asset_depreciations_approve_by_foreign (approve_by → users.id); asset_depreciations_header_id_foreign (header_id → assets.id); asset_depreciations_journal_id_foreign (journal_id → journals.id).

### `asset_groups` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `umur_ekonomis` | `double(20,2)` | NO | `0.00` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `method` | `int(11)` | NO | `1` | — | — |
| `account_asset_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_accumulation_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_depreciation_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** asset_groups_account_accumulation_id_foreign: account_accumulation_id; asset_groups_account_asset_id_foreign: account_asset_id; asset_groups_account_depreciation_id_foreign: account_depreciation_id; PRIMARY (UNIQUE): id.  
**Foreign key:** asset_groups_account_accumulation_id_foreign (account_accumulation_id → accounts.id); asset_groups_account_asset_id_foreign (account_asset_id → accounts.id); asset_groups_account_depreciation_id_foreign (account_depreciation_id → accounts.id).

### `asset_purchases` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `supplier_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `termin` | `int(11)` | NO | `—` | — | — |
| `tempo` | `int(11)` | YES | `NULL` | — | — |
| `cash_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `total_price` | `double(20,2)` | NO | `0.00` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** asset_purchases_approve_by_foreign: approve_by; asset_purchases_cash_account_id_foreign: cash_account_id; asset_purchases_company_id_foreign: company_id; asset_purchases_create_by_foreign: create_by; asset_purchases_journal_id_foreign: journal_id; asset_purchases_supplier_id_foreign: supplier_id; PRIMARY (UNIQUE): id.  
**Foreign key:** asset_purchases_approve_by_foreign (approve_by → users.id); asset_purchases_cash_account_id_foreign (cash_account_id → accounts.id); asset_purchases_company_id_foreign (company_id → companies.id); asset_purchases_create_by_foreign (create_by → users.id); asset_purchases_journal_id_foreign (journal_id → journals.id); asset_purchases_supplier_id_foreign (supplier_id → contacts.id).

### `asset_purchase_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `asset_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `price` | `double(20,2)` | NO | `0.00` | — | — |
| `residu` | `double(20,2)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** asset_purchase_details_asset_id_foreign: asset_id; asset_purchase_details_header_id_foreign: header_id; PRIMARY (UNIQUE): id.  
**Foreign key:** asset_purchase_details_asset_id_foreign (asset_id → assets.id); asset_purchase_details_header_id_foreign (header_id → asset_purchases.id).

### `asset_sales` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `costumer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `termin` | `int(11)` | NO | `—` | — | — |
| `tempo` | `int(11)` | YES | `NULL` | — | — |
| `cash_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `sales_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `total_price` | `double(20,2)` | NO | `0.00` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** asset_sales_approve_by_foreign: approve_by; asset_sales_cash_account_id_foreign: cash_account_id; asset_sales_company_id_foreign: company_id; asset_sales_costumer_id_foreign: costumer_id; asset_sales_create_by_foreign: create_by; asset_sales_journal_id_foreign: journal_id; asset_sales_sales_account_id_foreign: sales_account_id; PRIMARY (UNIQUE): id.  
**Foreign key:** asset_sales_approve_by_foreign (approve_by → users.id); asset_sales_cash_account_id_foreign (cash_account_id → accounts.id); asset_sales_company_id_foreign (company_id → companies.id); asset_sales_costumer_id_foreign (costumer_id → contacts.id); asset_sales_create_by_foreign (create_by → users.id); asset_sales_journal_id_foreign (journal_id → journals.id); asset_sales_sales_account_id_foreign (sales_account_id → accounts.id).

### `asset_sales_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `asset_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `price` | `double(20,2)` | NO | `0.00` | — | — |
| `nilai_buku` | `double(20,2)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** asset_sales_details_asset_id_foreign: asset_id; asset_sales_details_header_id_foreign: header_id; PRIMARY (UNIQUE): id.  
**Foreign key:** asset_sales_details_asset_id_foreign (asset_id → assets.id); asset_sales_details_header_id_foreign (header_id → asset_sales.id).

### `banks` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `bbm_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `bills` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_request` | `date` | NO | `—` | — | — |
| `date_cancel` | `date` | YES | `NULL` | — | — |
| `cancel_description` | `text` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `code_receive` | `varchar(191)` | YES | `NULL` | — | — |
| `date_receive` | `date` | YES | `NULL` | — | — |
| `description_receive` | `text` | YES | `NULL` | — | — |
| `paid` | `double` | NO | `0` | — | — |
| `overpayment` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `pi_due_date` | `date` | NO | `—` | — | — |
| `pi_print_count` | `int(11)` | NO | `0` | — | — |
| `date_created` | `date` | YES | `NULL` | — | — |
| `employee_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `pengajuan_print_count` | `int(11)` | YES | `NULL` | — | — |

**Indeks:** bills_cancel_by_foreign: cancel_by; bills_company_id_foreign: company_id; bills_create_by_foreign: create_by; bills_customer_id_foreign: customer_id; bills_journal_id_foreign: journal_id; PRIMARY (UNIQUE): id.  
**Foreign key:** bills_cancel_by_foreign (cancel_by → users.id); bills_company_id_foreign (company_id → companies.id); bills_create_by_foreign (create_by → users.id); bills_customer_id_foreign (customer_id → contacts.id); bills_journal_id_foreign (journal_id → journals.id).

### `bill_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `receivable_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `type_transaction_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `bill` | `double` | NO | `0` | — | — |
| `leftover` | `double` | NO | `0` | — | — |
| `total_bill` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `receivable_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `um_customer_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `nota_credit_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `nota_debet_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `jenis` | `int(11)` | NO | `1` | — | — |
| `pi_lampiran` | `varchar(191)` | NO | `—` | — | — |
| `pi_kapal` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `bill_files` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `bill_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(200)` | NO | `—` | MUL | — |
| `filename` | `text` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** bill_files_bill_id_index: bill_id; bill_files_name_index: name; PRIMARY (UNIQUE): id.  
**Foreign key:** bill_files_bill_id_foreign (bill_id → bills.id).

### `bill_payments` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `payment_type` | `int(11)` | NO | `1` | — | — |
| `reff` | `varchar(191)` | YES | `NULL` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `cash_account_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cek_giro_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `filename` | `varchar(100)` | NO | `—` | — | — |
| `valid` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `booking_car` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicles_id` | `int(10) unsigned` | NO | `—` | — | — |
| `contacts_id` | `int(10) unsigned` | NO | `—` | — | — |
| `name` | `varchar(255)` | NO | `—` | — | — |
| `division` | `enum('Marketing','Operasional')` | NO | `'Marketing'` | — | — |
| `booking_date` | `date` | NO | `—` | — | — |
| `booking_time` | `time` | NO | `—` | — | — |
| `return_date` | `date` | NO | `—` | — | — |
| `route` | `varchar(255)` | NO | `—` | — | — |
| `active` | `int(10) unsigned` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `budgets` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(50)` | NO | `—` | UNI | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `month` | `int(11)` | NO | `—` | — | — |
| `year` | `int(11)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `total_amount` | `decimal(15,2)` | NO | `0.00` | — | — |
| `status` | `tinyint(4)` | NO | `1` | MUL | — |
| `approved_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approved_at` | `timestamp` | YES | `NULL` | — | — |
| `rejected_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `rejected_at` | `timestamp` | YES | `NULL` | — | — |
| `rejected_reason` | `text` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** budgets_approved_by_foreign: approved_by; budgets_code_unique (UNIQUE): code; budgets_company_id_month_year_index: company_id, month, year; budgets_created_by_foreign: created_by; budgets_rejected_by_foreign: rejected_by; budgets_status_index: status; PRIMARY (UNIQUE): id.  
**Foreign key:** budgets_approved_by_foreign (approved_by → users.id); budgets_company_id_foreign (company_id → companies.id); budgets_created_by_foreign (created_by → users.id); budgets_rejected_by_foreign (rejected_by → users.id).

### `budget_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `amount` | `decimal(15,2)` | NO | `0.00` | — | — |
| `notes` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** budget_details_account_id_foreign: account_id; budget_details_header_id_foreign: header_id; PRIMARY (UNIQUE): id.  
**Foreign key:** budget_details_account_id_foreign (account_id → accounts.id); budget_details_header_id_foreign (header_id → budgets.id).

### `budget_files` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `file_path` | `varchar(255)` | NO | `—` | — | — |
| `file_name` | `varchar(255)` | NO | `—` | — | — |
| `file_type` | `varchar(50)` | YES | `NULL` | — | — |
| `file_size` | `int(11)` | YES | `NULL` | — | — |
| `mime_type` | `varchar(100)` | YES | `NULL` | — | — |
| `uploaded_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** budget_files_header_id_foreign: header_id; budget_files_uploaded_by_foreign: uploaded_by; PRIMARY (UNIQUE): id.  
**Foreign key:** budget_files_header_id_foreign (header_id → budgets.id); budget_files_uploaded_by_foreign (uploaded_by → users.id).

### `business` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `business_type` | `varchar(191)` | NO | `—` | — | — |
| `manage_shipment_type` | `varchar(191)` | NO | `—` | — | — |
| `is_land_freight` | `tinyint(1)` | NO | `0` | — | — |
| `is_sea_freight` | `tinyint(1)` | NO | `0` | — | — |
| `is_air_freight` | `tinyint(1)` | NO | `0` | — | — |
| `is_self_manage_fleet` | `tinyint(1)` | NO | `0` | — | — |
| `is_tracking_shipment` | `tinyint(1)` | NO | `0` | — | — |
| `business_name` | `varchar(191)` | NO | `—` | — | — |
| `business_address` | `varchar(255)` | NO | `—` | — | — |
| `business_email` | `varchar(255)` | NO | `—` | — | — |
| `business_phone` | `varchar(191)` | NO | `—` | — | — |
| `business_team_size` | `varchar(191)` | NO | `—` | — | — |
| `business_city_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** business_business_city_id_foreign: business_city_id; business_contact_id_foreign: contact_id; PRIMARY (UNIQUE): id.  
**Foreign key:** business_business_city_id_foreign (business_city_id → cities.id); business_contact_id_foreign (contact_id → contacts.id).

### `business_portfolios` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | UNI | — |
| `name` | `varchar(191)` | NO | `—` | UNI | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** business_portfolios_code_unique (UNIQUE): code; business_portfolios_name_unique (UNIQUE): name; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cashplan_transactions` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(100)` | NO | `—` | MUL | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `period_month` | `tinyint(4)` | NO | `—` | — | — |
| `period_year` | `year(4)` | NO | `—` | — | — |
| `opening_balance` | `decimal(15,2)` | NO | `0.00` | — | — |
| `min_cash_buffer` | `decimal(15,2)` | NO | `0.00` | — | — |
| `status` | `enum('draft','approved')` | NO | `'draft'` | MUL | — |
| `approved_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approved_at` | `datetime` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** cashplan_transactions_approved_by_index: approved_by; cashplan_transactions_code_index: code; cashplan_transactions_company_id_index: company_id; cashplan_transactions_created_by_index: created_by; cashplan_transactions_status_index: status; PRIMARY (UNIQUE): id.  
**Foreign key:** cashplan_transactions_approved_by_foreign (approved_by → users.id); cashplan_transactions_company_id_foreign (company_id → companies.id); cashplan_transactions_created_by_foreign (created_by → users.id).

### `cashplan_transaction_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `cashplan_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type` | `enum('in','out')` | NO | `—` | — | — |
| `department_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `entity_type` | `enum('contact','cost','other')` | NO | `—` | — | — |
| `contact_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cost_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** cashplan_transaction_details_account_id_index: account_id; cashplan_transaction_details_cashplan_transaction_id_index: cashplan_transaction_id; cashplan_transaction_details_contact_id_index: contact_id; cashplan_transaction_details_cost_id_index: cost_id; cashplan_transaction_details_department_id_index: department_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cashplan_transaction_details_account_id_foreign (account_id → accounts.id); cashplan_transaction_details_cashplan_transaction_id_foreign (cashplan_transaction_id → cashplan_transactions.id); cashplan_transaction_details_contact_id_foreign (contact_id → contacts.id); cashplan_transaction_details_cost_id_foreign (cost_id → cost_types.id); cashplan_transaction_details_department_id_foreign (department_id → departments.id).

### `cashplan_transaction_weeks` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `cashplan_transaction_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `week_number` | `tinyint(4)` | NO | `—` | — | — |
| `amount` | `decimal(15,2)` | NO | `0.00` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** cashplan_transaction_weeks_cashplan_transaction_detail_id_index: cashplan_transaction_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** fk_cashplan_detail_week (cashplan_transaction_detail_id → cashplan_transaction_details.id).

### `cash_advances` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `realisation_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `employee_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_cash_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_advance_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `paid_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `update_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `due_date` | `date` | YES | `NULL` | — | — |
| `total_cash_advance` | `double` | NO | `0` | — | — |
| `total_approve` | `double` | NO | `0` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `is_paid` | `tinyint(4)` | NO | `0` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `cancel_description` | `text` | YES | `NULL` | — | — |
| `is_realisation` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `date_opened` | `date` | NO | `—` | — | — |
| `date_closed` | `date` | NO | `—` | — | — |
| `cash_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `type_transaksi` | `int(11)` | YES | `1` | — | — |

**Indeks:** cash_advances_account_advance_id_foreign: account_advance_id; cash_advances_account_cash_id_foreign: account_cash_id; cash_advances_approve_by_foreign: approve_by; cash_advances_cancel_by_foreign: cancel_by; cash_advances_cash_transaction_id_foreign: cash_transaction_id; cash_advances_company_id_foreign: company_id; cash_advances_create_by_foreign: create_by; cash_advances_driver_id_foreign: employee_id; cash_advances_journal_id_foreign: journal_id; cash_advances_paid_by_foreign: paid_by; cash_advances_realisation_id_foreign: realisation_id; cash_advances_update_by_foreign: update_by; PRIMARY (UNIQUE): id.  
**Foreign key:** cash_advances_account_advance_id_foreign (account_advance_id → accounts.id); cash_advances_account_cash_id_foreign (account_cash_id → accounts.id); cash_advances_approve_by_foreign (approve_by → users.id); cash_advances_cancel_by_foreign (cancel_by → users.id); cash_advances_cash_transaction_id_foreign (cash_transaction_id → cash_transactions.id); cash_advances_company_id_foreign (company_id → companies.id); cash_advances_create_by_foreign (create_by → users.id); cash_advances_driver_id_foreign (employee_id → contacts.id); cash_advances_journal_id_foreign (journal_id → journals.id); cash_advances_paid_by_foreign (paid_by → users.id); cash_advances_realisation_id_foreign (realisation_id → cash_advances.id); cash_advances_update_by_foreign (update_by → users.id).

### `cash_advance_reports` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `cash_count_id` | `int(11)` | NO | `—` | — | — |
| `cash_advance_id` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cash_advance_statuses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `status` | `int(10) unsigned` | NO | `—` | — | — |
| `user_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** cash_advance_statuses_header_id_foreign: header_id; cash_advance_statuses_user_id_foreign: user_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cash_advance_statuses_header_id_foreign (header_id → cash_advances.id); cash_advance_statuses_user_id_foreign (user_id → users.id).

### `cash_advance_transactions` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `cash_advance_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cash_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `is_in` | `int(11)` | YES | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** cash_advance_transactions_cash_advance_id_foreign: cash_advance_id; cash_advance_transactions_cash_transaction_id_foreign: cash_transaction_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cash_advance_transactions_cash_advance_id_foreign (cash_advance_id → cash_advances.id); cash_advance_transactions_cash_transaction_id_foreign (cash_transaction_id → cash_transactions.id).

### `cash_categories` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `kategori` | `int(11)` | NO | `—` | — | — |
| `jenis` | `int(11)` | NO | `—` | — | — |
| `is_base` | `tinyint(1)` | NO | `0` | — | — |
| `parent_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** cash_categories_parent_id_foreign: parent_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cash_categories_parent_id_foreign (parent_id → cash_categories.id).

### `cash_category_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** cash_category_details_header_id_foreign: header_id; cash_category_details_type_transaction_id_foreign: type_transaction_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cash_category_details_header_id_foreign (header_id → cash_categories.id); cash_category_details_type_transaction_id_foreign (type_transaction_id → type_transactions.id).

### `cash_counts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `0` | — | — |
| `saldo_awal` | `double` | NO | `—` | — | — |
| `bailout` | `double` | NO | `—` | — | — |
| `officer` | `varchar(191)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `bkk_hari_ini` | `double` | NO | `0` | — | — |
| `bkm_hari_ini` | `double` | NO | `0` | — | — |
| `saldo_akhir` | `double` | NO | `0` | — | — |
| `total_cash_fisik` | `double` | NO | `0` | — | — |
| `total_kasbon` | `double` | NO | `0` | — | — |
| `approved_by_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** cash_counts_approved_by_id_index: approved_by_id; cash_counts_company_id_foreign: company_id; cash_counts_create_by_foreign: create_by; PRIMARY (UNIQUE): id.  
**Foreign key:** cash_counts_approved_by_id_foreign (approved_by_id → users.id); cash_counts_company_id_foreign (company_id → companies.id); cash_counts_create_by_foreign (create_by → users.id).

### `cash_count_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `nominal` | `double` | NO | `—` | — | — |
| `qty` | `double` | NO | `—` | — | — |
| `total` | `double` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** cash_count_details_header_id_foreign: header_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cash_count_details_header_id_foreign (header_id → cash_counts.id).

### `cash_migrations` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `company_from` | `int(10) unsigned` | NO | `—` | — | — |
| `company_to` | `int(10) unsigned` | NO | `—` | — | — |
| `date_request` | `date` | NO | `—` | — | — |
| `date_needed` | `date` | NO | `—` | — | — |
| `date_realisation` | `date` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `approve_direction_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `realisation_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cash_account_from` | `int(10) unsigned` | NO | `—` | — | — |
| `cash_account_to` | `int(10) unsigned` | NO | `—` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `total` | `double(20,2)` | NO | `0.00` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `reject_reason` | `text` | NO | `—` | — | — |
| `cash_account_cross` | `int(10) unsigned` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cash_reimburses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `code_realization` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_realization` | `date` | YES | `NULL` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `periode_start` | `date` | NO | `—` | — | — |
| `periode_end` | `date` | NO | `—` | — | — |
| `company_request_id` | `int(10) unsigned` | NO | `—` | — | — |
| `company_reimburse_id` | `int(10) unsigned` | NO | `—` | — | — |
| `account_request_id` | `int(10) unsigned` | NO | `—` | — | — |
| `account_mutation_id` | `int(10) unsigned` | NO | `—` | — | — |
| `account_reimburse_id` | `int(10) unsigned` | NO | `—` | — | — |
| `journal_id_out` | `int(10) unsigned` | YES | `NULL` | — | — |
| `journal_id_in` | `int(10) unsigned` | YES | `NULL` | — | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `approve_direction_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `realization_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `reject_reason` | `text` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cash_reimburse_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `cash_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `cash_transaction_detail_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cost_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cash_transactions` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `jenis` | `int(11)` | NO | `—` | — | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `reff` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_cut` | `tinyint(1)` | YES | `0` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `edit_count` | `int(11)` | NO | `0` | — | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `parent_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `status_cost` | `int(11)` | NO | `1` | — | — |
| `customer_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `from_kasbon` | `int(11)` | YES | `0` | — | — |

**Indeks:** cash_transactions_account_id_foreign: account_id; cash_transactions_company_id_foreign: company_id; cash_transactions_created_by_foreign: created_by; cash_transactions_customer_order_id_foreign: customer_order_id; cash_transactions_journal_id_foreign: journal_id; cash_transactions_parent_id_foreign: parent_id; cash_transactions_type_transaction_id_foreign: type_transaction_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cash_transactions_account_id_foreign (account_id → accounts.id); cash_transactions_company_id_foreign (company_id → companies.id); cash_transactions_created_by_foreign (created_by → users.id); cash_transactions_customer_order_id_foreign (customer_order_id → customer_orders.id); cash_transactions_journal_id_foreign (journal_id → journals.id); cash_transactions_parent_id_foreign (parent_id → cash_transactions.id); cash_transactions_type_transaction_id_foreign (type_transaction_id → type_transactions.id).

### `cash_transaction_cost_statuses` — 4 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(20)` | NO | `—` | MUL | — |
| `name` | `varchar(50)` | NO | `—` | — | — |

**Indeks:** cash_transaction_cost_statuses_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cash_transaction_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cash_category_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `contact_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `amount` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `jenis` | `int(11)` | NO | `1` | — | — |
| `is_reimburse` | `int(11)` | NO | `0` | — | — |
| `uploaded_file` | `varchar(191)` | YES | `NULL` | — | — |
| `job_order_cost_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `manifest_cost_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cost_id` | `int(11)` | YES | `NULL` | — | — |
| `kasbon_cost_title` | `varchar(191)` | YES | `NULL` | — | — |
| `relation_cost_id` | `int(11)` | YES | `NULL` | — | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** cash_transaction_details_job_order_cost_id_index: job_order_cost_id; cash_transaction_details_manifest_cost_id_index: manifest_cost_id; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `categories` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `parent_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `is_tire` | `tinyint(1)` | NO | `0` | — | — |
| `is_asset` | `tinyint(1)` | NO | `0` | — | — |
| `is_jasa` | `tinyint(1)` | NO | `0` | — | — |
| `is_ban_luar` | `tinyint(1)` | NO | `0` | — | — |
| `is_ban_dalam` | `tinyint(1)` | NO | `0` | — | — |
| `is_marset` | `tinyint(1)` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `ban_master` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_pallet` | `tinyint(1)` | NO | `0` | — | — |
| `is_container_part` | `smallint(6)` | NO | `0` | MUL | — |
| `is_container_yard` | `smallint(6)` | NO | `0` | MUL | — |
| `default_rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_radial` | `int(11)` | NO | `0` | — | — |
| `is_bias` | `int(11)` | NO | `0` | — | — |
| `is_bbm` | `int(11)` | NO | `0` | — | — |

**Indeks:** categories_default_rack_id_index: default_rack_id; categories_is_container_part_index: is_container_part; categories_is_container_yard_index: is_container_yard; categories_parent_id_foreign: parent_id; PRIMARY (UNIQUE): id.  
**Foreign key:** categories_default_rack_id_foreign (default_rack_id → racks.id); categories_parent_id_foreign (parent_id → categories.id).

### `cek_giros` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `bank_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `penerbit_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `penerima_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `kliring_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_effective` | `date` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `giro_no` | `varchar(191)` | NO | `—` | — | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `jenis` | `int(11)` | NO | `—` | — | — |
| `amount` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `is_kliring` | `tinyint(1)` | NO | `0` | — | — |
| `is_empty` | `tinyint(1)` | NO | `0` | — | — |
| `is_used` | `tinyint(1)` | NO | `0` | — | — |
| `is_saldo` | `tinyint(1)` | NO | `0` | — | — |
| `is_journal_saldo` | `tinyint(1)` | NO | `0` | — | — |
| `is_journal_empty` | `tinyint(1)` | NO | `0` | — | — |
| `is_cancel_kliring` | `tinyint(1)` | NO | `0` | — | — |
| `is_cancel_empty` | `tinyint(1)` | NO | `0` | — | — |
| `cancel_kliring_reason` | `varchar(191)` | YES | `NULL` | — | — |
| `cancel_empty_reason` | `varchar(191)` | YES | `NULL` | — | — |
| `cancel_giro_reason` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `account_bank_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** cek_giros_account_bank_id_foreign: account_bank_id; cek_giros_bank_id_foreign: bank_id; cek_giros_company_id_foreign: company_id; cek_giros_journal_id_foreign: journal_id; cek_giros_kliring_account_id_foreign: kliring_account_id; cek_giros_penerbit_id_foreign: penerbit_id; cek_giros_penerima_id_foreign: penerima_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cek_giros_account_bank_id_foreign (account_bank_id → accounts.id); cek_giros_bank_id_foreign (bank_id → banks.id); cek_giros_company_id_foreign (company_id → companies.id); cek_giros_journal_id_foreign (journal_id → journals.id); cek_giros_kliring_account_id_foreign (kliring_account_id → accounts.id); cek_giros_penerbit_id_foreign (penerbit_id → contacts.id); cek_giros_penerima_id_foreign (penerima_id → contacts.id).

### `cities` — 4 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `province_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `type` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** cities_province_id_foreign: province_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cities_province_id_foreign (province_id → provinces.id).

### `claims` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `collectible_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `job_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `sales_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `claim_type` | `int(11)` | NO | `1` | — | — |
| `driver_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `payable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `receivable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `status` | `tinyint(1)` | NO | `1` | — | — |
| `code` | `varchar(50)` | YES | `NULL` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** claims_code_index: code; claims_collectible_id_foreign: collectible_id; claims_company_id_foreign: company_id; claims_customer_id_foreign: customer_id; claims_driver_id_foreign: driver_id; claims_job_order_id_foreign: job_order_id; claims_journal_id_foreign: journal_id; claims_payable_id_foreign: payable_id; claims_receivable_id_foreign: receivable_id; claims_sales_order_id_foreign: sales_order_id; claims_vendor_id_foreign: vendor_id; PRIMARY (UNIQUE): id.  
**Foreign key:** claims_collectible_id_foreign (collectible_id → contacts.id); claims_company_id_foreign (company_id → companies.id); claims_customer_id_foreign (customer_id → contacts.id); claims_driver_id_foreign (driver_id → contacts.id); claims_job_order_id_foreign (job_order_id → job_orders.id); claims_journal_id_foreign (journal_id → journals.id); claims_payable_id_foreign (payable_id → payables.id); claims_receivable_id_foreign (receivable_id → receivables.id); claims_sales_order_id_foreign (sales_order_id → sales_orders.id); claims_vendor_id_foreign (vendor_id → contacts.id).

### `claim_categories` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(30)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `claim_category_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `category_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `claim_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** claim_category_details_category_id_foreign: category_id; claim_category_details_claim_detail_id_foreign: claim_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** claim_category_details_category_id_foreign (category_id → claim_categories.id); claim_category_details_claim_detail_id_foreign (claim_detail_id → claim_details.id).

### `claim_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_order_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `commodity_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `—` | — | — |
| `price` | `double` | NO | `—` | — | — |
| `total_price` | `double` | NO | `—` | — | — |
| `claim_qty` | `double` | NO | `—` | — | — |
| `claim_price` | `double` | NO | `—` | — | — |
| `claim_total_price` | `double` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `sold_qty` | `int(11)` | NO | `0` | — | — |

**Indeks:** claim_details_commodity_id_foreign: commodity_id; claim_details_header_id_foreign: header_id; claim_details_job_order_detail_id_foreign: job_order_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** claim_details_commodity_id_foreign (commodity_id → commodities.id); claim_details_header_id_foreign (header_id → claims.id); claim_details_job_order_detail_id_foreign (job_order_detail_id → job_order_details.id).

### `claim_sales` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `claim_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `term` | `int(11)` | NO | `1` | — | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `termin_day` | `int(11)` | NO | `0` | — | — |
| `termin_date` | `date` | YES | `NULL` | — | — |
| `payment_for` | `int(11)` | NO | `1` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `receivable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cash_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_pajak` | `int(11)` | NO | `0` | — | — |
| `is_npwp` | `int(11)` | YES | `0` | — | — |
| `ppn` | `int(11)` | NO | `0` | — | — |
| `pph` | `int(11)` | NO | `0` | — | — |

**Indeks:** claim_sales_account_id_foreign: account_id; claim_sales_cash_transaction_id_foreign: cash_transaction_id; claim_sales_claim_id_foreign: claim_id; claim_sales_company_id_foreign: company_id; claim_sales_customer_id_foreign: customer_id; claim_sales_journal_id_foreign: journal_id; claim_sales_receivable_id_foreign: receivable_id; PRIMARY (UNIQUE): id.  
**Foreign key:** claim_sales_account_id_foreign (account_id → accounts.id); claim_sales_cash_transaction_id_foreign (cash_transaction_id → cash_transactions.id); claim_sales_claim_id_foreign (claim_id → claims.id); claim_sales_company_id_foreign (company_id → companies.id); claim_sales_customer_id_foreign (customer_id → contacts.id); claim_sales_journal_id_foreign (journal_id → journals.id); claim_sales_receivable_id_foreign (receivable_id → receivables.id).

### `claim_sale_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `claim_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** claim_sale_details_claim_detail_id_foreign: claim_detail_id; claim_sale_details_commodity_id_foreign: commodity_id; claim_sale_details_header_id_foreign: header_id; PRIMARY (UNIQUE): id.  
**Foreign key:** claim_sale_details_claim_detail_id_foreign (claim_detail_id → claim_details.id); claim_sale_details_commodity_id_foreign (commodity_id → commodities.id); claim_sale_details_header_id_foreign (header_id → claim_sales.id).

### `closing` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `start_periode` | `date` | NO | `—` | — | — |
| `end_periode` | `date` | NO | `—` | — | — |
| `closing_date` | `date` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `0` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `is_lock` | `tinyint(1)` | NO | `0` | — | — |
| `is_depresiasi` | `tinyint(1)` | NO | `0` | — | — |
| `is_revaluasi` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** closing_company_id_foreign: company_id; closing_journal_id_foreign: journal_id; PRIMARY (UNIQUE): id.  
**Foreign key:** closing_company_id_foreign (company_id → companies.id); closing_journal_id_foreign (journal_id → journals.id).

### `combined_prices` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(200)` | NO | `—` | — | — |
| `name` | `varchar(200)` | NO | `—` | — | — |
| `service_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `total_item` | `int(11)` | NO | `0` | — | — |
| `is_active` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** combined_prices_company_id_foreign: company_id; combined_prices_created_by_foreign: created_by; combined_prices_service_id_index: service_id; PRIMARY (UNIQUE): id.  
**Foreign key:** combined_prices_company_id_foreign (company_id → companies.id); combined_prices_created_by_foreign (created_by → users.id); combined_prices_service_id_foreign (service_id → services.id).

### `combined_price_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `service_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** combined_price_details_header_id_foreign: header_id; combined_price_details_service_id_foreign: service_id; PRIMARY (UNIQUE): id.  
**Foreign key:** combined_price_details_header_id_foreign (header_id → combined_prices.id); combined_price_details_service_id_foreign (service_id → services.id).

### `commodities` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `text` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_default` | `tinyint(1)` | NO | `0` | — | — |
| `is_expired` | `tinyint(1)` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `companies` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `area_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `city_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `address` | `varchar(191)` | NO | `—` | — | — |
| `phone` | `varchar(191)` | YES | `NULL` | — | — |
| `email` | `varchar(191)` | YES | `NULL` | — | — |
| `website` | `varchar(191)` | YES | `NULL` | — | — |
| `is_pusat` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `rek_no_1` | `varchar(191)` | YES | `NULL` | — | — |
| `rek_name_1` | `varchar(191)` | YES | `NULL` | — | — |
| `rek_bank_1` | `varchar(191)` | YES | `NULL` | — | — |
| `rek_no_2` | `varchar(191)` | YES | `NULL` | — | — |
| `rek_name_2` | `varchar(191)` | YES | `NULL` | — | — |
| `rek_bank_2` | `varchar(191)` | YES | `NULL` | — | — |
| `plafond` | `double` | YES | `NULL` | — | — |
| `cash_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `bank_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `mutation_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_kasbon_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `rek_bank_id_1` | `int(10) unsigned` | YES | `NULL` | — | — |
| `rek_bank_id_2` | `int(10) unsigned` | YES | `NULL` | — | — |
| `fax` | `varchar(191)` | YES | `NULL` | — | — |
| `latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** companies_account_kasbon_id_foreign: account_kasbon_id; companies_area_id_foreign: area_id; companies_bank_for: bank_account_id; companies_cash_for: cash_account_id; companies_city_id_foreign: city_id; companies_mut_for: mutation_account_id; PRIMARY (UNIQUE): id.  
**Foreign key:** companies_account_kasbon_id_foreign (account_kasbon_id → accounts.id); companies_area_id_foreign (area_id → areas.id); companies_bank_for (bank_account_id → accounts.id); companies_cash_for (cash_account_id → accounts.id); companies_city_id_foreign (city_id → cities.id); companies_mut_for (mutation_account_id → accounts.id).

### `company_numberings` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `urut` | `int(11)` | NO | `—` | — | — |
| `prefix` | `varchar(191)` | NO | `—` | — | — |
| `type` | `varchar(191)` | NO | `—` | — | — |
| `format_data` | `varchar(191)` | YES | `NULL` | — | — |
| `last_value` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `contacts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `address` | `varchar(191)` | NO | `—` | — | — |
| `city_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `postal_code` | `varchar(191)` | YES | `NULL` | — | — |
| `phone` | `varchar(191)` | YES | `NULL` | — | — |
| `phone2` | `varchar(191)` | YES | `NULL` | — | — |
| `fax` | `varchar(191)` | YES | `NULL` | — | — |
| `email` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person_email` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person_no` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person_no_2` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person_position` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person_npwp` | `varchar(191)` | YES | `NULL` | — | — |
| `pegawai_no` | `varchar(191)` | YES | `NULL` | — | — |
| `vendor_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `category` | `varchar(191)` | YES | `NULL` | — | — |
| `is_pegawai` | `tinyint(1)` | NO | `0` | — | — |
| `is_investor` | `tinyint(1)` | NO | `0` | — | — |
| `is_pelanggan` | `tinyint(1)` | NO | `0` | — | — |
| `is_asuransi` | `tinyint(1)` | NO | `0` | — | — |
| `is_supplier` | `tinyint(1)` | NO | `0` | — | — |
| `is_depo_bongkar` | `tinyint(1)` | NO | `0` | — | — |
| `is_helper` | `tinyint(1)` | NO | `0` | — | — |
| `is_driver` | `tinyint(1)` | NO | `0` | — | — |
| `is_vendor` | `tinyint(1)` | NO | `0` | — | — |
| `is_sales` | `tinyint(1)` | NO | `0` | — | — |
| `is_kurir` | `tinyint(1)` | NO | `0` | — | — |
| `is_pengirim` | `tinyint(1)` | NO | `0` | — | — |
| `is_penerima` | `tinyint(1)` | NO | `0` | — | — |
| `is_spbu` | `tinyint(1)` | NO | `0` | — | — |
| `akun_hutang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `akun_piutang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `akun_um_supplier` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `akun_um_customer` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `term_of_payment` | `int(11)` | YES | `NULL` | — | — |
| `limit_piutang` | `int(11)` | YES | `NULL` | — | — |
| `limit_hutang` | `int(11)` | YES | `NULL` | — | — |
| `npwp` | `varchar(191)` | YES | `NULL` | — | — |
| `pkp` | `tinyint(1)` | YES | `NULL` | — | — |
| `tax_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `is_customer_po` | `tinyint(1)` | NO | `0` | — | — |
| `rek_no` | `varchar(191)` | YES | `NULL` | — | — |
| `rek_milik` | `varchar(191)` | YES | `NULL` | — | — |
| `rek_bank_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `rek_cabang` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_active` | `tinyint(1)` | YES | `1` | — | — |
| `vendor_register_date` | `datetime` | YES | `NULL` | — | — |
| `vendor_status_approve` | `tinyint(1)` | YES | `2` | — | — |
| `vendor_approve_date` | `datetime` | YES | `NULL` | — | — |
| `vendor_reject_register_date` | `datetime` | YES | `NULL` | — | — |
| `vendor_user_approve` | `int(10) unsigned` | YES | `NULL` | — | — |
| `driver_status` | `int(11)` | YES | `NULL` | — | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_internal` | `tinyint(1)` | YES | `1` | — | — |
| `address_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `file_name` | `varchar(191)` | YES | `NULL` | — | — |
| `file_extension` | `varchar(191)` | YES | `NULL` | — | — |
| `ktp_file_name` | `varchar(191)` | YES | `NULL` | — | — |
| `ktp_file_extension` | `varchar(191)` | YES | `NULL` | — | — |
| `npwp_file_name` | `varchar(191)` | YES | `NULL` | — | — |
| `npwp_file_extension` | `varchar(191)` | YES | `NULL` | — | — |
| `parent_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `password` | `varchar(191)` | YES | `NULL` | — | — |
| `api_token` | `varchar(191)` | YES | `NULL` | — | — |
| `last_login` | `datetime` | YES | `NULL` | — | — |
| `last_update` | `datetime` | YES | `NULL` | — | — |
| `is_staff_gudang` | `int(11)` | YES | `0` | — | — |
| `customer_service_name` | `varchar(200)` | NO | `—` | — | — |
| `sales_name` | `varchar(200)` | NO | `—` | — | — |
| `is_approved_customer` | `int(11)` | NO | `0` | — | — |
| `sales_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `customer_service_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `no_ktp` | `varchar(50)` | YES | `NULL` | — | — |
| `npwp_cabang` | `varchar(191)` | YES | `NULL` | UNI | — |
| `additional` | `text` | YES | `NULL` | — | — |
| `latitude` | `varchar(50)` | NO | `'0'` | — | — |
| `longitude` | `varchar(50)` | NO | `'0'` | — | — |
| `no_tdp` | `varchar(191)` | YES | `NULL` | — | — |
| `no_siup` | `varchar(191)` | YES | `NULL` | — | — |
| `no_sppkp` | `varchar(191)` | YES | `NULL` | — | — |
| `website` | `varchar(191)` | YES | `NULL` | — | — |
| `position` | `varchar(191)` | YES | `NULL` | — | — |
| `purchase_purpose` | `varchar(191)` | YES | `NULL` | — | — |
| `personal_facebook_account` | `varchar(191)` | YES | `NULL` | — | — |
| `personal_instagram_account` | `varchar(191)` | YES | `NULL` | — | — |
| `company_facebook_account` | `varchar(191)` | YES | `NULL` | — | — |
| `company_instagram_account` | `varchar(191)` | YES | `NULL` | — | — |
| `company_customer_service` | `varchar(191)` | YES | `NULL` | — | — |
| `owner_name` | `varchar(191)` | YES | `NULL` | — | — |
| `akun_hutang_belum_tertagih` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `no_sim` | `varchar(151)` | YES | `NULL` | — | — |
| `akun_piutang_belum_tertagih` | `int(11)` | YES | `NULL` | — | — |
| `is_bengkel` | `int(11)` | NO | `0` | — | — |

**Indeks:** contacts_akun_hutang_belum_tertagih_foreign: akun_hutang_belum_tertagih; contacts_akun_hutang_foreign: akun_hutang; contacts_akun_piutang_foreign: akun_piutang; contacts_akun_um_customer_foreign: akun_um_customer; contacts_akun_um_supplier_foreign: akun_um_supplier; contacts_city_id_foreign: city_id; contacts_company_id_foreign: company_id; contacts_customer_service_id_index: customer_service_id; contacts_npwp_cabang_unique (UNIQUE): npwp_cabang; contacts_parent_id_foreign: parent_id; contacts_rek_bank_id_foreign: rek_bank_id; contacts_sales_id_index: sales_id; contacts_tax_id_foreign: tax_id; contacts_vendor_type_id_foreign: vendor_type_id; PRIMARY (UNIQUE): id.  
**Foreign key:** contacts_akun_hutang_belum_tertagih_foreign (akun_hutang_belum_tertagih → accounts.id); contacts_akun_hutang_foreign (akun_hutang → accounts.id); contacts_akun_piutang_foreign (akun_piutang → accounts.id); contacts_akun_um_customer_foreign (akun_um_customer → accounts.id); contacts_akun_um_supplier_foreign (akun_um_supplier → accounts.id); contacts_city_id_foreign (city_id → cities.id); contacts_company_id_foreign (company_id → companies.id); contacts_customer_service_id_foreign (customer_service_id → contacts.id); contacts_parent_id_foreign (parent_id → contacts.id); contacts_rek_bank_id_foreign (rek_bank_id → banks.id); contacts_sales_id_foreign (sales_id → contacts.id); contacts_tax_id_foreign (tax_id → taxes.id); contacts_vendor_type_id_foreign (vendor_type_id → vendor_types.id).

### `contact_addresses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `contact_id` | `int(10) unsigned` | NO | `—` | — | — |
| `contact_address_id` | `int(10) unsigned` | NO | `—` | — | — |
| `contact_bill_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `address_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `contact_documents` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `file_name` | `varchar(191)` | YES | `NULL` | — | — |
| `file_extension` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** contact_documents_contact_id_foreign: contact_id; PRIMARY (UNIQUE): id.  
**Foreign key:** contact_documents_contact_id_foreign (contact_id → contacts.id).

### `contact_files` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `file_name` | `varchar(191)` | NO | `—` | — | — |
| `date_upload` | `date` | NO | `—` | — | — |
| `extension` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** contact_files_contact_id_foreign: contact_id; PRIMARY (UNIQUE): id.  
**Foreign key:** contact_files_contact_id_foreign (contact_id → contacts.id).

### `contact_locations` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `longitude` | `varchar(50)` | NO | `'0'` | — | — |
| `latitude` | `varchar(50)` | NO | `'0'` | — | — |
| `created_at` | `datetime` | NO | `current_timestamp()` | — | — |
| `delivery_order_driver_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** contact_locations_contact_id_index: contact_id; PRIMARY (UNIQUE): id.  
**Foreign key:** contact_locations_contact_id_foreign (contact_id → contacts.id).

### `containers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `container_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vessel_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `commodity_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `voyage_schedule_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `manifest_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `pickup_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `work_order_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `container_no` | `varchar(191)` | NO | `—` | — | — |
| `booking_date` | `date` | NO | `—` | — | — |
| `booking_number` | `varchar(191)` | NO | `—` | — | — |
| `no_bapb` | `varchar(191)` | YES | `NULL` | — | — |
| `rent_price` | `double` | NO | `0` | — | — |
| `departure` | `datetime` | YES | `NULL` | — | — |
| `arrival` | `datetime` | YES | `NULL` | — | — |
| `stripping` | `datetime` | YES | `NULL` | — | — |
| `seal_no` | `varchar(191)` | YES | `NULL` | — | — |
| `seal_date` | `date` | YES | `NULL` | — | — |
| `total_item` | `double` | NO | `0` | — | — |
| `total_tonase` | `double` | NO | `0` | — | — |
| `total_volume` | `double` | NO | `0` | — | — |
| `total_job_order` | `int(11)` | NO | `0` | — | — |
| `is_fcl` | `tinyint(1)` | NO | `1` | — | — |
| `commodity` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `stuffing` | `datetime` | YES | `NULL` | — | — |

**Indeks:** containers_commodity_id_foreign: commodity_id; containers_company_id_foreign: company_id; containers_container_type_id_foreign: container_type_id; containers_customer_id_foreign: customer_id; containers_manifest_id_foreign: manifest_id; containers_vendor_id_foreign: vendor_id; containers_vessel_id_foreign: vessel_id; containers_voyage_schedule_id_foreign: voyage_schedule_id; PRIMARY (UNIQUE): id.  
**Foreign key:** containers_commodity_id_foreign (commodity_id → commodities.id); containers_company_id_foreign (company_id → companies.id); containers_container_type_id_foreign (container_type_id → container_types.id); containers_customer_id_foreign (customer_id → contacts.id); containers_manifest_id_foreign (manifest_id → manifests.id); containers_vendor_id_foreign (vendor_id → contacts.id); containers_vessel_id_foreign (vessel_id → vessels.id); containers_voyage_schedule_id_foreign (voyage_schedule_id → voyage_schedules.id).

### `container_inspections` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `date` | `date` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `checker_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** container_inspections_checker_id_index: checker_id; container_inspections_created_by_foreign: created_by; PRIMARY (UNIQUE): id.  
**Foreign key:** container_inspections_checker_id_foreign (checker_id → contacts.id); container_inspections_created_by_foreign (created_by → users.id).

### `container_inspection_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `container_inspection_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `container_part_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_condition_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** container_inspection_details_container_inspection_id_index: container_inspection_id; container_inspection_details_container_part_id_index: container_part_id; container_inspection_details_item_condition_id_index: item_condition_id; PRIMARY (UNIQUE): id.  
**Foreign key:** container_inspection_details_container_part_id_foreign (container_part_id → items.id); container_inspection_details_item_condition_id_foreign (item_condition_id → item_conditions.id).

### `container_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `size` | `int(11)` | NO | `—` | — | — |
| `unit` | `varchar(15)` | NO | `'STD'` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cost_pl_categories` — 19 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cost_route_types` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(30)` | NO | `—` | MUL | — |
| `name` | `varchar(80)` | NO | `—` | MUL | — |

**Indeks:** cost_route_types_name_index: name; cost_route_types_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `cost_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `akun_biaya` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `akun_uang_muka` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `akun_kas_hutang` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cash_category_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `parent_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | UNI | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `initial_cost` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `is_bbm` | `tinyint(1)` | NO | `0` | — | — |
| `is_operasional` | `tinyint(1)` | NO | `0` | — | — |
| `is_invoice` | `tinyint(1)` | NO | `0` | — | — |
| `is_biaya_lain` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_ppn` | `tinyint(1)` | YES | `NULL` | — | — |
| `ppn_cost` | `double(20,2)` | YES | `0.00` | — | — |
| `qty` | `double(20,2)` | YES | `0.00` | — | — |
| `cost` | `double(20,2)` | YES | `0.00` | — | — |
| `company_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_overtime` | `tinyint(1)` | NO | `0` | — | — |
| `is_insurance` | `int(10) unsigned` | NO | `0` | — | — |
| `percentage` | `int(11)` | NO | `0` | — | — |
| `is_auto_invoice` | `smallint(6)` | NO | `0` | — | — |
| `is_shipment` | `smallint(6)` | NO | `0` | MUL | — |
| `cost_route_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `count_based_on` | `int(11)` | YES | `NULL` | — | — |
| `is_kasbon` | `int(11)` | YES | `0` | — | — |
| `akun_biaya_sementara` | `int(11)` | YES | `NULL` | — | — |
| `akun_biaya_reimbursh` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_driver` | `tinyint(1)` | NO | `0` | — | — |
| `is_co_driver` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_kendaraan` | `tinyint(1)` | NO | `0` | — | — |
| `is_rembes` | `tinyint(1)` | NO | `0` | — | — |
| `is_kali` | `tinyint(1)` | NO | `0` | — | — |
| `is_helper` | `tinyint(1)` | NO | `0` | — | — |
| `is_vendor` | `tinyint(1)` | NO | `0` | — | — |
| `is_retribusi` | `tinyint(1)` | NO | `0` | — | — |
| `is_titipan` | `tinyint(1)` | NO | `0` | — | — |
| `is_parent` | `tinyint(1)` | NO | `0` | — | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `item_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cost_pl_category_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** cost_types_akun_biaya_foreign: akun_biaya; cost_types_akun_kas_hutang_foreign: akun_kas_hutang; cost_types_akun_uang_muka_foreign: akun_uang_muka; cost_types_cash_category_id_foreign: cash_category_id; cost_types_code_unique (UNIQUE): code; cost_types_company_id_foreign: company_id; cost_types_cost_route_type_id_foreign: cost_route_type_id; cost_types_created_by_foreign: created_by; cost_types_is_shipment_index: is_shipment; cost_types_item_id_foreign: item_id; cost_types_parent_id_foreign: parent_id; cost_types_vendor_id_foreign: vendor_id; PRIMARY (UNIQUE): id.  
**Foreign key:** cost_types_akun_biaya_foreign (akun_biaya → accounts.id); cost_types_akun_kas_hutang_foreign (akun_kas_hutang → accounts.id); cost_types_akun_uang_muka_foreign (akun_uang_muka → accounts.id); cost_types_cash_category_id_foreign (cash_category_id → cash_categories.id); cost_types_company_id_foreign (company_id → companies.id); cost_types_cost_route_type_id_foreign (cost_route_type_id → cost_route_types.id); cost_types_created_by_foreign (created_by → users.id); cost_types_item_id_foreign (item_id → items.id); cost_types_parent_id_foreign (parent_id → cost_types.id); cost_types_vendor_id_foreign (vendor_id → contacts.id).

### `countries` — 1 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `customer_job_orders` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | — | — |
| `route_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `transaction_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `service_type_id` | `int(10) unsigned` | NO | `—` | — | — |
| `service_id` | `int(10) unsigned` | NO | `—` | — | — |
| `sender_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `receiver_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `quotation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `quotation_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `journal_temp_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `collectible_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `work_order_id` | `int(10) unsigned` | NO | `—` | — | — |
| `invoice_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `receivable_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `kpi_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `shipment_date` | `datetime` | YES | `NULL` | — | — |
| `shipment_done` | `datetime` | YES | `NULL` | — | — |
| `duration` | `double` | NO | `1` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(10) unsigned` | YES | `1` | — | — |
| `total_unit` | `double` | NO | `1` | — | — |
| `total_item` | `int(11)` | NO | `0` | — | — |
| `is_cancel` | `tinyint(4)` | NO | `0` | — | — |
| `cancel_date` | `date` | YES | `NULL` | — | — |
| `cancel_description` | `text` | YES | `NULL` | — | — |
| `is_manifest` | `tinyint(4)` | NO | `0` | — | — |
| `is_done` | `tinyint(4)` | NO | `0` | — | — |
| `code_invoice` | `varchar(191)` | YES | `NULL` | — | — |
| `date_invoice` | `date` | YES | `NULL` | — | — |
| `no_po_customer` | `varchar(191)` | YES | `NULL` | — | — |
| `no_bl` | `varchar(191)` | YES | `NULL` | — | — |
| `moda_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `container_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `docs_no` | `varchar(191)` | YES | `NULL` | — | — |
| `docs_reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `piece_name` | `varchar(191)` | YES | `NULL` | — | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `work_order_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `aju_number` | `varchar(191)` | YES | `NULL` | — | — |
| `submit` | `int(11)` | NO | `1` | — | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `warehouse_staff_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `imposition` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_operational_done` | `tinyint(4)` | NO | `0` | — | — |
| `vessel_name` | `varchar(191)` | YES | `NULL` | — | — |
| `voyage_no` | `varchar(191)` | YES | `NULL` | — | — |
| `document_name` | `varchar(191)` | YES | `NULL` | — | — |
| `is_handling` | `int(11)` | NO | `0` | — | — |
| `is_warehouse` | `int(11)` | NO | `0` | — | — |
| `is_packaging` | `int(11)` | NO | `0` | — | — |
| `is_warehouserent` | `int(11)` | NO | `0` | — | — |
| `is_stuffing` | `int(11)` | NO | `0` | — | — |
| `uniqid` | `varchar(191)` | YES | `NULL` | — | — |
| `warehouse_receipt_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `job_order_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `price_list_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `agent_name` | `varchar(191)` | YES | `NULL` | — | — |
| `awb_number` | `varchar(191)` | YES | `NULL` | — | — |
| `flight_code` | `varchar(191)` | YES | `NULL` | — | — |
| `flight_route` | `varchar(191)` | YES | `NULL` | — | — |
| `flight_date` | `date` | YES | `NULL` | — | — |
| `cargo_ready_date` | `date` | YES | `NULL` | — | — |
| `house_awb` | `varchar(191)` | YES | `NULL` | — | — |
| `hs_code` | `varchar(191)` | YES | `NULL` | — | — |
| `additional` | `longtext` | YES | `NULL` | — | — |
| `is_invoiced` | `tinyint(1)` | NO | `0` | — | — |
| `sales_order_code` | `varchar(191)` | YES | `NULL` | — | — |
| `depo_awal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `depo_tujuan_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `dock_awal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `dock_tujuan_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `start_window_time` | `timestamp` | YES | `NULL` | — | — |
| `end_window_time` | `timestamp` | YES | `NULL` | — | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |
| `is_planning` | `int(11)` | NO | `0` | — | — |
| `is_loco` | `int(11)` | NO | `0` | — | — |
| `type_tarif` | `int(11)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `customer_job_order_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `price_list_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `quotation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `quotation_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `sender_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `receiver_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_contract` | `tinyint(4)` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |
| `imposition` | `int(10) unsigned` | YES | `NULL` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `weight` | `double` | NO | `0` | — | — |
| `volume` | `double` | NO | `0` | — | — |
| `long` | `double` | NO | `0` | — | — |
| `wide` | `double` | NO | `0` | — | — |
| `high` | `double` | NO | `0` | — | — |
| `v1` | `double` | YES | `0` | — | — |
| `tebal_v1` | `double` | YES | `0` | — | — |
| `v2` | `double` | YES | `0` | — | — |
| `tebal_v2` | `double` | YES | `0` | — | — |
| `transported` | `double` | NO | `0` | — | — |
| `leftover` | `double` | NO | `0` | — | — |
| `item_name` | `varchar(191)` | NO | `—` | — | — |
| `barcode` | `varchar(191)` | NO | `—` | — | — |
| `no_reff` | `varchar(191)` | YES | `NULL` | — | — |
| `no_manifest` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `manifest_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `warehouse_receipt_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `date_out` | `date` | YES | `NULL` | — | — |
| `item_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `no_surat_jalan` | `varchar(191)` | NO | `—` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `picking_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `receive_date` | `datetime` | YES | `NULL` | — | — |
| `weight_type` | `int(11)` | YES | `NULL` | — | — |
| `actual_weight` | `double` | YES | `NULL` | — | — |
| `volumetric_weight` | `double` | YES | `NULL` | — | — |
| `load_date` | `date` | YES | `NULL` | — | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `container_status` | `tinyint(4)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `customer_job_order_detail_serial` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `item_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `serial_no` | `int(11)` | YES | `NULL` | — | — |
| `order_number` | `int(11)` | YES | `NULL` | — | — |
| `batch` | `int(11)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `customer_orders` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `quotation_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date` | `datetime` | NO | `—` | — | — |
| `payment_type` | `tinyint(1)` | NO | `—` | — | — |
| `customer_order_status_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `approved_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_deposit` | `double` | NO | `0` | — | — |
| `jumlah_deposit` | `int(11)` | YES | `NULL` | — | — |
| `all_qty` | `int(11)` | YES | `NULL` | — | — |
| `is_transit` | `int(11)` | NO | `0` | — | — |

**Indeks:** customer_orders_customer_id_foreign: customer_id; customer_orders_customer_order_status_id_foreign: customer_order_status_id; customer_orders_quotation_id_foreign: quotation_id; PRIMARY (UNIQUE): id.  
**Foreign key:** customer_orders_customer_id_foreign (customer_id → contacts.id); customer_orders_customer_order_status_id_foreign (customer_order_status_id → customer_order_statuses.id); customer_orders_quotation_id_foreign (quotation_id → quotations.id).

### `customer_order_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `—` | — | — |
| `stock` | `double` | NO | `—` | — | — |
| `price` | `double` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `available_qty` | `int(11)` | YES | `NULL` | — | — |
| `is_receipt` | `int(11)` | NO | `0` | — | — |

**Indeks:** customer_order_details_header_id_foreign: header_id; customer_order_details_item_id_foreign: item_id; customer_order_details_rack_id_foreign: rack_id; customer_order_details_requested_stock_transaction_id_foreign: requested_stock_transaction_id; customer_order_details_warehouse_receipt_detail_id_foreign: warehouse_receipt_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** customer_order_details_header_id_foreign (header_id → customer_orders.id); customer_order_details_item_id_foreign (item_id → items.id); customer_order_details_rack_id_foreign (rack_id → racks.id); customer_order_details_requested_stock_transaction_id_foreign (requested_stock_transaction_id → stock_transactions.id); customer_order_details_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `customer_order_files` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `file_name` | `varchar(191)` | NO | `—` | — | — |
| `date_upload` | `date` | NO | `—` | — | — |
| `extension` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** customer_order_files_header_id_foreign: header_id; PRIMARY (UNIQUE): id.  
**Foreign key:** customer_order_files_header_id_foreign (header_id → customer_orders.id).

### `customer_order_statuses` — 5 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `customer_prices` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `customer_id` | `int(10) unsigned` | NO | `—` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `route_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `service_id` | `int(10) unsigned` | NO | `—` | — | — |
| `combined_price_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price_type` | `varchar(10)` | NO | `'service'` | — | — |
| `service_type_id` | `int(10) unsigned` | NO | `—` | — | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `moda_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `container_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | NO | `—` | — | — |
| `updated_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `min_tonase` | `double` | YES | `NULL` | — | — |
| `price_tonase` | `double` | YES | `NULL` | — | — |
| `min_volume` | `double` | YES | `NULL` | — | — |
| `price_volume` | `double` | YES | `NULL` | — | — |
| `min_item` | `double` | YES | `NULL` | — | — |
| `price_item` | `double` | YES | `NULL` | — | — |
| `price_full` | `double` | YES | `NULL` | — | — |
| `piece_name` | `varchar(191)` | YES | `NULL` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |
| `imposition` | `int(11)` | YES | `0` | — | — |
| `price_imposition` | `double` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `price_handling_tonase` | `double` | YES | `NULL` | — | — |
| `price_handling_volume` | `double` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_warehouse` | `int(11)` | NO | `0` | — | — |
| `free_storage_day` | `int(11)` | NO | `0` | — | — |
| `over_storage_price` | `double` | NO | `0` | — | — |
| `daily_price` | `double` | NO | `0` | — | — |

**Indeks:** customer_prices_combined_price_id_foreign: combined_price_id; PRIMARY (UNIQUE): id.  
**Foreign key:** customer_prices_combined_price_id_foreign (combined_price_id → combined_prices.id).

### `customer_price_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `service_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `price` | `double` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** customer_price_details_header_id_foreign: header_id; customer_price_details_service_id_foreign: service_id; PRIMARY (UNIQUE): id.  
**Foreign key:** customer_price_details_header_id_foreign (header_id → customer_prices.id); customer_price_details_service_id_foreign (service_id → services.id).

### `customer_stages` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `bobot` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_close_deal` | `tinyint(1)` | NO | `0` | — | — |
| `is_prospect` | `tinyint(1)` | NO | `0` | — | — |
| `is_negotiation` | `tinyint(1)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `dashboards` — 4 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(100)` | NO | `—` | MUL | — |
| `role_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** dashboards_name_index: name; dashboards_role_id_index: role_id; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `dashboard_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `widget_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `row` | `int(11)` | NO | `0` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** dashboard_details_header_id_index: header_id; dashboard_details_row_index: row; dashboard_details_widget_id_index: widget_id; PRIMARY (UNIQUE): id.  
**Foreign key:** dashboard_details_header_id_foreign (header_id → dashboards.id); dashboard_details_widget_id_foreign (widget_id → widgets.id).

### `debts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_request` | `date` | NO | `—` | — | — |
| `date_cancel` | `date` | YES | `NULL` | — | — |
| `cancel_description` | `text` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `code_receive` | `varchar(191)` | YES | `NULL` | — | — |
| `date_receive` | `date` | YES | `NULL` | — | — |
| `description_receive` | `text` | YES | `NULL` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `paid` | `double` | NO | `0` | — | — |
| `overpayment` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `akun_selisih` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** debts_akun_selisih_index: akun_selisih; debts_cancel_by_foreign: cancel_by; debts_company_id_foreign: company_id; debts_create_by_foreign: create_by; debts_journal_id_foreign: journal_id; PRIMARY (UNIQUE): id.  
**Foreign key:** debts_akun_selisih_foreign (akun_selisih → accounts.id); debts_cancel_by_foreign (cancel_by → users.id); debts_company_id_foreign (company_id → companies.id); debts_create_by_foreign (create_by → users.id); debts_journal_id_foreign (journal_id → journals.id).

### `debt_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `payable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `payable_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `um_supplier_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `nota_debet_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `nota_credit_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `debt` | `double` | NO | `0` | — | — |
| `leftover` | `double` | NO | `0` | — | — |
| `total_debt` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** debt_details_create_by_foreign: create_by; debt_details_header_id_foreign: header_id; debt_details_nota_credit_id_foreign: nota_credit_id; debt_details_nota_debet_id_foreign: nota_debet_id; debt_details_payable_detail_id_foreign: payable_detail_id; debt_details_payable_id_foreign: payable_id; debt_details_type_transaction_id_foreign: type_transaction_id; debt_details_um_supplier_id_foreign: um_supplier_id; PRIMARY (UNIQUE): id.  
**Foreign key:** debt_details_create_by_foreign (create_by → users.id); debt_details_header_id_foreign (header_id → debts.id); debt_details_nota_credit_id_foreign (nota_credit_id → nota_credits.id); debt_details_nota_debet_id_foreign (nota_debet_id → nota_debets.id); debt_details_payable_detail_id_foreign (payable_detail_id → payable_details.id); debt_details_payable_id_foreign (payable_id → payables.id); debt_details_type_transaction_id_foreign (type_transaction_id → type_transactions.id); debt_details_um_supplier_id_foreign (um_supplier_id → um_suppliers.id).

### `debt_payments` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cash_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cek_giro_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `payment_type` | `int(11)` | NO | `1` | — | — |
| `reff` | `varchar(191)` | YES | `NULL` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `filename` | `varchar(100)` | NO | `—` | — | — |
| `valid` | `int(11)` | NO | `0` | — | — |

**Indeks:** debt_payments_cash_account_id_foreign: cash_account_id; debt_payments_cek_giro_id_foreign: cek_giro_id; debt_payments_create_by_foreign: create_by; debt_payments_header_id_foreign: header_id; debt_payments_journal_id_foreign: journal_id; PRIMARY (UNIQUE): id.  
**Foreign key:** debt_payments_cash_account_id_foreign (cash_account_id → accounts.id); debt_payments_cek_giro_id_foreign (cek_giro_id → cek_giros.id); debt_payments_create_by_foreign (create_by → users.id); debt_payments_header_id_foreign (header_id → debts.id); debt_payments_journal_id_foreign (journal_id → journals.id).

### `delivery_manifests` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `manifest_id` | `int(10) unsigned` | NO | `—` | — | — |
| `delivery_order_driver_id` | `int(10) unsigned` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `delivery_manifest_status_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `delivery_order_driver_id` | `int(10) unsigned` | NO | `—` | — | — |
| `manifest_detail_id` | `int(10) unsigned` | NO | `—` | — | — |
| `location_id` | `int(10) unsigned` | NO | `—` | — | — |
| `location_type` | `varchar(191)` | NO | `—` | — | — |
| `job_status_id` | `int(10) unsigned` | NO | `—` | — | — |
| `job_type` | `varchar(191)` | YES | `NULL` | — | — |
| `is_done` | `tinyint(4)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `delivery_order_drivers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `driver_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `co_driver_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `driver_name` | `varchar(100)` | YES | `NULL` | — | — |
| `co_driver` | `varchar(191)` | YES | `NULL` | — | — |
| `nopol` | `varchar(100)` | YES | `NULL` | — | — |
| `from_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `from_address_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `to_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `to_address_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `commodity_name` | `varchar(191)` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `latitude_start` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude_start` | `varchar(191)` | YES | `NULL` | — | — |
| `latitude_end` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude_end` | `varchar(191)` | YES | `NULL` | — | — |
| `pick_date` | `timestamp` | NO | `current_timestamp()` | — | — |
| `finish_date` | `datetime` | NO | `'0000-00-00 00:00:00'` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_internal` | `tinyint(1)` | NO | `1` | — | — |
| `is_finish` | `tinyint(1)` | NO | `0` | — | — |
| `cancelled_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_reason` | `varchar(256)` | YES | `NULL` | — | — |
| `job_status_id` | `int(10) unsigned` | NO | `0` | MUL | — |
| `journey_distance` | `double(8,3)` | NO | `0.000` | — | — |
| `code_external` | `varchar(191)` | YES | `NULL` | — | — |
| `depo_awal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `depo_tujuan_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `dock_awal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `dock_tujuan_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |
| `delivery_order_status_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `driver_eksternal` | `varchar(191)` | YES | `NULL` | — | — |
| `vehicle_eksternal` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** delivery_order_drivers_cancelled_by_foreign: cancelled_by; delivery_order_drivers_create_by_foreign: create_by; delivery_order_drivers_depo_awal_id_foreign: depo_awal_id; delivery_order_drivers_depo_tujuan_id_foreign: depo_tujuan_id; delivery_order_drivers_dock_awal_id_foreign: dock_awal_id; delivery_order_drivers_dock_tujuan_id_foreign: dock_tujuan_id; delivery_order_drivers_driver_id_foreign: driver_id; delivery_order_drivers_from_address_id_foreign: from_address_id; delivery_order_drivers_from_id_foreign: from_id; delivery_order_drivers_job_status_id_index: job_status_id; delivery_order_drivers_to_address_id_foreign: to_address_id; delivery_order_drivers_to_id_foreign: to_id; delivery_order_drivers_vehicle_id_foreign: vehicle_id; delivery_order_drivers_vendor_id_foreign: vendor_id; PRIMARY (UNIQUE): id.  
**Foreign key:** delivery_order_drivers_cancelled_by_foreign (cancelled_by → users.id); delivery_order_drivers_create_by_foreign (create_by → users.id); delivery_order_drivers_depo_awal_id_foreign (depo_awal_id → depo_containers.id); delivery_order_drivers_depo_tujuan_id_foreign (depo_tujuan_id → depo_containers.id); delivery_order_drivers_dock_awal_id_foreign (dock_awal_id → docks.id); delivery_order_drivers_dock_tujuan_id_foreign (dock_tujuan_id → docks.id); delivery_order_drivers_driver_id_foreign (driver_id → contacts.id); delivery_order_drivers_from_address_id_foreign (from_address_id → contacts.id); delivery_order_drivers_from_id_foreign (from_id → contacts.id); delivery_order_drivers_to_address_id_foreign (to_address_id → contacts.id); delivery_order_drivers_to_id_foreign (to_id → contacts.id); delivery_order_drivers_vehicle_id_foreign (vehicle_id → vehicles.id); delivery_order_drivers_vendor_id_foreign (vendor_id → contacts.id).

### `delivery_order_driver_documents` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `delivery_order_driver_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `file` | `varchar(191)` | NO | `—` | — | — |
| `filename` | `varchar(191)` | NO | `—` | — | — |
| `job_order_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** delivery_order_driver_documents_delivery_order_driver_id_index: delivery_order_driver_id; PRIMARY (UNIQUE): id.  
**Foreign key:** delivery_order_driver_documents_delivery_order_driver_id_foreign (delivery_order_driver_id → delivery_order_drivers.id).

### `delivery_order_ongoing_jobs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `delivery_order_driver_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_order_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** delivery_order_ongoing_jobs_delivery_order_driver_id_index: delivery_order_driver_id; delivery_order_ongoing_jobs_job_order_id_index: job_order_id; PRIMARY (UNIQUE): id.  
**Foreign key:** delivery_order_ongoing_jobs_delivery_order_driver_id_foreign (delivery_order_driver_id → delivery_order_drivers.id); delivery_order_ongoing_jobs_job_order_id_foreign (job_order_id → job_orders.id).

### `delivery_order_photos` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `receipt_id` | `int(11)` | NO | `—` | — | — |
| `name` | `varchar(300)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `delivery_order_routes` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `delivery_order_driver_id` | `int(10) unsigned` | NO | `—` | — | — |
| `depo_id` | `varchar(191)` | YES | `NULL` | — | — |
| `dock_id` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_id` | `varchar(191)` | YES | `NULL` | — | — |
| `priority` | `int(11)` | NO | `—` | — | — |
| `type` | `varchar(191)` | YES | `NULL` | — | — |
| `location_name` | `varchar(191)` | YES | `NULL` | — | — |
| `location_address` | `varchar(191)` | YES | `NULL` | — | — |
| `latitude` | `varchar(191)` | NO | `—` | — | — |
| `longitude` | `varchar(191)` | NO | `—` | — | — |
| `raw_here_map` | `text` | YES | `NULL` | — | — |
| `is_finished` | `tinyint(4)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `job_order_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `delivery_order_statuses` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `is_start` | `tinyint(4)` | NO | `—` | — | — |
| `is_progress` | `tinyint(4)` | NO | `—` | — | — |
| `is_finish` | `tinyint(4)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `delivery_order_status_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `delivery_order_driver_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_status_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `datetime` | NO | `current_timestamp()` | — | — |
| `job_order_id` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_by_contact` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** delivery_order_status_logs_created_by_index: created_by; delivery_order_status_logs_delivery_order_driver_id_index: delivery_order_driver_id; delivery_order_status_logs_job_status_id_index: job_status_id; PRIMARY (UNIQUE): id.  
**Foreign key:** delivery_order_status_logs_created_by_foreign (created_by → users.id); delivery_order_status_logs_delivery_order_driver_id_foreign (delivery_order_driver_id → delivery_order_drivers.id); delivery_order_status_logs_job_status_id_foreign (job_status_id → job_statuses.id).

### `delivery_reject_histories` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `delivery_order_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `driver_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `lat` | `varchar(191)` | YES | `NULL` | — | — |
| `lng` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** delivery_reject_histories_delivery_order_id_foreign: delivery_order_id; delivery_reject_histories_driver_id_foreign: driver_id; PRIMARY (UNIQUE): id.  
**Foreign key:** delivery_reject_histories_delivery_order_id_foreign (delivery_order_id → delivery_order_drivers.id); delivery_reject_histories_driver_id_foreign (driver_id → contacts.id).

### `departments` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | UNI | — |
| `name` | `varchar(191)` | NO | `—` | UNI | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** departments_code_unique (UNIQUE): code; departments_name_unique (UNIQUE): name; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `depo_containers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `service_time` | `int(11)` | NO | `—` | — | — |
| `port_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | YES | `NULL` | — | — |
| `polygon` | `longtext` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `address` | `varchar(191)` | YES | `NULL` | — | — |
| `is_active` | `tinyint(4)` | NO | `1` | — | — |

**Indeks:** depo_containers_port_id_foreign: port_id; PRIMARY (UNIQUE): id.  
**Foreign key:** depo_containers_port_id_foreign (port_id → ports.id).

### `docks` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `service_time` | `int(11)` | NO | `—` | — | — |
| `port_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | YES | `NULL` | — | — |
| `polygon` | `longtext` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `address` | `varchar(191)` | YES | `NULL` | — | — |
| `is_active` | `tinyint(4)` | NO | `1` | — | — |

**Indeks:** docks_port_id_foreign: port_id; PRIMARY (UNIQUE): id.  
**Foreign key:** docks_port_id_foreign (port_id → ports.id).

### `driver_messages` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `driver_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `message` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** driver_messages_driver_id_foreign: driver_id; PRIMARY (UNIQUE): id.  
**Foreign key:** driver_messages_driver_id_foreign (driver_id → contacts.id).

### `driver_ritase_points` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `km_start` | `int(11)` | NO | `—` | — | — |
| `km_end` | `int(11)` | NO | `—` | — | — |
| `ritase_point` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `driver_ritase_point_options` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `emails` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(100)` | YES | `NULL` | — | — |
| `mail_driver` | `varchar(100)` | YES | `NULL` | — | — |
| `host` | `varchar(100)` | YES | `NULL` | — | — |
| `port` | `int(11)` | NO | `0` | — | — |
| `username` | `varchar(100)` | YES | `NULL` | — | — |
| `password` | `varchar(100)` | YES | `NULL` | — | — |
| `encryption` | `varchar(10)` | YES | `NULL` | — | — |
| `receipt_subject` | `varchar(100)` | YES | `NULL` | — | — |
| `receipt_body` | `varchar(100)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `shipment_subject` | `varchar(100)` | YES | `NULL` | — | — |
| `shipment_body` | `varchar(100)` | YES | `NULL` | — | — |
| `from_email` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `email_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `subject` | `varchar(100)` | YES | `NULL` | — | — |
| `destination` | `text` | NO | `—` | — | — |
| `body` | `text` | YES | `NULL` | — | — |
| `status` | `varchar(10)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `datetime` | NO | `—` | — | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `field_types` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(15)` | NO | `—` | MUL | — |
| `name` | `varchar(50)` | NO | `—` | — | — |

**Indeks:** field_types_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `gate_activities` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `gate_activity_types` — 5 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(30)` | NO | `—` | MUL | — |
| `name` | `varchar(100)` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** gate_activity_types_name_index: name; gate_activity_types_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `gate_in_containers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `owner_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `container_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(100)` | NO | `—` | MUL | — |
| `date` | `datetime` | NO | `—` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `no_container` | `varchar(100)` | NO | `—` | — | — |
| `container_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `status` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** gate_in_containers_code_index: code; gate_in_containers_company_id_index: company_id; gate_in_containers_container_id_index: container_id; gate_in_containers_container_type_id_index: container_type_id; gate_in_containers_created_by_index: created_by; gate_in_containers_date_index: date; gate_in_containers_owner_id_index: owner_id; gate_in_containers_status_index: status; PRIMARY (UNIQUE): id.  
**Foreign key:** gate_in_containers_company_id_foreign (company_id → companies.id); gate_in_containers_container_type_id_foreign (container_type_id → container_types.id); gate_in_containers_created_by_foreign (created_by → users.id); gate_in_containers_owner_id_foreign (owner_id → contacts.id).

### `gate_in_container_statuses` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `order` | `smallint(6)` | NO | `0` | MUL | — |
| `name` | `varchar(20)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** gate_in_container_statuses_order_index: order; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `generate_costs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cost_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `driver_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `helper_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_start` | `date` | NO | `—` | — | — |
| `date_end` | `date` | NO | `—` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `status` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | NO | `current_timestamp()` | — | — |
| `updated_at` | `timestamp` | NO | `current_timestamp()` | — | — |

**Indeks:** generate_costs_company_id_foreign: company_id; generate_costs_cost_type_id_foreign: cost_type_id; generate_costs_driver_id_foreign: driver_id; generate_costs_helper_id_foreign: helper_id; generate_costs_journal_id_foreign: journal_id; generate_costs_vehicle_id_foreign: vehicle_id; generate_costs_vendor_id_foreign: vendor_id; PRIMARY (UNIQUE): id.  
**Foreign key:** generate_costs_company_id_foreign (company_id → companies.id); generate_costs_cost_type_id_foreign (cost_type_id → cost_types.id); generate_costs_driver_id_foreign (driver_id → contacts.id); generate_costs_helper_id_foreign (helper_id → contacts.id); generate_costs_journal_id_foreign (journal_id → journals.id); generate_costs_vehicle_id_foreign (vehicle_id → vehicles.id); generate_costs_vendor_id_foreign (vendor_id → contacts.id).

### `group_roles` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `group_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `role_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** group_roles_group_type_id_foreign: group_type_id; group_roles_role_id_foreign: role_id; PRIMARY (UNIQUE): id.  
**Foreign key:** group_roles_group_type_id_foreign (group_type_id → group_types.id); group_roles_role_id_foreign (role_id → roles.id).

### `group_types` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `dashboard_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** group_types_dashboard_id_foreign: dashboard_id; PRIMARY (UNIQUE): id.  
**Foreign key:** group_types_dashboard_id_foreign (dashboard_id → dashboards.id).

### `handlings` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(11)` | NO | `—` | — | — |
| `job_order_id` | `int(11)` | NO | `—` | — | — |
| `is_overtime` | `int(11)` | NO | `0` | — | — |
| `start_time` | `time` | NO | `'00:00:00'` | — | — |
| `end_time` | `time` | NO | `'00:00:00'` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `description` | `text` | NO | `—` | — | — |
| `staff_gudang_name` | `varchar(200)` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `handling_vehicles` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `handling_id` | `int(11)` | NO | `—` | — | — |
| `space_type` | `varchar(30)` | NO | `—` | — | — |
| `no_seal` | `varchar(100)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `type` | `varchar(10)` | YES | `NULL` | — | — |
| `carrier_name` | `varchar(100)` | NO | `—` | — | — |
| `carrier_size` | `int(11)` | NO | `0` | — | — |
| `driver_name` | `varchar(200)` | NO | `—` | — | — |
| `no_carrier` | `varchar(100)` | NO | `—` | — | — |
| `no_container` | `varchar(100)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `impositions` — 4 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `slug` | `varchar(20)` | NO | `—` | MUL | — |

**Indeks:** impositions_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `industries` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |

**Indeks:** industries_create_by_foreign: create_by; PRIMARY (UNIQUE): id.  
**Foreign key:** industries_create_by_foreign (create_by → users.id).

### `inqueries` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `sales_opportunity_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `sales_inquery_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `quotation_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `customer_stage_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `inquery_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `opportunity_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code_inquery` | `varchar(191)` | YES | `NULL` | — | — |
| `code_opportunity` | `varchar(191)` | YES | `NULL` | — | — |
| `date_inquery` | `date` | YES | `NULL` | — | — |
| `date_opportunity` | `date` | YES | `NULL` | — | — |
| `date_quotation` | `date` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description_inquery` | `text` | YES | `NULL` | — | — |
| `description_opportunity` | `text` | YES | `NULL` | — | — |
| `type_send` | `int(11)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `cancel_opportunity_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_opportunity_date` | `datetime` | YES | `NULL` | — | — |
| `cancel_inquery_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_inquery_date` | `datetime` | YES | `NULL` | — | — |
| `interest` | `varchar(191)` | YES | `NULL` | — | — |
| `lead_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `inquery_customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** inqueries_cancel_inquery_by_foreign: cancel_inquery_by; inqueries_cancel_opportunity_by_foreign: cancel_opportunity_by; inqueries_company_id_foreign: company_id; inqueries_create_by_foreign: create_by; inqueries_customer_id_foreign: customer_id; inqueries_customer_stage_id_foreign: customer_stage_id; inqueries_inquery_by_foreign: inquery_by; inqueries_inquery_customer_id_foreign: inquery_customer_id; inqueries_lead_id_foreign: lead_id; inqueries_opportunity_id_foreign: opportunity_id; inqueries_quotation_id_foreign: quotation_id; inqueries_sales_inquery_id_foreign: sales_inquery_id; inqueries_sales_opportunity_id_foreign: sales_opportunity_id; PRIMARY (UNIQUE): id.  
**Foreign key:** inqueries_cancel_inquery_by_foreign (cancel_inquery_by → users.id); inqueries_cancel_opportunity_by_foreign (cancel_opportunity_by → users.id); inqueries_company_id_foreign (company_id → companies.id); inqueries_create_by_foreign (create_by → users.id); inqueries_customer_id_foreign (customer_id → contacts.id); inqueries_customer_stage_id_foreign (customer_stage_id → customer_stages.id); inqueries_inquery_by_foreign (inquery_by → users.id); inqueries_inquery_customer_id_foreign (inquery_customer_id → inquery_customers.id); inqueries_lead_id_foreign (lead_id → leads.id); inqueries_opportunity_id_foreign (opportunity_id → inqueries.id); inqueries_quotation_id_foreign (quotation_id → quotations.id); inqueries_sales_inquery_id_foreign (sales_inquery_id → contacts.id); inqueries_sales_opportunity_id_foreign (sales_opportunity_id → contacts.id).

### `inquery_activities` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `sales_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `customer_stage_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `date_activity` | `date` | YES | `NULL` | — | — |
| `is_done` | `tinyint(1)` | NO | `0` | — | — |
| `is_opportunity` | `tinyint(1)` | NO | `1` | — | — |
| `date_done` | `date` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `file_name` | `varchar(191)` | YES | `NULL` | — | — |
| `extension` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `inquery_customers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `file_name` | `varchar(191)` | YES | `NULL` | — | — |
| `file_extension` | `varchar(191)` | YES | `NULL` | — | — |
| `is_done` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** inquery_customers_customer_id_foreign: customer_id; PRIMARY (UNIQUE): id.  
**Foreign key:** inquery_customers_customer_id_foreign (customer_id → contacts.id).

### `invoices` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_cash_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_receivable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_selling_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `receivable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `collectible_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `tax_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `termin` | `int(11)` | YES | `NULL` | — | — |
| `terms` | `varchar(191)` | YES | `NULL` | — | — |
| `date_invoice` | `date` | NO | `—` | — | — |
| `due_date` | `date` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `sub_total` | `double` | NO | `0` | — | — |
| `discount_percent` | `double` | NO | `0` | — | — |
| `discount_total` | `double` | NO | `0` | — | — |
| `is_ppn` | `tinyint(1)` | NO | `—` | — | — |
| `total_another_ppn` | `double` | NO | `0` | — | — |
| `grand_total` | `double` | NO | `0` | — | — |
| `sub_total_additional` | `double` | NO | `0` | — | — |
| `discount_percent_additional` | `double` | NO | `0` | — | — |
| `discount_total_additional` | `double` | NO | `0` | — | — |
| `grand_total_additional` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `type_bayar` | `tinyint(1)` | NO | `1` | — | — |
| `is_approve` | `tinyint(1)` | NO | `0` | — | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_approve` | `datetime` | YES | `NULL` | — | — |
| `journal_date` | `date` | YES | `NULL` | — | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |
| `is_join` | `tinyint(1)` | NO | `0` | — | — |
| `serial` | `int(10) unsigned` | YES | `NULL` | — | — |
| `printed_amount` | `varchar(100)` | YES | `NULL` | — | — |
| `qty_edit` | `int(11)` | NO | `0` | MUL | — |
| `qty_batal_posting` | `int(11)` | NO | `0` | MUL | — |
| `is_npwp` | `int(11)` | NO | `0` | — | — |
| `ppn` | `int(11)` | NO | `0` | — | — |
| `is_taxinvoice` | `tinyint(1)` | NO | `—` | — | — |
| `setting_tax_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** invoices_account_cash_id_foreign: account_cash_id; invoices_account_receivable_id_foreign: account_receivable_id; invoices_account_selling_id_foreign: account_selling_id; invoices_approve_by_foreign: approve_by; invoices_company_id_foreign: company_id; invoices_create_by_foreign: create_by; invoices_customer_id_foreign: customer_id; invoices_journal_id_foreign: journal_id; invoices_qty_batal_posting_index: qty_batal_posting; invoices_qty_edit_index: qty_edit; invoices_receivable_id_foreign: receivable_id; invoices_tax_id_foreign: tax_id; invoices_type_transaction_id_foreign: type_transaction_id; PRIMARY (UNIQUE): id.  
**Foreign key:** invoices_account_cash_id_foreign (account_cash_id → accounts.id); invoices_account_receivable_id_foreign (account_receivable_id → accounts.id); invoices_account_selling_id_foreign (account_selling_id → accounts.id); invoices_approve_by_foreign (approve_by → users.id); invoices_company_id_foreign (company_id → companies.id); invoices_create_by_foreign (create_by → users.id); invoices_customer_id_foreign (customer_id → contacts.id); invoices_journal_id_foreign (journal_id → journals.id); invoices_receivable_id_foreign (receivable_id → receivables.id); invoices_tax_id_foreign (tax_id → taxes.id); invoices_type_transaction_id_foreign (type_transaction_id → type_transactions.id).

### `invoice_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `job_order_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `work_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `job_order_cost_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cost_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |
| `imposition` | `int(11)` | YES | `NULL` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `is_other_cost` | `tinyint(1)` | NO | `0` | — | — |
| `type_other_cost` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `manifest_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `imposition_name` | `varchar(191)` | YES | `NULL` | — | — |
| `commodity_name` | `varchar(191)` | YES | `NULL` | — | — |
| `discount` | `double` | NO | `0` | — | — |
| `is_ppn` | `tinyint(1)` | NO | `0` | — | — |
| `ppn` | `double` | NO | `0` | — | — |
| `service_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `total_tax` | `double` | YES | `0` | — | — |

**Indeks:** invoice_details_cost_type_id_foreign: cost_type_id; invoice_details_create_by_foreign: create_by; invoice_details_header_id_foreign: header_id; invoice_details_job_order_detail_id_foreign: job_order_detail_id; invoice_details_job_order_id_foreign: job_order_id; invoice_details_manifest_id_foreign: manifest_id; invoice_details_service_id_index: service_id; invoice_details_work_order_id_foreign: work_order_id; PRIMARY (UNIQUE): id.  
**Foreign key:** invoice_details_cost_type_id_foreign (cost_type_id → cost_types.id); invoice_details_create_by_foreign (create_by → users.id); invoice_details_header_id_foreign (header_id → invoices.id); invoice_details_job_order_detail_id_foreign (job_order_detail_id → job_order_details.id); invoice_details_job_order_id_foreign (job_order_id → job_orders.id); invoice_details_manifest_id_foreign (manifest_id → manifests.id); invoice_details_service_id_foreign (service_id → services.id); invoice_details_work_order_id_foreign (work_order_id → work_orders.id).

### `invoice_job_order` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `invoice_id` | `int(10) unsigned` | NO | `—` | PRI | — |
| `job_order_id` | `int(10) unsigned` | NO | `—` | PRI | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** invoice_job_order_job_order_id_foreign: job_order_id; PRIMARY (UNIQUE): invoice_id, job_order_id.  
**Foreign key:** invoice_job_order_invoice_id_foreign (invoice_id → invoices.id); invoice_job_order_job_order_id_foreign (job_order_id → job_orders.id).

### `invoice_joins` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `serial` | `int(10) unsigned` | NO | `—` | — | — |
| `invoice_id` | `int(10) unsigned` | NO | `—` | — | — |
| `type_wo` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `invoice_taxes` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `tax_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `amount` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `invoice_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_request` | `int(11)` | YES | `0` | — | — |
| `value_pajak` | `int(11)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `invoice_vendors` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vendor_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_invoice` | `date` | NO | `—` | — | — |
| `date_receive` | `date` | NO | `—` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |
| `status_approve` | `int(11)` | NO | `0` | — | — |
| `due_date` | `date` | NO | `—` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `payable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `subtotal` | `double` | NO | `0` | — | — |
| `ppn` | `double` | NO | `0` | — | — |
| `ppn_is_faktur` | `tinyint(1)` | NO | `1` | — | — |
| `is_vehicle_maintenance` | `tinyint(1)` | NO | `0` | — | — |
| `is_good_receipt` | `tinyint(1)` | NO | `0` | — | — |
| `total_discount` | `double` | NO | `0` | — | — |
| `total_pph` | `double` | NO | `0` | — | — |
| `is_finance_vendor_bills` | `tinyint(1)` | NO | `0` | — | — |
| `no_faktur_pajak` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** invoice_vendors_company_id_foreign: company_id; invoice_vendors_create_by_foreign: create_by; invoice_vendors_journal_id_index: journal_id; invoice_vendors_payable_id_index: payable_id; invoice_vendors_vendor_id_foreign: vendor_id; PRIMARY (UNIQUE): id.  
**Foreign key:** invoice_vendors_company_id_foreign (company_id → companies.id); invoice_vendors_create_by_foreign (create_by → users.id); invoice_vendors_journal_id_foreign (journal_id → journals.id); invoice_vendors_payable_id_foreign (payable_id → payables.id); invoice_vendors_vendor_id_foreign (vendor_id → contacts.id).

### `invoice_vendor_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_id` | `int(11)` | NO | `0` | — | — |
| `cash_categories_id` | `int(11)` | NO | `0` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `diskon` | `double` | NO | `0` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `total_origin` | `double` | NO | `0` | — | — |
| `manifest_cost_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `job_order_cost_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `payable_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `ppn` | `double` | NO | `0` | — | — |
| `vehicle_maintenance_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `item_name` | `varchar(191)` | YES | `NULL` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** invoice_vendor_details_header_id_foreign: header_id; invoice_vendor_details_job_order_cost_id_foreign: job_order_cost_id; invoice_vendor_details_manifest_cost_id_foreign: manifest_cost_id; invoice_vendor_details_payable_detail_id_foreign: payable_detail_id; invoice_vendor_details_vehicle_maintenance_id_foreign: vehicle_maintenance_id; PRIMARY (UNIQUE): id.  
**Foreign key:** invoice_vendor_details_header_id_foreign (header_id → invoice_vendors.id); invoice_vendor_details_job_order_cost_id_foreign (job_order_cost_id → job_order_costs.id); invoice_vendor_details_manifest_cost_id_foreign (manifest_cost_id → manifest_costs.id); invoice_vendor_details_payable_detail_id_foreign (payable_detail_id → payable_details.id); invoice_vendor_details_vehicle_maintenance_id_foreign (vehicle_maintenance_id → vehicle_maintenances.id).

### `invoice_vendor_taxes` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `tax_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `amount` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** invoice_vendor_taxes_detail_id_foreign: detail_id; invoice_vendor_taxes_header_id_foreign: header_id; invoice_vendor_taxes_tax_id_foreign: tax_id; PRIMARY (UNIQUE): id.  
**Foreign key:** invoice_vendor_taxes_detail_id_foreign (detail_id → invoice_vendor_details.id); invoice_vendor_taxes_header_id_foreign (header_id → invoice_vendors.id); invoice_vendor_taxes_tax_id_foreign (tax_id → taxes.id).

### `items` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `category_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `tire_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `tire_size_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `tire_manufacture_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `part_number` | `varchar(191)` | YES | `NULL` | — | — |
| `sku` | `varchar(191)` | YES | `NULL` | — | — |
| `barcode` | `varchar(191)` | YES | `NULL` | — | — |
| `qrcode` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `image` | `varchar(191)` | YES | `NULL` | — | — |
| `initial_cost` | `double` | NO | `0` | — | — |
| `harga_beli` | `double` | NO | `0` | — | — |
| `harga_jual` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_purchase_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_purchase_retur_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_sale_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_sale_retur_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `main_supplier_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `minimal_stock` | `double(20,2)` | NO | `0.00` | — | — |
| `std_purchase` | `double(20,2)` | NO | `0.00` | — | — |
| `std_sale` | `double(20,2)` | NO | `0.00` | — | — |
| `is_stock` | `tinyint(1)` | NO | `1` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |
| `is_generate` | `tinyint(1)` | NO | `0` | — | — |
| `last_number` | `int(11)` | NO | `0` | — | — |
| `is_package` | `int(11)` | NO | `0` | — | — |
| `customer_id` | `int(11)` | YES | `NULL` | — | — |
| `long` | `double` | NO | `0` | — | — |
| `wide` | `double` | NO | `0` | — | — |
| `height` | `double` | NO | `0` | — | — |
| `volume` | `double` | NO | `0` | — | — |
| `v1` | `double` | YES | `0` | — | — |
| `tebal_v1` | `double` | YES | `0` | — | — |
| `v2` | `double` | YES | `0` | — | — |
| `tebal_v2` | `double` | YES | `0` | — | — |
| `sender_id` | `int(11)` | YES | `NULL` | — | — |
| `receiver_id` | `int(11)` | YES | `NULL` | — | — |
| `inbound_date` | `date` | YES | `NULL` | — | — |
| `tonase` | `int(11)` | NO | `0` | — | — |
| `account_payable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_cash_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_accrual` | `int(11)` | NO | `1` | — | — |
| `item_type` | `int(11)` | NO | `1` | — | — |
| `is_service` | `int(11)` | NO | `0` | — | — |
| `is_cost` | `tinyint(4)` | NO | `0` | — | — |
| `is_expired` | `int(11)` | NO | `0` | — | — |
| `is_bbm` | `int(11)` | NO | `0` | — | — |
| `is_operational` | `int(11)` | NO | `0` | — | — |
| `is_invoice` | `int(11)` | NO | `0` | — | — |
| `is_overtime` | `int(11)` | NO | `0` | — | — |
| `is_ppn` | `int(11)` | NO | `0` | — | — |
| `vendor_path_no` | `varchar(191)` | YES | `NULL` | — | — |
| `brand_name` | `varchar(191)` | YES | `NULL` | — | — |
| `is_dangerous_good` | `smallint(6)` | NO | `0` | MUL | — |
| `is_fast_moving` | `smallint(6)` | NO | `0` | MUL | — |
| `is_merchandise` | `tinyint(1)` | NO | `0` | — | — |
| `default_rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `tire_category_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_usage` | `int(11)` | YES | `NULL` | — | — |
| `cost_type_id` | `bigint(20) unsigned` | YES | `NULL` | — | — |

**Indeks:** items_account_cash_id_foreign: account_cash_id; items_account_id_foreign: account_id; items_account_payable_id_foreign: account_payable_id; items_account_purchase_id_foreign: account_purchase_id; items_account_purchase_retur_id_foreign: account_purchase_retur_id; items_account_sale_id_foreign: account_sale_id; items_account_sale_retur_id_foreign: account_sale_retur_id; items_category_id_foreign: category_id; items_default_rack_id_index: default_rack_id; items_is_dangerous_good_index: is_dangerous_good; items_is_fast_moving_index: is_fast_moving; items_main_supplier_id_foreign: main_supplier_id; items_piece_id_foreign: piece_id; items_tire_category_id_foreign: tire_category_id; items_tire_manufacture_id_foreign: tire_manufacture_id; items_tire_size_id_foreign: tire_size_id; items_tire_type_id_foreign: tire_type_id; PRIMARY (UNIQUE): id.  
**Foreign key:** items_account_cash_id_foreign (account_cash_id → accounts.id); items_account_id_foreign (account_id → accounts.id); items_account_payable_id_foreign (account_payable_id → accounts.id); items_account_purchase_id_foreign (account_purchase_id → accounts.id); items_account_purchase_retur_id_foreign (account_purchase_retur_id → accounts.id); items_account_sale_id_foreign (account_sale_id → accounts.id); items_account_sale_retur_id_foreign (account_sale_retur_id → accounts.id); items_category_id_foreign (category_id → categories.id); items_default_rack_id_foreign (default_rack_id → racks.id); items_main_supplier_id_foreign (main_supplier_id → contacts.id); items_piece_id_foreign (piece_id → pieces.id); items_tire_category_id_foreign (tire_category_id → tire_categories.id); items_tire_manufacture_id_foreign (tire_manufacture_id → tire_manufacturers.id); items_tire_size_id_foreign (tire_size_id → tire_sizes.id); items_tire_type_id_foreign (tire_type_id → tire_types.id).

### `item_conditions` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(100)` | NO | `—` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** item_conditions_name_index: name; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `item_deletions` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `date_cancel` | `date` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** item_deletions_approve_by_foreign: approve_by; item_deletions_cancel_by_foreign: cancel_by; item_deletions_create_by_foreign: create_by; item_deletions_journal_id_foreign: journal_id; item_deletions_warehouse_id_foreign: warehouse_id; PRIMARY (UNIQUE): id.  
**Foreign key:** item_deletions_approve_by_foreign (approve_by → users.id); item_deletions_cancel_by_foreign (cancel_by → users.id); item_deletions_create_by_foreign (create_by → users.id); item_deletions_journal_id_foreign (journal_id → journals.id); item_deletions_warehouse_id_foreign (warehouse_id → warehouses.id).

### `item_deletion_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `qty` | `int(11)` | NO | `0` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `rack_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `outbound_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** item_deletion_details_item_id_index: item_id; item_deletion_details_outbound_stock_transaction_id_index: outbound_stock_transaction_id; item_deletion_details_rack_id_index: rack_id; item_deletion_details_requested_stock_transaction_id_index: requested_stock_transaction_id; item_deletion_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** item_deletion_details_item_id_foreign (item_id → items.id); item_deletion_details_outbound_stock_transaction_id_foreign (outbound_stock_transaction_id → stock_transactions.id); item_deletion_details_rack_id_foreign (rack_id → racks.id); item_deletion_details_requested_stock_transaction_id_foreign (requested_stock_transaction_id → stock_transactions.id); item_deletion_details_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `item_deletion_statuses` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | — |
| `name` | `varchar(50)` | NO | `—` | — | — |

**Indeks:** item_deletion_statuses_id_unique (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `item_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `po_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `deletion_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `batch_no` | `varchar(191)` | NO | `—` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_tire` | `tinyint(4)` | NO | `0` | — | — |
| `tire_km_used` | `double(20,2)` | NO | `0.00` | — | — |

**Indeks:** item_details_item_id_foreign: item_id; item_details_po_id_foreign: po_id; item_details_rack_id_foreign: rack_id; item_details_warehouse_id_foreign: warehouse_id; PRIMARY (UNIQUE): id.  
**Foreign key:** item_details_item_id_foreign (item_id → items.id); item_details_po_id_foreign (po_id → purchase_orders.id); item_details_rack_id_foreign (rack_id → racks.id); item_details_warehouse_id_foreign (warehouse_id → warehouses.id).

### `item_migrations` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_from_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `rack_from_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_to_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `rack_to_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `date_cancel` | `date` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `cancel_reason` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `no_surat_jalan` | `varchar(100)` | YES | `NULL` | — | — |
| `is_inventory` | `int(11)` | NO | `0` | — | — |
| `warehouse_receipt_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `item_migration_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** item_migrations_approve_by_foreign: approve_by; item_migrations_cancel_by_foreign: cancel_by; item_migrations_create_by_foreign: create_by; item_migrations_item_migration_type_id_index: item_migration_type_id; item_migrations_rack_from_id_foreign: rack_from_id; item_migrations_rack_to_id_foreign: rack_to_id; item_migrations_warehouse_from_id_foreign: warehouse_from_id; item_migrations_warehouse_receipt_id_index: warehouse_receipt_id; item_migrations_warehouse_to_id_foreign: warehouse_to_id; PRIMARY (UNIQUE): id.  
**Foreign key:** item_migrations_approve_by_foreign (approve_by → users.id); item_migrations_cancel_by_foreign (cancel_by → users.id); item_migrations_create_by_foreign (create_by → users.id); item_migrations_item_migration_type_id_foreign (item_migration_type_id → item_migration_types.id); item_migrations_rack_from_id_foreign (rack_from_id → racks.id); item_migrations_rack_to_id_foreign (rack_to_id → racks.id); item_migrations_warehouse_from_id_foreign (warehouse_from_id → warehouses.id); item_migrations_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id); item_migrations_warehouse_to_id_foreign (warehouse_to_id → warehouses.id).

### `item_migration_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | — | — |
| `qty` | `double` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `no_surat_jalan` | `varchar(100)` | YES | `NULL` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `destination_rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `outbound_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `inbound_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `destination_warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** item_migration_details_destination_rack_id_index: destination_rack_id; item_migration_details_destination_warehouse_id_index: destination_warehouse_id; item_migration_details_inbound_stock_transaction_id_index: inbound_stock_transaction_id; item_migration_details_outbound_stock_transaction_id_index: outbound_stock_transaction_id; item_migration_details_rack_id_index: rack_id; item_migration_details_requested_stock_transaction_id_index: requested_stock_transaction_id; item_migration_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** item_migration_details_destination_warehouse_id_foreign (destination_warehouse_id → warehouses.id); item_migration_details_inbound_stock_transaction_id_foreign (inbound_stock_transaction_id → stock_transactions.id); item_migration_details_outbound_stock_transaction_id_foreign (outbound_stock_transaction_id → stock_transactions.id); item_migration_details_requested_stock_transaction_id_foreign (requested_stock_transaction_id → stock_transactions.id); item_migration_details_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `item_migration_receipts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `item_migration_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_receipt_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** item_migration_receipts_item_migration_id_index: item_migration_id; item_migration_receipts_warehouse_receipt_id_index: warehouse_receipt_id; PRIMARY (UNIQUE): id.  
**Foreign key:** item_migration_receipts_item_migration_id_foreign (item_migration_id → item_migrations.id); item_migration_receipts_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id).

### `item_migration_statuses` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(30)` | NO | `—` | MUL | — |
| `name` | `varchar(100)` | NO | `—` | MUL | — |

**Indeks:** item_migration_statuses_name_index: name; item_migration_statuses_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `item_migration_types` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(20)` | NO | `—` | MUL | — |

**Indeks:** item_migration_types_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `item_pictures` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `file_path` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** item_pictures_item_id_foreign: item_id; PRIMARY (UNIQUE): id.  
**Foreign key:** item_pictures_item_id_foreign (item_id → items.id).

### `jenis_ban` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(30)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `job_orders` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `price_list_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `route_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `transaction_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `service_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `service_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `sender_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `receiver_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `quotation_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `quotation_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_temp_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `collectible_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `work_order_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `receivable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `kpi_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `shipment_date` | `datetime` | YES | `NULL` | — | — |
| `shipment_done` | `datetime` | YES | `NULL` | — | — |
| `duration` | `double` | NO | `1` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `total_unit` | `double(20,2)` | NO | `1.00` | — | — |
| `total_item` | `int(11)` | NO | `0` | — | — |
| `is_cancel` | `tinyint(1)` | NO | `0` | — | — |
| `cancel_date` | `date` | YES | `NULL` | — | — |
| `cancel_description` | `text` | YES | `NULL` | — | — |
| `is_manifest` | `tinyint(1)` | NO | `0` | — | — |
| `is_done` | `tinyint(1)` | NO | `0` | — | — |
| `code_invoice` | `varchar(191)` | YES | `NULL` | — | — |
| `date_invoice` | `date` | YES | `NULL` | — | — |
| `no_po_customer` | `varchar(191)` | YES | `NULL` | — | — |
| `no_bl` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `moda_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `container_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `docs_no` | `varchar(191)` | YES | `NULL` | — | — |
| `docs_reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `piece_name` | `varchar(191)` | YES | `NULL` | — | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `work_order_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `aju_number` | `varchar(191)` | YES | `NULL` | — | — |
| `submit` | `int(11)` | NO | `1` | — | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_staff_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `imposition` | `int(11)` | YES | `NULL` | — | — |
| `is_operational_done` | `tinyint(1)` | NO | `0` | — | — |
| `vessel_name` | `varchar(191)` | YES | `NULL` | — | — |
| `voyage_no` | `varchar(191)` | YES | `NULL` | — | — |
| `document_name` | `varchar(191)` | YES | `NULL` | — | — |
| `is_handling` | `int(11)` | NO | `0` | — | — |
| `is_warehouse` | `int(11)` | NO | `0` | — | — |
| `is_packaging` | `int(11)` | NO | `0` | — | — |
| `is_warehouserent` | `int(11)` | NO | `0` | — | — |
| `is_stuffing` | `int(11)` | NO | `0` | — | — |
| `uniqid` | `varchar(191)` | YES | `NULL` | — | — |
| `warehouse_receipt_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `agent_name` | `varchar(100)` | YES | `NULL` | — | — |
| `awb_number` | `varchar(100)` | YES | `NULL` | — | — |
| `flight_code` | `varchar(100)` | YES | `NULL` | — | — |
| `flight_route` | `varchar(100)` | YES | `NULL` | — | — |
| `flight_date` | `date` | YES | `NULL` | — | — |
| `cargo_ready_date` | `date` | YES | `NULL` | — | — |
| `house_awb` | `varchar(100)` | YES | `NULL` | — | — |
| `hs_code` | `varchar(100)` | YES | `NULL` | — | — |
| `additional` | `longtext` | YES | `NULL` | — | — |
| `is_invoiced` | `tinyint(1)` | NO | `0` | — | — |
| `sales_order_code` | `varchar(191)` | YES | `NULL` | — | — |
| `depo_awal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `depo_tujuan_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `dock_awal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `dock_tujuan_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `start_window_time` | `timestamp` | YES | `NULL` | — | — |
| `end_window_time` | `timestamp` | YES | `NULL` | — | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |
| `is_planning` | `int(11)` | NO | `0` | — | — |
| `is_loco` | `int(11)` | NO | `0` | — | — |
| `customer_job_order_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_approve` | `tinyint(4)` | YES | `0` | — | — |
| `approved_by` | `int(11)` | YES | `NULL` | — | — |
| `date_approve` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** job_orders_cancel_by_foreign: cancel_by; job_orders_collectible_id_foreign: collectible_id; job_orders_commodity_id_foreign: commodity_id; job_orders_company_id_foreign: company_id; job_orders_container_type_id_foreign: container_type_id; job_orders_create_by_foreign: create_by; job_orders_customer_id_foreign: customer_id; job_orders_depo_awal_id_foreign: depo_awal_id; job_orders_depo_tujuan_id_foreign: depo_tujuan_id; job_orders_dock_awal_id_foreign: dock_awal_id; job_orders_dock_tujuan_id_foreign: dock_tujuan_id; job_orders_journal_id_foreign: journal_id; job_orders_journal_temp_id_foreign: journal_temp_id; job_orders_kpi_id_foreign: kpi_id; job_orders_moda_id_foreign: moda_id; job_orders_piece_id_foreign: piece_id; job_orders_quotation_detail_id_foreign: quotation_detail_id; job_orders_quotation_id_foreign: quotation_id; job_orders_receivable_id_foreign: receivable_id; job_orders_receiver_id_foreign: receiver_id; job_orders_route_id_foreign: route_id; job_orders_sender_id_foreign: sender_id; job_orders_service_id_foreign: service_id; job_orders_service_type_id_foreign: service_type_id; job_orders_transaction_type_id_foreign: transaction_type_id; job_orders_vehicle_type_id_foreign: vehicle_type_id; job_orders_warehouse_id_foreign: warehouse_id; job_orders_warehouse_receipt_id_index: warehouse_receipt_id; job_orders_warehouse_staff_id_foreign: warehouse_staff_id; job_orders_work_order_detail_id_foreign: work_order_detail_id; job_orders_work_order_id_foreign: work_order_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_orders_cancel_by_foreign (cancel_by → users.id); job_orders_collectible_id_foreign (collectible_id → contacts.id); job_orders_commodity_id_foreign (commodity_id → commodities.id); job_orders_company_id_foreign (company_id → companies.id); job_orders_container_type_id_foreign (container_type_id → container_types.id); job_orders_create_by_foreign (create_by → users.id); job_orders_customer_id_foreign (customer_id → contacts.id); job_orders_depo_awal_id_foreign (depo_awal_id → depo_containers.id); job_orders_depo_tujuan_id_foreign (depo_tujuan_id → depo_containers.id); job_orders_dock_awal_id_foreign (dock_awal_id → docks.id); job_orders_dock_tujuan_id_foreign (dock_tujuan_id → docks.id); job_orders_journal_id_foreign (journal_id → journals.id); job_orders_journal_temp_id_foreign (journal_temp_id → journals.id); job_orders_kpi_id_foreign (kpi_id → kpi_statuses.id); job_orders_moda_id_foreign (moda_id → modas.id); job_orders_piece_id_foreign (piece_id → pieces.id); job_orders_quotation_detail_id_foreign (quotation_detail_id → quotation_details.id); job_orders_quotation_id_foreign (quotation_id → quotations.id); job_orders_receivable_id_foreign (receivable_id → receivables.id); job_orders_receiver_id_foreign (receiver_id → contacts.id); job_orders_route_id_foreign (route_id → routes.id); job_orders_sender_id_foreign (sender_id → contacts.id); job_orders_service_id_foreign (service_id → services.id); job_orders_service_type_id_foreign (service_type_id → service_types.id); job_orders_transaction_type_id_foreign (transaction_type_id → type_transactions.id); job_orders_vehicle_type_id_foreign (vehicle_type_id → vehicle_types.id); job_orders_warehouse_id_foreign (warehouse_id → warehouses.id); job_orders_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id); job_orders_warehouse_staff_id_foreign (warehouse_staff_id → users.id); job_orders_work_order_detail_id_foreign (work_order_detail_id → work_order_details.id).

### `job_order_containers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `container_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_order_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** job_order_containers_container_id_index: container_id; job_order_containers_job_order_id_index: job_order_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_order_containers_container_id_foreign (container_id → containers.id); job_order_containers_job_order_id_foreign (job_order_id → job_orders.id).

### `job_order_costs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `cost_type_id` | `int(10) unsigned` | NO | `—` | — | — |
| `transaction_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `pickup_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `manifest_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `quotation_costs` | `double(20,2)` | NO | `0.00` | — | — |
| `before_revision_cost` | `double(20,2)` | NO | `0.00` | — | — |
| `manifest_cost_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `type` | `int(11)` | NO | `1` | — | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |
| `is_edit` | `tinyint(1)` | NO | `0` | — | — |
| `vendor_job_status_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_invoice` | `smallint(6)` | NO | `0` | — | — |
| `is_vendor_bill` | `smallint(6)` | NO | `0` | — | — |
| `driver_name` | `varchar(191)` | YES | `NULL` | — | — |
| `is_kasbon` | `int(11)` | YES | `0` | — | — |
| `qty_real` | `int(11)` | YES | `0` | — | — |
| `price_real` | `int(11)` | YES | `0` | — | — |
| `total_real` | `int(11)` | NO | `0` | — | — |
| `jurnal_realisasi` | `int(11)` | YES | `NULL` | — | — |
| `jurnal_jo_cost` | `int(11)` | YES | `NULL` | — | — |
| `generate_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `company_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code_invoice` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** job_order_costs_company_id_foreign: company_id; job_order_costs_generate_id_foreign: generate_id; job_order_costs_manifest_cost_id_foreign: manifest_cost_id; job_order_costs_vendor_job_status_id_index: vendor_job_status_id; job_order_costs_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_order_costs_company_id_foreign (company_id → companies.id); job_order_costs_generate_id_foreign (generate_id → generate_costs.id); job_order_costs_manifest_cost_id_foreign (manifest_cost_id → manifest_costs.id); job_order_costs_vendor_job_status_id_foreign (vendor_job_status_id → vendor_job_statuses.id).

### `job_order_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `picking_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `price_list_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `quotation_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `quotation_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `sender_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `receiver_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `is_contract` | `tinyint(1)` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |
| `imposition` | `int(11)` | NO | `1` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `weight` | `double` | NO | `0` | — | — |
| `volume` | `double` | NO | `0` | — | — |
| `long` | `double` | NO | `0` | — | — |
| `wide` | `double` | NO | `0` | — | — |
| `high` | `double` | NO | `0` | — | — |
| `v1` | `double` | YES | `0` | — | — |
| `tebal_v1` | `double` | YES | `0` | — | — |
| `v2` | `double` | YES | `0` | — | — |
| `tebal_v2` | `double` | YES | `0` | — | — |
| `transported` | `double` | NO | `0` | — | — |
| `leftover` | `double` | NO | `0` | — | — |
| `item_name` | `varchar(191)` | NO | `—` | — | — |
| `barcode` | `varchar(200)` | NO | `—` | — | — |
| `no_reff` | `varchar(191)` | YES | `NULL` | — | — |
| `no_manifest` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `manifest_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_receipt_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_out` | `date` | YES | `NULL` | — | — |
| `item_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `no_surat_jalan` | `varchar(100)` | YES | `NULL` | — | — |
| `rack_id` | `int(11)` | YES | `NULL` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `receive_date` | `datetime` | YES | `NULL` | — | — |
| `weight_type` | `int(11)` | YES | `NULL` | — | — |
| `volumetric_weight` | `double` | NO | `0` | — | — |
| `load_date` | `date` | YES | `NULL` | — | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `container_status` | `tinyint(4)` | YES | `NULL` | — | — |
| `code_item` | `varchar(191)` | YES | `NULL` | — | — |
| `gweight` | `double` | YES | `NULL` | — | — |
| `chgweight` | `double` | YES | `NULL` | — | — |
| `container_id` | `int(11)` | YES | `NULL` | — | — |
| `container_no` | `varchar(191)` | YES | `NULL` | — | — |
| `seal_number` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** job_order_details_commodity_id_foreign: commodity_id; job_order_details_create_by_foreign: create_by; job_order_details_header_id_foreign: header_id; job_order_details_manifest_id_foreign: manifest_id; job_order_details_piece_id_foreign: piece_id; job_order_details_price_list_id_foreign: price_list_id; job_order_details_quotation_detail_id_foreign: quotation_detail_id; job_order_details_quotation_id_foreign: quotation_id; job_order_details_receiver_id_foreign: receiver_id; job_order_details_requested_stock_transaction_id_index: requested_stock_transaction_id; job_order_details_sender_id_foreign: sender_id; job_order_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; job_order_details_warehouse_receipt_id_foreign: warehouse_receipt_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_order_details_commodity_id_foreign (commodity_id → commodities.id); job_order_details_create_by_foreign (create_by → users.id); job_order_details_header_id_foreign (header_id → job_orders.id); job_order_details_manifest_id_foreign (manifest_id → manifests.id); job_order_details_piece_id_foreign (piece_id → pieces.id); job_order_details_price_list_id_foreign (price_list_id → price_lists.id); job_order_details_quotation_detail_id_foreign (quotation_detail_id → quotation_details.id); job_order_details_quotation_id_foreign (quotation_id → quotations.id); job_order_details_receiver_id_foreign (receiver_id → contacts.id); job_order_details_requested_stock_transaction_id_foreign (requested_stock_transaction_id → stock_transactions.id); job_order_details_sender_id_foreign (sender_id → contacts.id); job_order_details_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id); job_order_details_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id).

### `job_order_detail_outputs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `job_order_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `date_out` | `date` | NO | `—` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `weight` | `double` | NO | `0` | — | — |
| `volume` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** job_order_detail_outputs_job_order_detail_id_foreign: job_order_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_order_detail_outputs_job_order_detail_id_foreign (job_order_detail_id → job_order_details.id).

### `job_order_documents` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `file_name` | `varchar(191)` | NO | `—` | — | — |
| `extension` | `varchar(191)` | NO | `—` | — | — |
| `upload_date` | `date` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_customer_view` | `tinyint(1)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `job_order_receivers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `date_receive` | `date` | NO | `—` | — | — |
| `receiver` | `varchar(191)` | NO | `—` | — | — |
| `telephone` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** job_order_receivers_create_by_foreign: create_by; job_order_receivers_header_id_foreign: header_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_order_receivers_create_by_foreign (create_by → users.id); job_order_receivers_header_id_foreign (header_id → job_orders.id).

### `job_order_transits` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(50)` | YES | `NULL` | — | — |
| `route_name` | `varchar(50)` | YES | `NULL` | — | — |
| `date` | `date` | YES | `NULL` | — | — |

**Indeks:** job_order_transits_header_id_index: header_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_order_transits_header_id_foreign (header_id → job_orders.id).

### `job_order_vehicles` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `no_lambung` | `varchar(255)` | YES | `NULL` | — | — |
| `nopol` | `varchar(255)` | YES | `NULL` | — | — |
| `model` | `varchar(255)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `job_packets` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `job_order_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `work_order_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `duration` | `int(11)` | NO | `1` | MUL | — |
| `qty` | `int(11)` | NO | `1` | MUL | — |
| `price` | `int(11)` | NO | `0` | MUL | — |
| `total_price` | `int(11)` | NO | `0` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** job_packets_duration_index: duration; job_packets_job_order_id_index: job_order_id; job_packets_price_index: price; job_packets_qty_index: qty; job_packets_total_price_index: total_price; job_packets_work_order_detail_id_index: work_order_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_packets_job_order_id_foreign (job_order_id → job_orders.id); job_packets_work_order_detail_id_foreign (work_order_detail_id → work_order_details.id).

### `job_statuses` — 20 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `urut` | `int(11)` | YES | `NULL` | — | — |
| `urut_full` | `int(11)` | YES | `NULL` | — | — |
| `urut_export` | `int(11)` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `is_start` | `tinyint(1)` | NO | `0` | — | — |
| `is_finish` | `tinyint(1)` | NO | `0` | — | — |
| `is_repeat` | `tinyint(1)` | NO | `0` | — | — |
| `is_cancel` | `tinyint(1)` | NO | `0` | — | — |
| `is_reject` | `tinyint(1)` | NO | `0` | — | — |
| `slug` | `varchar(50)` | YES | `NULL` | MUL | — |
| `must_upload_file` | `smallint(6)` | NO | `0` | — | — |
| `type` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch1` | `int(11)` | YES | `NULL` | — | — |
| `type_ch1` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch2` | `int(11)` | YES | `NULL` | — | — |
| `type_ch2` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch3` | `int(11)` | YES | `NULL` | — | — |
| `type_ch3` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch4` | `int(11)` | YES | `NULL` | — | — |
| `type_ch4` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch5` | `int(11)` | YES | `NULL` | — | — |
| `type_ch5` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch6` | `int(11)` | YES | `NULL` | — | — |
| `type_ch6` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch7` | `int(11)` | YES | `NULL` | — | — |
| `type_ch7` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch8` | `int(11)` | YES | `NULL` | — | — |
| `type_ch8` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch9` | `int(11)` | YES | `NULL` | — | — |
| `type_ch9` | `varchar(191)` | YES | `NULL` | — | — |
| `urut_ch10` | `int(11)` | YES | `NULL` | — | — |
| `type_ch10` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** job_statuses_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `job_status_histories` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `delivery_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_status_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `driver_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** job_status_histories_delivery_id_foreign: delivery_id; job_status_histories_job_status_id_foreign: job_status_id; PRIMARY (UNIQUE): id.  
**Foreign key:** job_status_histories_delivery_id_foreign (delivery_id → delivery_order_drivers.id); job_status_histories_job_status_id_foreign (job_status_id → job_statuses.id).

### `journals` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `posting_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `unposting_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_posting` | `date` | YES | `NULL` | — | — |
| `date_unposting` | `date` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `unposting_reason` | `varchar(191)` | YES | `NULL` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `source` | `int(11)` | YES | `NULL` | — | — |
| `is_audit` | `int(11)` | NO | `0` | MUL | — |
| `is_pajak` | `int(11)` | NO | `0` | — | — |

**Indeks:** journals_company_id_foreign: company_id; journals_created_by_foreign: created_by; journals_is_audit_index: is_audit; journals_posting_by_foreign: posting_by; journals_type_transaction_id_foreign: type_transaction_id; journals_unposting_by_foreign: unposting_by; PRIMARY (UNIQUE): id.  
**Foreign key:** journals_company_id_foreign (company_id → companies.id); journals_created_by_foreign (created_by → users.id); journals_posting_by_foreign (posting_by → users.id); journals_type_transaction_id_foreign (type_transaction_id → type_transactions.id); journals_unposting_by_foreign (unposting_by → users.id).

### `journal_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `account_id` | `int(10) unsigned` | NO | `—` | — | — |
| `cash_category_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_pajak` | `int(11)` | NO | `0` | — | — |
| `relation_cost_id` | `int(11)` | YES | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `journal_favorites` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** journal_favorites_created_by_foreign: created_by; PRIMARY (UNIQUE): id.  
**Foreign key:** journal_favorites_created_by_foreign (created_by → users.id).

### `journal_favorite_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `account_id` | `int(10) unsigned` | NO | `—` | — | — |
| `cash_category_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `jenis` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `km_tires` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `bias_min_km` | `int(11)` | NO | `—` | — | — |
| `bias_std_km` | `int(11)` | NO | `—` | — | — |
| `radial_min_km` | `int(11)` | NO | `—` | — | — |
| `radial_std_km` | `int(11)` | NO | `—` | — | — |
| `vulkanisir_min_km` | `int(11)` | NO | `—` | — | — |
| `vulkanisir_std_km` | `int(11)` | NO | `—` | — | — |
| `company_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** km_tires_company_id_foreign: company_id; PRIMARY (UNIQUE): id.  
**Foreign key:** km_tires_company_id_foreign (company_id → companies.id).

### `kpi_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `kpi_status_id` | `int(10) unsigned` | NO | `—` | — | — |
| `job_order_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `invoice_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `date_update` | `timestamp` | NO | `current_timestamp()` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `file_name` | `varchar(191)` | YES | `NULL` | — | — |
| `extension` | `varchar(191)` | YES | `NULL` | — | — |
| `manifest_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `kpi_statuses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `service_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `sort_number` | `int(11)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `duration` | `double(10,2)` | NO | `—` | — | — |
| `is_core` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `type` | `int(11)` | NO | `1` | — | — |
| `is_done` | `tinyint(1)` | NO | `0` | — | — |
| `status` | `int(11)` | NO | `2` | — | — |

**Indeks:** kpi_statuses_create_by_foreign: create_by; kpi_statuses_service_id_foreign: service_id; PRIMARY (UNIQUE): id.  
**Foreign key:** kpi_statuses_create_by_foreign (create_by → users.id); kpi_statuses_service_id_foreign (service_id → services.id).

### `kurs_valas` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `valas` | `varchar(255)` | NO | `—` | — | — |
| `manual` | `double(20,2)` | NO | `0.00` | — | — |
| `beli` | `double(20,2)` | NO | `0.00` | — | — |
| `jual` | `double(20,2)` | NO | `0.00` | — | — |
| `keterangan` | `varchar(255)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `leads` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `city_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `lead_status_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `lead_source_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `industry_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `sales_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `address` | `varchar(191)` | YES | `NULL` | — | — |
| `postal_code` | `varchar(191)` | YES | `NULL` | — | — |
| `phone` | `varchar(191)` | YES | `NULL` | — | — |
| `phone2` | `varchar(191)` | YES | `NULL` | — | — |
| `email` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person_email` | `varchar(191)` | YES | `NULL` | — | — |
| `contact_person_phone` | `varchar(191)` | YES | `NULL` | — | — |
| `is_contact` | `tinyint(1)` | NO | `0` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `inquery_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `quotation_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `step` | `int(11)` | NO | `1` | — | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_date` | `datetime` | YES | `NULL` | — | — |

**Indeks:** leads_cancel_by_foreign: cancel_by; leads_city_id_foreign: city_id; leads_company_id_foreign: company_id; leads_create_by_foreign: create_by; leads_industry_id_foreign: industry_id; leads_inquery_id_foreign: inquery_id; leads_lead_source_id_foreign: lead_source_id; leads_lead_status_id_foreign: lead_status_id; leads_quotation_id_foreign: quotation_id; leads_sales_id_foreign: sales_id; PRIMARY (UNIQUE): id.  
**Foreign key:** leads_cancel_by_foreign (cancel_by → users.id); leads_city_id_foreign (city_id → cities.id); leads_company_id_foreign (company_id → companies.id); leads_create_by_foreign (create_by → users.id); leads_industry_id_foreign (industry_id → industries.id); leads_inquery_id_foreign (inquery_id → inqueries.id); leads_lead_source_id_foreign (lead_source_id → lead_sources.id); leads_lead_status_id_foreign (lead_status_id → lead_statuses.id); leads_quotation_id_foreign (quotation_id → quotations.id); leads_sales_id_foreign (sales_id → contacts.id).

### `lead_activities` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `date_activity` | `date` | NO | `—` | — | — |
| `is_done` | `tinyint(1)` | NO | `0` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `lead_documents` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `file_name` | `varchar(191)` | NO | `—` | — | — |
| `extension` | `varchar(191)` | NO | `—` | — | — |
| `upload_date` | `date` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `lead_sources` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `lead_statuses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `status` | `varchar(191)` | NO | `—` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `maintenance_statuses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `manifests` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `job_order_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `transaction_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `container_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `route_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `moda_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `driver_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `co_driver_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `helper_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `container_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `delivery_order_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cancel_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_manifest` | `datetime` | YES | `NULL` | — | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `is_cancel` | `tinyint(1)` | NO | `0` | — | — |
| `cancel_date` | `date` | YES | `NULL` | — | — |
| `cancel_description` | `varchar(191)` | YES | `NULL` | — | — |
| `status_cost` | `int(11)` | NO | `1` | — | — |
| `is_container` | `tinyint(1)` | NO | `0` | — | — |
| `seal_number` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_full` | `tinyint(1)` | YES | `0` | — | — |
| `is_invoice` | `tinyint(1)` | NO | `0` | — | — |
| `etd_time` | `datetime` | YES | `NULL` | — | — |
| `eta_time` | `datetime` | YES | `NULL` | — | — |
| `depart` | `datetime` | YES | `NULL` | — | — |
| `arrive` | `datetime` | YES | `NULL` | — | — |
| `nopol` | `varchar(191)` | YES | `NULL` | — | — |
| `driver` | `varchar(191)` | YES | `NULL` | — | — |
| `co_driver` | `varchar(191)` | YES | `NULL` | — | — |
| `is_internal_driver` | `int(11)` | NO | `1` | — | — |
| `container_no` | `varchar(191)` | YES | `NULL` | — | — |
| `moda_info` | `varchar(191)` | YES | `NULL` | — | — |
| `source` | `varchar(30)` | NO | `'job_order'` | MUL | — |
| `is_crossdocking` | `smallint(6)` | NO | `0` | — | — |
| `additional` | `longtext` | YES | `NULL` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `revenue` | `int(11)` | NO | `0` | — | — |
| `generate_cost_id` | `int(11)` | YES | `NULL` | — | — |
| `no_sj_customer` | `varchar(191)` | YES | `NULL` | — | — |
| `job_status_id` | `int(10) unsigned` | NO | `2` | — | — |

**Indeks:** manifests_cancel_id_foreign: cancel_id; manifests_commodity_id_foreign: commodity_id; manifests_company_id_foreign: company_id; manifests_container_id_foreign: container_id; manifests_container_type_id_foreign: container_type_id; manifests_create_by_foreign: create_by; manifests_driver_id_foreign: driver_id; manifests_helper_id_foreign: helper_id; manifests_moda_id_foreign: moda_id; manifests_route_id_foreign: route_id; manifests_source_index: source; manifests_transaction_type_id_foreign: transaction_type_id; manifests_vehicle_id_foreign: vehicle_id; manifests_vehicle_type_id_foreign: vehicle_type_id; PRIMARY (UNIQUE): id.  
**Foreign key:** manifests_cancel_id_foreign (cancel_id → users.id); manifests_commodity_id_foreign (commodity_id → commodities.id); manifests_company_id_foreign (company_id → companies.id); manifests_container_id_foreign (container_id → containers.id); manifests_container_type_id_foreign (container_type_id → container_types.id); manifests_create_by_foreign (create_by → users.id); manifests_driver_id_foreign (driver_id → contacts.id); manifests_helper_id_foreign (helper_id → contacts.id); manifests_moda_id_foreign (moda_id → modas.id); manifests_route_id_foreign (route_id → routes.id); manifests_transaction_type_id_foreign (transaction_type_id → type_transactions.id); manifests_vehicle_id_foreign (vehicle_id → vehicles.id); manifests_vehicle_type_id_foreign (vehicle_type_id → vehicle_types.id).

### `manifest_costs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `cost_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `is_generated` | `tinyint(1)` | NO | `1` | — | — |
| `is_internal` | `tinyint(1)` | NO | `1` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `quotation_costs` | `double(20,2)` | NO | `0.00` | — | — |
| `before_revision_cost` | `double(20,2)` | NO | `0.00` | — | — |
| `type` | `int(11)` | NO | `1` | MUL | — |
| `is_edit` | `int(11)` | NO | `0` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `transaction_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `slug` | `varchar(50)` | YES | `NULL` | MUL | — |
| `job_order_cost_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vendor_job_status_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_invoice` | `int(11)` | NO | `0` | — | — |
| `is_vendor_bill` | `smallint(6)` | NO | `0` | — | — |
| `is_kasbon` | `int(11)` | YES | `0` | — | — |
| `driver_id` | `int(11)` | YES | `NULL` | — | — |
| `qty_real` | `int(11)` | YES | `0` | — | — |
| `price_real` | `int(11)` | YES | `0` | — | — |
| `total_real` | `int(11)` | YES | `0` | — | — |
| `is_realisasi` | `int(11)` | YES | `0` | — | — |
| `is_approve` | `int(11)` | YES | `0` | — | — |
| `journal_waiting_realisasi` | `int(11)` | YES | `NULL` | — | — |
| `journal_realisasi` | `int(11)` | YES | `NULL` | — | — |
| `journal_cost_manifest` | `int(11)` | YES | `NULL` | — | — |
| `driver_name` | `varchar(191)` | YES | `NULL` | — | — |
| `generate_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `from_bbm` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** manifest_costs_approve_by_index: approve_by; manifest_costs_generate_id_foreign: generate_id; manifest_costs_is_edit_index: is_edit; manifest_costs_job_order_cost_id_foreign: job_order_cost_id; manifest_costs_slug_index: slug; manifest_costs_transaction_type_id_index: transaction_type_id; manifest_costs_type_index: type; manifest_costs_vendor_job_status_id_index: vendor_job_status_id; PRIMARY (UNIQUE): id.  
**Foreign key:** manifest_costs_generate_id_foreign (generate_id → generate_costs.id); manifest_costs_job_order_cost_id_foreign (job_order_cost_id → job_order_costs.id); manifest_costs_vendor_job_status_id_foreign (vendor_job_status_id → vendor_job_statuses.id).

### `manifest_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_order_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `update_by` | `int(10) unsigned` | NO | `—` | — | — |
| `transported` | `double` | NO | `0` | — | — |
| `leftover` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_invoice` | `tinyint(1)` | NO | `0` | — | — |
| `picking_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `requested_qty` | `double` | NO | `0` | — | — |
| `discharged_qty` | `double` | NO | `0` | — | — |
| `outbound_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `packing_code` | `varchar(191)` | YES | `NULL` | — | — |
| `job_status_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** manifest_details_header_id_foreign: header_id; manifest_details_outbound_stock_transaction_id_index: outbound_stock_transaction_id; PRIMARY (UNIQUE): id.  
**Foreign key:** manifest_details_header_id_foreign (header_id → manifests.id); manifest_details_outbound_stock_transaction_id_foreign (outbound_stock_transaction_id → stock_transactions.id).

### `manifest_email_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `manifest_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `email_log_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** manifest_email_logs_email_log_id_index: email_log_id; manifest_email_logs_manifest_id_index: manifest_id; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `manifest_status_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `manifest_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_status_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** manifest_status_logs_created_by_index: created_by; manifest_status_logs_job_status_id_index: job_status_id; manifest_status_logs_manifest_id_index: manifest_id; PRIMARY (UNIQUE): id.  
**Foreign key:** manifest_status_logs_created_by_foreign (created_by → users.id); manifest_status_logs_job_status_id_foreign (job_status_id → job_statuses.id); manifest_status_logs_manifest_id_foreign (manifest_id → manifests.id).

### `migrations` — 1081 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `migration` | `varchar(191)` | NO | `—` | — | — |
| `batch` | `int(11)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `modas` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `months` — 12 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `sequence` | `smallint(6)` | NO | `0` | MUL | — |
| `name` | `varchar(20)` | NO | `—` | — | — |

**Indeks:** months_sequence_index: sequence; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `movement_containers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `date` | `datetime` | NO | `—` | MUL | — |
| `code` | `varchar(200)` | YES | `NULL` | MUL | — |
| `operator_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `status` | `int(10) unsigned` | NO | `—` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** movement_containers_code_index: code; movement_containers_company_id_index: company_id; movement_containers_created_by_index: created_by; movement_containers_date_index: date; movement_containers_operator_id_index: operator_id; movement_containers_status_index: status; PRIMARY (UNIQUE): id.  
**Foreign key:** movement_containers_company_id_foreign (company_id → companies.id); movement_containers_created_by_foreign (created_by → users.id); movement_containers_operator_id_foreign (operator_id → contacts.id).

### `movement_container_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `movement_container_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `gate_in_container_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `container_yard_destination_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** movement_container_details_container_yard_destination_id_index: container_yard_destination_id; movement_container_details_gate_in_container_id_index: gate_in_container_id; movement_container_details_movement_container_id_index: movement_container_id; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `movement_container_statuses` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `order` | `smallint(6)` | NO | `0` | — | — |
| `name` | `varchar(20)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `nota_credits` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `receivable_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cash_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `jenis` | `int(11)` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `reference_code` | `varchar(191)` | YES | `NULL` | — | — |
| `amount` | `double` | NO | `0` | — | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** nota_credits_cash_transaction_id_foreign: cash_transaction_id; nota_credits_company_id_foreign: company_id; nota_credits_contact_id_foreign: contact_id; nota_credits_journal_id_foreign: journal_id; nota_credits_receivable_id_foreign: receivable_id; PRIMARY (UNIQUE): id.  
**Foreign key:** nota_credits_cash_transaction_id_foreign (cash_transaction_id → cash_transactions.id); nota_credits_company_id_foreign (company_id → companies.id); nota_credits_contact_id_foreign (contact_id → contacts.id); nota_credits_journal_id_foreign (journal_id → journals.id); nota_credits_receivable_id_foreign (receivable_id → receivables.id).

### `nota_debets` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `payable_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cash_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `jenis` | `int(11)` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `reference` | `varchar(191)` | YES | `NULL` | — | — |
| `amount` | `double` | NO | `0` | — | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** nota_debets_cash_transaction_id_foreign: cash_transaction_id; nota_debets_company_id_foreign: company_id; nota_debets_contact_id_foreign: contact_id; nota_debets_journal_id_foreign: journal_id; nota_debets_payable_id_foreign: payable_id; PRIMARY (UNIQUE): id.  
**Foreign key:** nota_debets_cash_transaction_id_foreign (cash_transaction_id → cash_transactions.id); nota_debets_company_id_foreign (company_id → companies.id); nota_debets_contact_id_foreign (contact_id → contacts.id); nota_debets_journal_id_foreign (journal_id → journals.id); nota_debets_payable_id_foreign (payable_id → payables.id).

### `noticed_journal_notifications` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `journal_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `user_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** noticed_journal_notifications_journal_id_index: journal_id; noticed_journal_notifications_user_id_index: user_id; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `noticed_notifications` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `notification_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type` | `int(10) unsigned` | NO | `—` | MUL | — |
| `user_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** noticed_notifications_notification_id_index: notification_id; noticed_notifications_type_index: type; noticed_notifications_user_id_index: user_id; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `notifications` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `notification_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `is_done` | `tinyint(1)` | NO | `0` | — | — |
| `route` | `varchar(191)` | NO | `—` | — | — |
| `parameter` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** notifications_notification_type_id_foreign: notification_type_id; PRIMARY (UNIQUE): id.  
**Foreign key:** notifications_notification_type_id_foreign (notification_type_id → notification_types.id).

### `notification_types` — 11 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `notification_type_users` — 4 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `notification_type_id` | `int(10) unsigned` | NO | `—` | — | — |
| `user_id` | `int(10) unsigned` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `notification_users` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `notification_id` | `int(10) unsigned` | NO | `—` | — | — |
| `user_id` | `int(10) unsigned` | NO | `—` | — | — |
| `is_read` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `packagings` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date` | `date` | YES | `NULL` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `is_approve` | `smallint(6)` | NO | `0` | — | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(100)` | YES | `NULL` | MUL | — |

**Indeks:** packagings_code_index: code; packagings_company_id_index: company_id; packagings_created_by_index: created_by; packagings_customer_id_index: customer_id; packagings_date_index: date; packagings_warehouse_id_index: warehouse_id; PRIMARY (UNIQUE): id.  
**Foreign key:** packagings_company_id_foreign (company_id → companies.id); packagings_created_by_foreign (created_by → users.id); packagings_customer_id_foreign (customer_id → contacts.id); packagings_warehouse_id_foreign (warehouse_id → warehouses.id).

### `packaging_new_items` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `packaging_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `int(11)` | NO | `0` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approved_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** packaging_new_items_approved_stock_transaction_id_index: approved_stock_transaction_id; packaging_new_items_item_id_index: item_id; packaging_new_items_packaging_id_index: packaging_id; packaging_new_items_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** packaging_new_items_approved_stock_transaction_id_foreign (approved_stock_transaction_id → stock_transactions.id); packaging_new_items_item_id_foreign (item_id → items.id); packaging_new_items_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `packaging_old_items` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `packaging_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `int(11)` | NO | `0` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approved_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** packaging_old_items_approved_stock_transaction_id_index: approved_stock_transaction_id; packaging_old_items_packaging_id_index: packaging_id; packaging_old_items_rack_id_index: rack_id; packaging_old_items_requested_stock_transaction_id_index: requested_stock_transaction_id; packaging_old_items_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** packaging_old_items_approved_stock_transaction_id_foreign (approved_stock_transaction_id → stock_transactions.id); packaging_old_items_rack_id_foreign (rack_id → racks.id); packaging_old_items_requested_stock_transaction_id_foreign (requested_stock_transaction_id → stock_transactions.id); packaging_old_items_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `pallet_usages` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `shipping_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `using_date` | `date` | NO | `—` | — | — |
| `shipping_date` | `date` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** pallet_usages_create_by_foreign: create_by; pallet_usages_customer_id_foreign: customer_id; pallet_usages_shipping_by_foreign: shipping_by; pallet_usages_warehouse_id_foreign: warehouse_id; PRIMARY (UNIQUE): id.  
**Foreign key:** pallet_usages_create_by_foreign (create_by → users.id); pallet_usages_customer_id_foreign (customer_id → contacts.id); pallet_usages_shipping_by_foreign (shipping_by → users.id); pallet_usages_warehouse_id_foreign (warehouse_id → warehouses.id).

### `pallet_usage_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `leftover` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** pallet_usage_details_header_id_foreign: header_id; pallet_usage_details_item_id_foreign: item_id; PRIMARY (UNIQUE): id.  
**Foreign key:** pallet_usage_details_header_id_foreign (header_id → pallet_usages.id); pallet_usage_details_item_id_foreign (item_id → items.id).

### `password_resets` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `email` | `varchar(191)` | NO | `—` | MUL | — |
| `token` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `datetime` | YES | `NULL` | — | — |

**Indeks:** password_resets_email_index: email.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `payables` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_tempo` | `date` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_invoice` | `tinyint(1)` | NO | `0` | — | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_temporary` | `int(11)` | NO | `0` | — | — |
| `period` | `int(11)` | NO | `0` | — | — |
| `is_cost` | `int(11)` | YES | `0` | — | — |
| `is_payment` | `int(11)` | YES | `0` | — | — |
| `is_setting` | `int(10) unsigned` | YES | `NULL` | — | — |
| `credit_note` | `varchar(191)` | YES | `NULL` | — | — |
| `cash_request` | `varchar(191)` | YES | `NULL` | — | — |
| `cr_desc` | `varchar(191)` | YES | `NULL` | — | — |
| `status_cr` | `enum('Diajukan','Disetujui','Ditolak','Pusat')` | YES | `NULL` | — | — |
| `status_sp` | `enum('Lunas','Belum Lunas')` | YES | `NULL` | — | — |
| `cr_date` | `datetime` | NO | `—` | — | — |
| `sp_date` | `datetime` | NO | `—` | — | — |
| `priority` | `enum('Prioritas 1','Prioritas 2','Prioritas 3')` | YES | `NULL` | — | — |

**Indeks:** payables_account_id_foreign: account_id; payables_company_id_foreign: company_id; payables_contact_id_foreign: contact_id; payables_created_by_foreign: created_by; payables_journal_id_foreign: journal_id; payables_type_transaction_id_foreign: type_transaction_id; PRIMARY (UNIQUE): id.  
**Foreign key:** payables_account_id_foreign (account_id → accounts.id); payables_company_id_foreign (company_id → companies.id); payables_contact_id_foreign (contact_id → contacts.id); payables_created_by_foreign (created_by → users.id); payables_journal_id_foreign (journal_id → journals.id); payables_type_transaction_id_foreign (type_transaction_id → type_transactions.id).

### `payable_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_journal` | `tinyint(1)` | NO | `1` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `pickings` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(200)` | NO | `—` | — | — |
| `warehouse_id` | `int(11)` | NO | `—` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_approve` | `date` | NO | `—` | — | — |
| `date_cancel` | `date` | NO | `—` | — | — |
| `create_by` | `int(11)` | NO | `—` | — | — |
| `approve_by` | `int(11)` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `company_id` | `int(11)` | NO | `—` | — | — |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `staff_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** pickings_staff_id_foreign: staff_id; PRIMARY (UNIQUE): id.  
**Foreign key:** pickings_staff_id_foreign (staff_id → contacts.id).

### `picking_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `customer_order_detail_id` | `bigint(20) unsigned` | YES | `NULL` | — | — |
| `item_id` | `int(11)` | NO | `—` | — | — |
| `no_surat_jalan` | `varchar(100)` | YES | `NULL` | — | — |
| `qty` | `int(11)` | NO | `—` | — | — |
| `rack_id` | `int(11)` | NO | `—` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `lot_no` | `varchar(191)` | YES | `NULL` | — | — |
| `um` | `varchar(191)` | YES | `NULL` | — | — |
| `delivery_schedule` | `timestamp` | YES | `NULL` | — | — |
| `time_staging` | `timestamp` | YES | `NULL` | — | — |
| `time_finish` | `timestamp` | YES | `NULL` | — | — |
| `qty_delivered` | `double` | NO | `0` | — | — |
| `qty_leftover` | `int(11)` | NO | `0` | — | — |
| `category_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approved_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** picking_details_approved_stock_transaction_id_index: approved_stock_transaction_id; picking_details_category_id_foreign: category_id; picking_details_requested_stock_transaction_id_index: requested_stock_transaction_id; picking_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; PRIMARY (UNIQUE): id.  
**Foreign key:** picking_details_approved_stock_transaction_id_foreign (approved_stock_transaction_id → stock_transactions.id); picking_details_category_id_foreign (category_id → categories.id); picking_details_requested_stock_transaction_id_foreign (requested_stock_transaction_id → stock_transactions.id); picking_details_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `picking_statuses` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(191)` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** picking_statuses_slug_index: slug; PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `pieces` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `ports` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `island_name` | `varchar(191)` | NO | `—` | — | — |
| `latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `country_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** ports_country_id_foreign: country_id; PRIMARY (UNIQUE): id.  
**Foreign key:** ports_country_id_foreign (country_id → countries.id).

### `price_lists` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `route_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `service_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `combined_price_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price_type` | `varchar(10)` | NO | `'service'` | — | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `moda_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `min_tonase` | `double` | YES | `NULL` | — | — |
| `price_tonase` | `double` | YES | `NULL` | — | — |
| `min_volume` | `double` | YES | `NULL` | — | — |
| `price_volume` | `double` | YES | `NULL` | — | — |
| `min_item` | `double` | YES | `NULL` | — | — |
| `price_item` | `double` | YES | `NULL` | — | — |
| `price_full` | `double` | YES | `NULL` | — | — |
| `is_active` | `double` | NO | `1` | — | — |
| `piece_name` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `price_handling_tonase` | `double` | YES | `NULL` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `container_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `service_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price_handling_volume` | `double` | YES | `NULL` | — | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_warehouse` | `int(11)` | NO | `0` | — | — |
| `price_borongan` | `double` | NO | `0` | — | — |
| `min_borongan` | `int(11)` | NO | `0` | — | — |
| `free_storage_day` | `int(11)` | NO | `0` | — | — |
| `over_storage_price` | `double` | NO | `0` | — | — |
| `daily_price` | `double` | NO | `0` | — | — |
| `pallet_price` | `double` | NO | `0` | — | — |
| `handling_type` | `int(11)` | NO | `1` | MUL | — |
| `min_type` | `int(11)` | YES | `NULL` | — | — |
| `depo_awal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `depo_tujuan_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `dock_awal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `dock_tujuan_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** price_lists_combined_price_id_foreign: combined_price_id; price_lists_commodity_id_foreign: commodity_id; price_lists_company_id_foreign: company_id; price_lists_created_by_foreign: created_by; price_lists_depo_awal_id_foreign: depo_awal_id; price_lists_depo_tujuan_id_foreign: depo_tujuan_id; price_lists_dock_awal_id_foreign: dock_awal_id; price_lists_dock_tujuan_id_foreign: dock_tujuan_id; price_lists_handling_type_index: handling_type; price_lists_moda_id_foreign: moda_id; price_lists_piece_id_foreign: piece_id; price_lists_route_id_foreign: route_id; price_lists_service_id_foreign: service_id; price_lists_vehicle_type_id_foreign: vehicle_type_id; price_lists_warehouse_id_foreign: warehouse_id; price_list_ctype_for: container_type_id; price_list_rack_id_for: rack_id; price_list_service_type_for: service_type_id; PRIMARY (UNIQUE): id.  
**Foreign key:** price_lists_combined_price_id_foreign (combined_price_id → combined_prices.id); price_lists_commodity_id_foreign (commodity_id → commodities.id); price_lists_company_id_foreign (company_id → companies.id); price_lists_created_by_foreign (created_by → users.id); price_lists_depo_awal_id_foreign (depo_awal_id → depo_containers.id); price_lists_depo_tujuan_id_foreign (depo_tujuan_id → depo_containers.id); price_lists_dock_awal_id_foreign (dock_awal_id → docks.id); price_lists_dock_tujuan_id_foreign (dock_tujuan_id → docks.id); price_lists_moda_id_foreign (moda_id → modas.id); price_lists_piece_id_foreign (piece_id → pieces.id); price_lists_route_id_foreign (route_id → routes.id); price_lists_service_id_foreign (service_id → services.id); price_lists_vehicle_type_id_foreign (vehicle_type_id → vehicle_types.id); price_lists_warehouse_id_foreign (warehouse_id → warehouses.id); price_list_ctype_for (container_type_id → container_types.id); price_list_rack_id_for (rack_id → racks.id); price_list_service_type_for (service_type_id → service_types.id).

### `price_list_costs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cost_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type` | `int(10) unsigned` | NO | `1` | MUL | — |
| `qty` | `double(10,2)` | NO | `0.00` | MUL | — |
| `price` | `double(10,2)` | NO | `0.00` | MUL | — |
| `total_price` | `double(10,2)` | NO | `0.00` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** price_list_costs_cost_type_id_index: cost_type_id; price_list_costs_create_by_index: create_by; price_list_costs_header_id_foreign: header_id; price_list_costs_journal_id_index: journal_id; price_list_costs_price_index: price; price_list_costs_qty_index: qty; price_list_costs_total_price_index: total_price; price_list_costs_type_index: type; price_list_costs_vendor_id_index: vendor_id; PRIMARY (UNIQUE): id.  
**Foreign key:** price_list_costs_cost_type_id_foreign (cost_type_id → cost_types.id); price_list_costs_create_by_foreign (create_by → users.id); price_list_costs_header_id_foreign (header_id → price_lists.id); price_list_costs_journal_id_foreign (journal_id → journals.id); price_list_costs_vendor_id_foreign (vendor_id → contacts.id).

### `price_list_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `service_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `price` | `double` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** price_list_details_header_id_foreign: header_id; price_list_details_service_id_foreign: service_id; PRIMARY (UNIQUE): id.  
**Foreign key:** price_list_details_header_id_foreign (header_id → price_lists.id); price_list_details_service_id_foreign (service_id → services.id).

### `price_list_minimum_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `price_list_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `quotation_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `price_per_kg` | `double` | NO | `—` | — | — |
| `min_kg` | `int(11)` | NO | `—` | — | — |
| `price_per_m3` | `double` | NO | `—` | — | — |
| `min_m3` | `int(11)` | NO | `—` | — | — |
| `price_per_item` | `double` | NO | `—` | — | — |
| `min_item` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `print_remarks` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `account` | `text` | YES | `NULL` | — | — |
| `bank` | `text` | YES | `NULL` | — | — |
| `person` | `text` | YES | `NULL` | — | — |
| `signature` | `text` | YES | `NULL` | — | — |
| `position` | `text` | YES | `NULL` | — | — |
| `attn` | `text` | YES | `NULL` | — | — |
| `address` | `text` | YES | `NULL` | — | — |
| `phone` | `text` | YES | `NULL` | — | — |
| `fax` | `text` | YES | `NULL` | — | — |
| `logo` | `varchar(191)` | YES | `NULL` | — | — |
| `email` | `varchar(100)` | YES | `NULL` | — | — |
| `sms_center` | `varchar(100)` | YES | `NULL` | — | — |
| `additional` | `text` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `projects` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | UNI | — |
| `name` | `varchar(191)` | NO | `—` | UNI | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; projects_code_unique (UNIQUE): code; projects_name_unique (UNIQUE): name.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `provinces` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `country_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; provinces_country_id_foreign: country_id.  
**Foreign key:** provinces_country_id_foreign (country_id → countries.id).

### `purchase_orders` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `supplier_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `po_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `po_date` | `date` | NO | `—` | — | — |
| `po_status` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `vehicle_maintenance_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `payment_type` | `int(11)` | NO | `1` | MUL | — |
| `ppn_is_faktur` | `tinyint(4)` | NO | `1` | — | — |
| `no_faktur_pajak` | `varchar(100)` | YES | `NULL` | — | — |
| `cash_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `payable_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `due_date` | `text` | YES | `NULL` | — | — |
| `no_ref` | `varchar(191)` | YES | `NULL` | — | — |
| `file_name` | `varchar(191)` | YES | `NULL` | — | — |
| `approved_by` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; purchase_orders_cash_transaction_id_foreign: cash_transaction_id; purchase_orders_company_id_foreign: company_id; purchase_orders_journal_id_foreign: journal_id; purchase_orders_payable_id_foreign: payable_id; purchase_orders_payment_type_index: payment_type; purchase_orders_po_by_foreign: po_by; purchase_orders_status_index: status; purchase_orders_supplier_id_foreign: supplier_id; purchase_orders_vm_id_foreign: vehicle_maintenance_id; purchase_orders_warehouse_id_foreign: warehouse_id.  
**Foreign key:** purchase_orders_cash_transaction_id_foreign (cash_transaction_id → cash_transactions.id); purchase_orders_company_id_foreign (company_id → companies.id); purchase_orders_journal_id_foreign (journal_id → journals.id); purchase_orders_payable_id_foreign (payable_id → payables.id); purchase_orders_po_by_foreign (po_by → users.id); purchase_orders_status_foreign (status → purchase_order_statuses.id); purchase_orders_supplier_id_foreign (supplier_id → contacts.id); purchase_orders_vm_id_foreign (vehicle_maintenance_id → vehicle_maintenances.id); purchase_orders_warehouse_id_foreign (warehouse_id → warehouses.id).

### `purchase_order_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `purchase_request_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `ppn` | `double` | NO | `0` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `receive` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `files` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; purchase_order_details_header_id_foreign: header_id; purchase_order_details_item_id_foreign: item_id; purchase_order_details_purchase_request_detail_id_foreign: purchase_request_detail_id.  
**Foreign key:** purchase_order_details_header_id_foreign (header_id → purchase_orders.id); purchase_order_details_item_id_foreign (item_id → items.id); purchase_order_details_purchase_request_detail_id_foreign (purchase_request_detail_id → purchase_request_details.id).

### `purchase_order_purchase_request` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `po_id` | `int(10) unsigned` | NO | `—` | PRI | — |
| `pr_id` | `int(10) unsigned` | NO | `—` | PRI | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): po_id, pr_id; purchase_order_purchase_request_pr_id_foreign: pr_id.  
**Foreign key:** purchase_order_purchase_request_po_id_foreign (po_id → purchase_orders.id); purchase_order_purchase_request_pr_id_foreign (pr_id → purchase_requests.id).

### `purchase_order_receipt_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `purchase_order_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `average_price` | `double` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; purchase_order_receipt_details_purchase_order_detail_id_index: purchase_order_detail_id; purchase_order_receipt_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `purchase_order_returns` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `purchase_order_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_return_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `date_cancel` | `date` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `cancel_reason` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; purchase_order_returns_account_return_id_foreign: account_return_id; purchase_order_returns_approve_by_foreign: approve_by; purchase_order_returns_cancel_by_foreign: cancel_by; purchase_order_returns_create_by_foreign: create_by; purchase_order_returns_journal_id_foreign: journal_id; purchase_order_returns_purchase_order_id_foreign: purchase_order_id; purchase_order_returns_warehouse_id_foreign: warehouse_id.  
**Foreign key:** purchase_order_returns_account_return_id_foreign (account_return_id → accounts.id); purchase_order_returns_approve_by_foreign (approve_by → users.id); purchase_order_returns_cancel_by_foreign (cancel_by → users.id); purchase_order_returns_create_by_foreign (create_by → users.id); purchase_order_returns_journal_id_foreign (journal_id → journals.id); purchase_order_returns_purchase_order_id_foreign (purchase_order_id → purchase_orders.id); purchase_order_returns_warehouse_id_foreign (warehouse_id → warehouses.id).

### `purchase_order_return_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `po_qty` | `double` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `po_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `receive` | `double` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; purchase_order_return_details_header_id_foreign: header_id; purchase_order_return_details_item_id_foreign: item_id; purchase_order_return_details_po_detail_id_foreign: po_detail_id.  
**Foreign key:** purchase_order_return_details_header_id_foreign (header_id → purchase_order_returns.id); purchase_order_return_details_item_id_foreign (item_id → items.id); purchase_order_return_details_po_detail_id_foreign (po_detail_id → purchase_order_details.id).

### `purchase_order_statuses` — 6 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(20)` | NO | `—` | MUL | — |
| `name` | `varchar(50)` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; purchase_order_statuses_name_index: name; purchase_order_statuses_slug_index: slug.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `purchase_requests` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `reject_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_request` | `date` | NO | `—` | — | — |
| `date_needed` | `date` | NO | `—` | — | — |
| `date_approved` | `date` | YES | `NULL` | — | — |
| `date_reject` | `date` | YES | `NULL` | — | — |
| `reject_reason` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `vehicle_maintenance_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_pallet` | `tinyint(1)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; purchase_requests_approve_by_foreign: approve_by; purchase_requests_company_id_foreign: company_id; purchase_requests_create_by_foreign: create_by; purchase_requests_reject_by_foreign: reject_by; purchase_requests_vm_id_foreign: vehicle_maintenance_id; purchase_requests_warehouse_id_foreign: warehouse_id.  
**Foreign key:** purchase_requests_approve_by_foreign (approve_by → users.id); purchase_requests_company_id_foreign (company_id → companies.id); purchase_requests_create_by_foreign (create_by → users.id); purchase_requests_reject_by_foreign (reject_by → users.id); purchase_requests_vm_id_foreign (vehicle_maintenance_id → vehicle_maintenances.id); purchase_requests_warehouse_id_foreign (warehouse_id → warehouses.id).

### `purchase_request_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `qty_approve` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `vehicle_maintenance_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `customer_order_details_id` | `int(11)` | YES | `NULL` | — | — |
| `department_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `project_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `qty_po` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; purchase_request_details_department_id_foreign: department_id; purchase_request_details_header_id_foreign: header_id; purchase_request_details_item_id_foreign: item_id; purchase_request_details_project_id_foreign: project_id; purchase_request_details_vehicle_id_foreign: vehicle_id; purchase_request_details_vmd_id_foreign: vehicle_maintenance_detail_id.  
**Foreign key:** purchase_request_details_department_id_foreign (department_id → departments.id); purchase_request_details_header_id_foreign (header_id → purchase_requests.id); purchase_request_details_item_id_foreign (item_id → items.id); purchase_request_details_project_id_foreign (project_id → projects.id); purchase_request_details_vehicle_id_foreign (vehicle_id → vehicles.id); purchase_request_details_vmd_id_foreign (vehicle_maintenance_detail_id → vehicle_maintenance_details.id).

### `putaways` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `queries` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(200)` | NO | `—` | MUL | — |
| `query` | `text` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; queries_name_index: name.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `quotations` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `lead_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `sales_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `customer_stage_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `contract_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `no_inquery` | `varchar(191)` | YES | `NULL` | — | — |
| `date_inquery` | `date` | YES | `NULL` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `no_contract` | `varchar(191)` | YES | `NULL` | — | — |
| `date_contract` | `date` | YES | `NULL` | — | — |
| `date_start_contract` | `date` | YES | `NULL` | — | — |
| `date_end_contract` | `date` | YES | `NULL` | — | — |
| `date_cancel` | `date` | YES | `NULL` | — | — |
| `is_contract` | `tinyint(1)` | NO | `0` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |
| `is_cancel` | `tinyint(1)` | NO | `0` | — | — |
| `sales_commision` | `double` | NO | `0` | — | — |
| `bill_type` | `int(11)` | NO | `—` | — | — |
| `send_type` | `int(11)` | NO | `—` | — | — |
| `price_full_inquery` | `double` | NO | `0` | — | — |
| `price_full_contract` | `double` | NO | `0` | — | — |
| `description_inquery` | `text` | YES | `NULL` | — | — |
| `description_contract` | `text` | YES | `NULL` | — | — |
| `type_entry` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | YES | `NULL` | — | — |
| `submit_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approve_direction_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approve_manager_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `status_approve` | `int(11)` | NO | `1` | — | — |
| `description_stop_contract` | `text` | YES | `NULL` | — | — |
| `stop_contract_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_stop_contract` | `date` | YES | `NULL` | — | — |
| `description_amandemen` | `text` | YES | `NULL` | — | — |
| `date_amandemen` | `date` | YES | `NULL` | — | — |
| `parent_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_hide` | `tinyint(1)` | NO | `0` | — | — |
| `cancel_quotation_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_quotation_date` | `datetime` | YES | `NULL` | — | — |
| `imposition` | `int(11)` | YES | `NULL` | — | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |
| `path` | `varchar(50)` | YES | `NULL` | MUL | — |
| `is_sales_contract` | `smallint(6)` | NO | `0` | — | — |
| `is_borongan` | `tinyint(1)` | YES | `0` | — | — |
| `total_price` | `int(11)` | YES | `0` | — | — |
| `min_trip` | `int(11)` | NO | `0` | — | — |
| `max_trip` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; quotations_approve_by_foreign: approve_by; quotations_approve_direction_by_foreign: approve_direction_by; quotations_approve_manager_by_foreign: approve_manager_by; quotations_cancel_by_foreign: cancel_by; quotations_cancel_quotation_by_foreign: cancel_quotation_by; quotations_company_id_foreign: company_id; quotations_contract_by_foreign: contract_by; quotations_created_by_foreign: created_by; quotations_customer_id_foreign: customer_id; quotations_customer_stage_id_foreign: customer_stage_id; quotations_lead_id_foreign: lead_id; quotations_parent_id_foreign: parent_id; quotations_path_index: path; quotations_piece_id_foreign: piece_id; quotations_sales_id_foreign: sales_id; quotations_stop_contract_by_foreign: stop_contract_by; quotations_submit_by_foreign: submit_by.  
**Foreign key:** quotations_approve_by_foreign (approve_by → users.id); quotations_approve_direction_by_foreign (approve_direction_by → users.id); quotations_approve_manager_by_foreign (approve_manager_by → users.id); quotations_cancel_by_foreign (cancel_by → users.id); quotations_cancel_quotation_by_foreign (cancel_quotation_by → users.id); quotations_company_id_foreign (company_id → companies.id); quotations_contract_by_foreign (contract_by → users.id); quotations_created_by_foreign (created_by → users.id); quotations_customer_id_foreign (customer_id → contacts.id); quotations_customer_stage_id_foreign (customer_stage_id → customer_stages.id); quotations_lead_id_foreign (lead_id → leads.id); quotations_parent_id_foreign (parent_id → quotations.id); quotations_piece_id_foreign (piece_id → pieces.id); quotations_sales_id_foreign (sales_id → contacts.id); quotations_stop_contract_by_foreign (stop_contract_by → users.id); quotations_submit_by_foreign (submit_by → users.id).

### `quotation_costs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `cost_type_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vendor_id` | `int(10) unsigned` | NO | `—` | — | — |
| `created_by` | `int(10) unsigned` | NO | `—` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `cost` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `is_internal` | `tinyint(1)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `quotation_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `route_cost_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `total_cost` | `double` | YES | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `quotation_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | YES | `NULL` | — | — |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `price_list_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `route_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `service_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `business_portfolio_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `combined_price_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price_type` | `varchar(10)` | NO | `'service'` | — | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `moda_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `piece_name` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `imposition` | `int(11)` | YES | `0` | — | — |
| `total` | `double` | YES | `NULL` | — | — |
| `price_inquery_tonase` | `double` | YES | `NULL` | — | — |
| `price_contract_tonase` | `double` | YES | `NULL` | — | — |
| `price_inquery_volume` | `double` | YES | `NULL` | — | — |
| `price_contract_volume` | `double` | YES | `NULL` | — | — |
| `price_inquery_item` | `double` | YES | `NULL` | — | — |
| `price_contract_item` | `double` | YES | `NULL` | — | — |
| `price_inquery_full` | `double` | YES | `NULL` | — | — |
| `price_contract_full` | `double` | YES | `NULL` | — | — |
| `cost` | `double` | YES | `NULL` | — | — |
| `is_generate` | `int(11)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `price_inquery_handling_tonase` | `double` | YES | `NULL` | — | — |
| `price_contract_handling_tonase` | `double` | YES | `NULL` | — | — |
| `price_inquery_handling_volume` | `double` | YES | `NULL` | — | — |
| `price_contract_handling_volume` | `double` | YES | `NULL` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `container_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `service_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price_inquery_min_tonase` | `double` | YES | `NULL` | — | — |
| `price_contract_min_tonase` | `double` | YES | `NULL` | — | — |
| `price_inquery_min_volume` | `double` | YES | `NULL` | — | — |
| `price_contract_min_volume` | `double` | YES | `NULL` | — | — |
| `price_inquery_min_item` | `double` | YES | `NULL` | — | — |
| `price_contract_min_item` | `double` | YES | `NULL` | — | — |
| `route_cost_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `price_list_price_full` | `double` | NO | `0` | — | — |
| `price_list_price_tonase` | `double` | NO | `0` | — | — |
| `price_list_price_volume` | `double` | NO | `0` | — | — |
| `price_list_price_item` | `double` | NO | `0` | — | — |
| `is_approve` | `tinyint(1)` | NO | `0` | — | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |
| `free_storage_day` | `int(11)` | NO | `0` | — | — |
| `over_storage_price` | `double` | NO | `0` | — | — |
| `pallet_price` | `double` | NO | `0` | — | — |
| `handling_type` | `int(11)` | YES | `1` | MUL | — |
| `min_type` | `int(11)` | YES | `NULL` | — | — |
| `standard_price` | `double` | YES | `NULL` | — | — |
| `depo_awal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `depo_tujuan_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `dock_awal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `dock_tujuan_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_borongan` | `tinyint(1)` | NO | `0` | — | — |
| `price_inquery_borongan` | `double` | YES | `NULL` | — | — |
| `price_contract_borongan` | `double` | YES | `NULL` | — | — |
| `price_inquery_min_borongan` | `double` | YES | `NULL` | — | — |
| `price_contract_min_borongan` | `double` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; quotation_details_approve_by_foreign: approve_by; quotation_details_combined_price_id_foreign: combined_price_id; quotation_details_commodity_id_foreign: commodity_id; quotation_details_depo_awal_id_foreign: depo_awal_id; quotation_details_depo_tujuan_id_foreign: depo_tujuan_id; quotation_details_dock_awal_id_foreign: dock_awal_id; quotation_details_dock_tujuan_id_foreign: dock_tujuan_id; quotation_details_handling_type_index: handling_type; quotation_details_header_id_foreign: header_id; quotation_details_moda_id_foreign: moda_id; quotation_details_piece_id_foreign: piece_id; quotation_details_price_list_id_foreign: price_list_id; quotation_details_route_id_foreign: route_id; quotation_details_service_id_foreign: service_id; quotation_details_vehicle_type_id_foreign: vehicle_type_id; quotation_details_warehouse_id_foreign: warehouse_id; quot_det_cont_type_for: container_type_id; quot_det_rack_id_for: rack_id; quot_det_ser_type_for: service_type_id.  
**Foreign key:** quotation_details_approve_by_foreign (approve_by → users.id); quotation_details_combined_price_id_foreign (combined_price_id → combined_prices.id); quotation_details_commodity_id_foreign (commodity_id → commodities.id); quotation_details_depo_awal_id_foreign (depo_awal_id → depo_containers.id); quotation_details_depo_tujuan_id_foreign (depo_tujuan_id → depo_containers.id); quotation_details_dock_awal_id_foreign (dock_awal_id → docks.id); quotation_details_dock_tujuan_id_foreign (dock_tujuan_id → docks.id); quotation_details_header_id_foreign (header_id → quotations.id); quotation_details_moda_id_foreign (moda_id → modas.id); quotation_details_piece_id_foreign (piece_id → pieces.id); quotation_details_price_list_id_foreign (price_list_id → price_lists.id); quotation_details_route_id_foreign (route_id → routes.id); quotation_details_service_id_foreign (service_id → services.id); quotation_details_vehicle_type_id_foreign (vehicle_type_id → vehicle_types.id); quotation_details_warehouse_id_foreign (warehouse_id → warehouses.id); quot_det_cont_type_for (container_type_id → container_types.id); quot_det_rack_id_for (rack_id → racks.id); quot_det_ser_type_for (service_type_id → service_types.id).

### `quotation_files` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `file_name` | `varchar(191)` | NO | `—` | — | — |
| `date_upload` | `date` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `extension` | `varchar(191)` | YES | `NULL` | — | — |
| `is_customer_view` | `tinyint(1)` | NO | `1` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; quotation_files_header_id_foreign: header_id.  
**Foreign key:** quotation_files_header_id_foreign (header_id → quotations.id).

### `quotation_history_offers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `quotation_detail_id` | `int(10) unsigned` | NO | `—` | — | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `reject_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `is_approve` | `tinyint(1)` | NO | `0` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_cost` | `double` | NO | `0` | — | — |
| `total_offering` | `double` | NO | `0` | — | — |
| `date_approve` | `datetime` | YES | `NULL` | — | — |
| `date_reject` | `datetime` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `quotation_items` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `quotation_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; quotation_items_item_id_index: item_id; quotation_items_quotation_id_index: quotation_id; quotation_items_warehouse_receipt_detail_id_foreign: warehouse_receipt_detail_id.  
**Foreign key:** quotation_items_item_id_foreign (item_id → items.id); quotation_items_quotation_id_foreign (quotation_id → quotations.id); quotation_items_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `quotation_price_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `service_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `price` | `double` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; quotation_price_details_header_id_foreign: header_id; quotation_price_details_service_id_foreign: service_id.  
**Foreign key:** quotation_price_details_header_id_foreign (header_id → quotation_details.id); quotation_price_details_service_id_foreign (service_id → services.id).

### `racks` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `capacity_volume` | `double` | NO | `0` | — | — |
| `capacity_volume_used` | `double` | NO | `0` | — | — |
| `capacity_tonase` | `double` | NO | `0` | — | — |
| `capacity_tonase_used` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `storage_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `barcode` | `varchar(191)` | YES | `NULL` | — | — |
| `max_pallet` | `int(11)` | NO | `0` | — | — |
| `is_floor_stake` | `smallint(6)` | NO | `0` | — | — |
| `luas` | `int(11)` | NO | `0` | — | — |
| `is_dangerous_good` | `smallint(6)` | NO | `0` | MUL | — |
| `is_fast_moving` | `smallint(6)` | NO | `0` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; racks_is_dangerous_good_index: is_dangerous_good; racks_is_fast_moving_index: is_fast_moving; racks_storage_type_id_foreign: storage_type_id; racks_warehouse_id_foreign: warehouse_id.  
**Foreign key:** racks_storage_type_id_foreign (storage_type_id → storage_types.id); racks_warehouse_id_foreign (warehouse_id → warehouses.id).

### `rack_maps` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `rack_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_map_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; rack_maps_rack_id_index: rack_id; rack_maps_warehouse_map_id_index: warehouse_map_id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `receipts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `po_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `po_return_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `sales_return_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `usage_return_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `item_migration_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `is_tms` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `relation_code` | `varchar(191)` | YES | `NULL` | — | — |
| `relation_type` | `int(11)` | NO | `1` | — | — |
| `account_item_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price` | `double` | NO | `0` | — | — |
| `gift_from` | `varchar(200)` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; receipts_account_item_id_foreign: account_item_id; receipts_company_id_foreign: company_id; receipts_gift_from_index: gift_from; receipts_item_migration_id_foreign: item_migration_id; receipts_journal_id_foreign: journal_id; receipts_po_id_foreign: po_id; receipts_po_return_id_foreign: po_return_id; receipts_sales_return_id_foreign: sales_return_id; receipts_usage_return_id_foreign: usage_return_id.  
**Foreign key:** receipts_account_item_id_foreign (account_item_id → accounts.id); receipts_company_id_foreign (company_id → companies.id); receipts_item_migration_id_foreign (item_migration_id → item_migrations.id); receipts_journal_id_foreign (journal_id → journals.id); receipts_po_id_foreign (po_id → purchase_orders.id); receipts_po_return_id_foreign (po_return_id → purchase_order_returns.id); receipts_sales_return_id_foreign (sales_return_id → sales_order_returns.id); receipts_usage_return_id_foreign (usage_return_id → using_items.id).

### `receipt_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `price` | `double` | NO | `0` | MUL | — |
| `total_price` | `double` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; receipt_details_header_id_foreign: header_id; receipt_details_item_id_foreign: item_id; receipt_details_price_index: price.  
**Foreign key:** receipt_details_header_id_foreign (header_id → receipts.id); receipt_details_item_id_foreign (item_id → items.id).

### `receipt_lists` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cash_account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `delivery_no` | `varchar(191)` | NO | `—` | — | — |
| `receive_name` | `varchar(191)` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `receive_date` | `date` | NO | `—` | — | — |
| `termin` | `int(11)` | NO | `1` | — | — |
| `urut` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `type` | `tinyint(1)` | YES | `1` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; receipt_lists_cash_account_id_foreign: cash_account_id; receipt_lists_header_id_foreign: header_id; receipt_lists_warehouse_id_foreign: warehouse_id.  
**Foreign key:** receipt_lists_cash_account_id_foreign (cash_account_id → accounts.id); receipt_lists_header_id_foreign (header_id → receipts.id); receipt_lists_warehouse_id_foreign (warehouse_id → warehouses.id).

### `receipt_list_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; receipt_list_details_header_id_foreign: header_id; receipt_list_details_item_id_foreign: item_id.  
**Foreign key:** receipt_list_details_header_id_foreign (header_id → receipt_lists.id); receipt_list_details_item_id_foreign (item_id → items.id).

### `receipt_quality_statuses` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(30)` | NO | `—` | MUL | — |
| `name` | `varchar(30)` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; receipt_quality_statuses_name_index: name; receipt_quality_statuses_slug_index: slug.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `receipt_types` — 10 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(10)` | NO | `—` | MUL | — |
| `name` | `varchar(50)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; receipt_types_code_index: code.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `receivables` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_tempo` | `date` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_confirm` | `int(11)` | NO | `0` | — | — |
| `is_temporary` | `int(11)` | NO | `0` | — | — |
| `period` | `int(11)` | NO | `0` | — | — |
| `debet_note` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; receivables_account_id_foreign: account_id; receivables_company_id_foreign: company_id; receivables_contact_id_foreign: contact_id; receivables_created_by_foreign: created_by; receivables_journal_id_foreign: journal_id; receivables_type_transaction_id_foreign: type_transaction_id.  
**Foreign key:** receivables_account_id_foreign (account_id → accounts.id); receivables_company_id_foreign (company_id → companies.id); receivables_contact_id_foreign (contact_id → contacts.id); receivables_created_by_foreign (created_by → users.id); receivables_journal_id_foreign (journal_id → journals.id); receivables_type_transaction_id_foreign (type_transaction_id → type_transactions.id).

### `receivable_confirms` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `customer_id` | `int(11)` | NO | `—` | — | — |
| `start_date` | `date` | YES | `NULL` | — | — |
| `end_date` | `date` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `amount` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `receivable_confirm_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(11)` | NO | `—` | — | — |
| `receivable_id` | `int(11)` | NO | `—` | — | — |
| `amount` | `int(11)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `receivable_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_journal` | `tinyint(1)` | NO | `1` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `register_bbm` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vehicle_id` | `int(11)` | YES | `NULL` | MUL | — |
| `vehicle_maintenance_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_request` | `date` | YES | `NULL` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `date_pemakaian` | `date` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `varchar(255)` | YES | `NULL` | — | — |
| `peruntukkan` | `varchar(191)` | YES | `NULL` | — | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `spbu_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `requested_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `route_id` | `int(11)` | YES | `NULL` | — | — |
| `do_id` | `int(11)` | YES | `NULL` | — | — |
| `manifests_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `total` | `decimal(16,2)` | NO | `0.00` | — | — |
| `driver_id` | `int(11)` | YES | `NULL` | — | — |
| `jabatan` | `varchar(191)` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `update_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `reject_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `jatuh_tempo` | `date` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; register_bbm_manifests_id_foreign: manifests_id; register_bbm_requested_by_foreign: requested_by; register_bbm_spbu_id_foreign: spbu_id; register_bbm_vehicle_id_index: vehicle_id; register_bbm_warehouse_id_foreign: warehouse_id.  
**Foreign key:** register_bbm_manifests_id_foreign (manifests_id → manifests.id); register_bbm_requested_by_foreign (requested_by → contacts.id); register_bbm_spbu_id_foreign (spbu_id → contacts.id); register_bbm_warehouse_id_foreign (warehouse_id → warehouses.id).

### `register_bbm_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_maintenance_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `item_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cost_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `cost` | `double` | NO | `0` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `used` | `double` | NO | `0` | — | — |
| `is_internal` | `int(11)` | NO | `0` | — | — |
| `type` | `int(11)` | NO | `1` | — | — |
| `is_kasbon` | `int(11)` | NO | `0` | — | — |
| `qty_real` | `double` | NO | `0` | — | — |
| `cost_real` | `double` | NO | `0` | — | — |
| `total_real` | `double` | NO | `0` | — | — |
| `receive` | `double` | NO | `0` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `outbound_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; register_bbm_details_cost_id_foreign: cost_id; register_bbm_details_header_id_foreign: header_id; register_bbm_details_item_id_foreign: item_id; register_bbm_details_outbound_stock_transaction_id_index: outbound_stock_transaction_id; register_bbm_details_rack_id_index: rack_id; register_bbm_details_requested_stock_transaction_id_index: requested_stock_transaction_id; register_bbm_details_vehicle_maintenance_detail_id_foreign: vehicle_maintenance_detail_id; register_bbm_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id.  
**Foreign key:** register_bbm_details_cost_id_foreign (cost_id → cost_types.id); register_bbm_details_header_id_foreign (header_id → register_bbm.id); register_bbm_details_item_id_foreign (item_id → items.id); register_bbm_details_outbound_stock_transaction_id_foreign (outbound_stock_transaction_id → stock_transactions.id); register_bbm_details_requested_stock_transaction_id_foreign (requested_stock_transaction_id → stock_transactions.id); register_bbm_details_vehicle_maintenance_detail_id_foreign (vehicle_maintenance_detail_id → vehicle_maintenance_details.id).

### `reminder_types` — 4 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `interval` | `int(11)` | NO | `—` | — | — |
| `slug` | `varchar(191)` | NO | `—` | UNI | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; reminder_types_slug_unique (UNIQUE): slug.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `reminder_type_data` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `value` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `returs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `supplier_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `account_cash_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type_retur` | `int(11)` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `purchase_order_id` | `int(11)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; returs_account_cash_id_foreign: account_cash_id; returs_company_id_foreign: company_id; returs_create_by_foreign: create_by; returs_journal_id_foreign: journal_id; returs_supplier_id_foreign: supplier_id; returs_warehouse_id_foreign: warehouse_id.  
**Foreign key:** returs_account_cash_id_foreign (account_cash_id → accounts.id); returs_company_id_foreign (company_id → companies.id); returs_create_by_foreign (create_by → users.id); returs_journal_id_foreign (journal_id → journals.id); returs_supplier_id_foreign (supplier_id → contacts.id); returs_warehouse_id_foreign (warehouse_id → warehouses.id).

### `retur_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty_retur` | `double` | NO | `0` | — | — |
| `leftover` | `double` | NO | `0` | — | — |
| `receive` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `rack_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `outbound_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; retur_details_header_id_foreign: header_id; retur_details_item_id_foreign: item_id; retur_details_outbound_stock_transaction_id_index: outbound_stock_transaction_id; retur_details_rack_id_index: rack_id; retur_details_requested_stock_transaction_id_index: requested_stock_transaction_id; retur_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id.  
**Foreign key:** retur_details_header_id_foreign (header_id → returs.id); retur_details_item_id_foreign (item_id → items.id).

### `retur_receipts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_receipt` | `date` | NO | `—` | — | — |
| `receiver` | `varchar(191)` | NO | `—` | — | — |
| `deliver_no` | `varchar(191)` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; retur_receipts_company_id_foreign: company_id; retur_receipts_create_by_foreign: create_by; retur_receipts_header_id_foreign: header_id; retur_receipts_warehouse_id_foreign: warehouse_id.  
**Foreign key:** retur_receipts_company_id_foreign (company_id → companies.id); retur_receipts_create_by_foreign (create_by → users.id); retur_receipts_header_id_foreign (header_id → returs.id); retur_receipts_warehouse_id_foreign (warehouse_id → warehouses.id).

### `retur_receipt_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `retur_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `total_retur` | `double` | NO | `—` | — | — |
| `total_receipt` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; retur_receipt_details_header_id_foreign: header_id; retur_receipt_details_item_id_foreign: item_id; retur_receipt_details_retur_detail_id_foreign: retur_detail_id.  
**Foreign key:** retur_receipt_details_header_id_foreign (header_id → retur_receipts.id); retur_receipt_details_item_id_foreign (item_id → items.id); retur_receipt_details_retur_detail_id_foreign (retur_detail_id → retur_details.id).

### `retur_statuses` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | — |
| `name` | `varchar(20)` | NO | `—` | — | — |

**Indeks:** retur_statuses_id_unique (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `roles` — 1018 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `deep` | `int(11)` | NO | `—` | — | — |
| `urut` | `bigint(20)` | NO | `—` | — | — |
| `parent_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; roles_parent_id_index: parent_id.  
**Foreign key:** roles_parent_id_foreign (parent_id → roles.id).

### `routes` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `city_from` | `int(10) unsigned` | NO | `—` | MUL | — |
| `city_to` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `distance` | `int(11)` | NO | `0` | — | — |
| `duration` | `int(11)` | NO | `0` | — | — |
| `type_satuan` | `int(11)` | NO | `—` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `ritase_point` | `int(11)` | NO | `0` | — | — |
| `origin_address` | `varchar(191)` | YES | `NULL` | — | — |
| `origin_latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `origin_longitude` | `varchar(191)` | YES | `NULL` | — | — |
| `destination_address` | `varchar(191)` | YES | `NULL` | — | — |
| `destination_latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `destination_longitude` | `varchar(191)` | YES | `NULL` | — | — |
| `is_three_point` | `tinyint(1)` | YES | `0` | — | — |
| `city_to_2` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `destination_address_2` | `varchar(191)` | YES | `NULL` | — | — |
| `destination_latitude_2` | `varchar(191)` | YES | `NULL` | — | — |
| `destination_longitude_2` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; routes_city_from_foreign: city_from; routes_city_to_2_foreign: city_to_2; routes_city_to_foreign: city_to; routes_company_id_foreign: company_id; routes_created_by_foreign: created_by.  
**Foreign key:** routes_city_from_foreign (city_from → cities.id); routes_city_to_2_foreign (city_to_2 → cities.id); routes_city_to_foreign (city_to → cities.id); routes_company_id_foreign (company_id → companies.id); routes_created_by_foreign (created_by → users.id).

### `route_costs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `route_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `commodity_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `cost` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `header_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `container_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_container` | `tinyint(1)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; route_costs_commodity_id_foreign: commodity_id; route_costs_container_type_id_foreign: container_type_id; route_costs_created_by_foreign: created_by; route_costs_route_id_foreign: route_id.  
**Foreign key:** route_costs_commodity_id_foreign (commodity_id → commodities.id); route_costs_container_type_id_foreign (container_type_id → container_types.id); route_costs_created_by_foreign (created_by → users.id); route_costs_route_id_foreign (route_id → routes.id).

### `route_cost_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `cost_type_id` | `int(10) unsigned` | NO | `—` | — | — |
| `created_by` | `int(10) unsigned` | NO | `—` | — | — |
| `cost` | `double` | NO | `0` | — | — |
| `total_liter` | `int(11)` | NO | `0` | — | — |
| `is_bbm` | `tinyint(1)` | NO | `—` | — | — |
| `is_internal` | `tinyint(1)` | NO | `—` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `harga_satuan` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `sales_orders` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `job_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `customer_order_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `sales_order_status_id` | `int(11)` | NO | `—` | — | — |
| `jumlah_deposit` | `double` | NO | `0` | — | — |
| `is_deposit` | `int(11)` | NO | `0` | — | — |
| `invoice_id` | `int(11)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; sales_orders_job_order_id_index: job_order_id; sales_orders_journal_id_foreign: journal_id.  
**Foreign key:** sales_orders_job_order_id_foreign (job_order_id → job_orders.id); sales_orders_journal_id_foreign (journal_id → journals.id).

### `sales_order_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `price` | `double` | NO | `0` | — | — |
| `total_price` | `double` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; sales_order_details_header_id_foreign: header_id; sales_order_details_item_id_foreign: item_id.  
**Foreign key:** sales_order_details_header_id_foreign (header_id → sales_orders.id); sales_order_details_item_id_foreign (item_id → items.id).

### `sales_order_returns` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `sales_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `date_cancel` | `date` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; sales_order_returns_approve_by_foreign: approve_by; sales_order_returns_cancel_by_foreign: cancel_by; sales_order_returns_company_id_index: company_id; sales_order_returns_create_by_foreign: create_by; sales_order_returns_customer_id_index: customer_id; sales_order_returns_journal_id_foreign: journal_id; sales_order_returns_sales_order_id_foreign: sales_order_id; sales_order_returns_warehouse_id_foreign: warehouse_id.  
**Foreign key:** sales_order_returns_approve_by_foreign (approve_by → users.id); sales_order_returns_cancel_by_foreign (cancel_by → users.id); sales_order_returns_create_by_foreign (create_by → users.id); sales_order_returns_journal_id_foreign (journal_id → journals.id); sales_order_returns_sales_order_id_foreign (sales_order_id → sales_orders.id); sales_order_returns_warehouse_id_foreign (warehouse_id → warehouses.id).

### `sales_order_return_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `receive` | `double` | NO | `0` | — | — |
| `sales_order_detail_id` | `int(10) unsigned` | NO | `—` | — | — |
| `so_qty` | `double` | NO | `0` | — | — |
| `job_order_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; sales_order_return_details_header_id_foreign: header_id; sales_order_return_details_item_id_foreign: item_id; sales_order_return_details_job_order_detail_id_index: job_order_detail_id.  
**Foreign key:** sales_order_return_details_header_id_foreign (header_id → sales_order_returns.id); sales_order_return_details_item_id_foreign (item_id → items.id); sales_order_return_details_job_order_detail_id_foreign (job_order_detail_id → job_order_details.id).

### `sales_order_return_receipts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `sales_order_return_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_receipt_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `sales_order_return_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; sales_order_return_receipts_sales_order_return_detail_id_index: sales_order_return_detail_id; sales_order_return_receipts_sales_order_return_id_index: sales_order_return_id; sales_order_return_receipts_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; sales_order_return_receipts_warehouse_receipt_id_index: warehouse_receipt_id.  
**Foreign key:** sales_order_return_receipts_sales_order_return_detail_id_foreign (sales_order_return_detail_id → sales_order_return_details.id); sales_order_return_receipts_sales_order_return_id_foreign (sales_order_return_id → sales_order_returns.id); sales_order_return_receipts_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id); sales_order_return_receipts_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id).

### `sales_order_return_statuses` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(30)` | NO | `—` | — | — |
| `slug` | `varchar(30)` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; sales_order_return_statuses_slug_index: slug.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `sales_order_statuses` — 5 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `services` — 9 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `is_default` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `service_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_sale_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `service_group_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_warehouse` | `int(11)` | NO | `0` | — | — |
| `is_wh_rent` | `int(11)` | NO | `0` | — | — |
| `is_overtime` | `int(11)` | NO | `0` | — | — |
| `kpi_status_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_ppn` | `smallint(6)` | NO | `1` | — | — |
| `account_sale_temporary` | `int(11)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; services_account_sale_id_foreign: account_sale_id; services_kpi_status_id_foreign: kpi_status_id; services_service_group_id_foreign: service_group_id; service_type_for_id: service_type_id.  
**Foreign key:** services_account_sale_id_foreign (account_sale_id → accounts.id); services_kpi_status_id_foreign (kpi_status_id → kpi_statuses.id); services_service_group_id_foreign (service_group_id → service_groups.id); service_type_for_id (service_type_id → service_types.id).

### `service_groups` — 1 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `service_types` — 11 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `settings` — 8 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(30)` | NO | `—` | MUL | — |
| `name` | `varchar(30)` | NO | `—` | MUL | — |
| `content` | `text` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; settings_name_index: name; settings_slug_index: slug.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `setting_taxs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code_pref_suf` | `varchar(10)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `is_normal` | `tinyint(1)` | NO | `—` | — | — |
| `is_pengganti` | `tinyint(1)` | NO | `—` | — | — |
| `is_active` | `tinyint(1)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `shipment_statuses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_receipt_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `status` | `int(10) unsigned` | NO | `0` | MUL | — |
| `status_date` | `date` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; shipment_statuses_status_date_index: status_date; shipment_statuses_status_index: status; shipment_statuses_warehouse_receipt_id_index: warehouse_receipt_id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `solog_queue` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `action` | `varchar(191)` | NO | `—` | — | — |
| `table_name` | `varchar(191)` | NO | `—` | — | — |
| `parameters` | `text` | NO | `—` | — | — |
| `is_processed` | `tinyint(1)` | NO | `0` | — | — |
| `processed_at` | `datetime` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `stock_adjustments` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; stock_adjustments_company_id_foreign: company_id; stock_adjustments_create_by_foreign: create_by; stock_adjustments_warehouse_id_foreign: warehouse_id.  
**Foreign key:** stock_adjustments_company_id_foreign (company_id → companies.id); stock_adjustments_create_by_foreign (create_by → users.id); stock_adjustments_warehouse_id_foreign (warehouse_id → warehouses.id).

### `stock_adjustment_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; stock_adjustment_details_header_id_foreign: header_id; stock_adjustment_details_item_id_foreign: item_id.  
**Foreign key:** stock_adjustment_details_header_id_foreign (header_id → stock_adjustments.id); stock_adjustment_details_item_id_foreign (item_id → items.id).

### `stock_initials` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | — | — |
| `batch_no` | `varchar(191)` | YES | `NULL` | — | — |
| `stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `qty` | `double` | NO | `—` | — | — |
| `price` | `double` | NO | `—` | — | — |
| `total` | `double` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_tire_id` | `int(10) unsigned` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `stock_transactions` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | — | — |
| `type_transaction_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `qty_masuk` | `double` | NO | `0` | — | — |
| `qty_keluar` | `double` | NO | `0` | — | — |
| `harga_masuk` | `double` | NO | `0` | — | — |
| `harga_keluar` | `double` | NO | `0` | — | — |
| `jumlah_stok` | `int(11)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `no_surat_jalan` | `varchar(100)` | YES | `NULL` | — | — |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_approve` | `smallint(6)` | NO | `1` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; stock_transactions_customer_id_foreign: customer_id; stock_transactions_is_approve_index: is_approve; stock_transactions_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id.  
**Foreign key:** stock_transactions_customer_id_foreign (customer_id → contacts.id); stock_transactions_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `stock_transactions_report` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | — | — |
| `type_transaction_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `qty_masuk` | `double` | NO | `0` | — | — |
| `qty_keluar` | `double` | NO | `0` | — | — |
| `harga_masuk` | `double` | NO | `0` | — | — |
| `harga_keluar` | `double` | NO | `0` | — | — |
| `jumlah_stok` | `int(11)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; stock_transactions_report_header_id_foreign: header_id.  
**Foreign key:** stock_transactions_report_header_id_foreign (header_id → stock_transactions.id).

### `stok_opname_statuses` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(191)` | NO | `—` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; stok_opname_statuses_slug_index: slug.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `stok_opname_warehouses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_receipt_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `type` | `int(10) unsigned` | NO | `—` | — | — |
| `code` | `varchar(200)` | NO | `—` | — | — |
| `date_transactions` | `date` | NO | `—` | — | — |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `status` | `int(11)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; stok_opname_warehouses_created_by_foreign: created_by; stok_opname_warehouses_customer_id_foreign: customer_id; stok_opname_warehouses_warehouse_id_foreign: warehouse_id; stok_opname_warehouses_warehouse_receipt_id_foreign: warehouse_receipt_id.  
**Foreign key:** stok_opname_warehouses_created_by_foreign (created_by → users.id); stok_opname_warehouses_customer_id_foreign (customer_id → contacts.id); stok_opname_warehouses_warehouse_id_foreign (warehouse_id → warehouses.id); stok_opname_warehouses_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id).

### `stok_opname_warehouse_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | — | — |
| `stock_sistem` | `int(11)` | NO | `—` | — | — |
| `stock_riil` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `rack_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `no_surat_jalan` | `varchar(300)` | NO | `—` | — | — |
| `warehouse_receipt_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; stok_opname_warehouse_details_header_id_foreign: header_id; stok_opname_warehouse_details_rack_id_foreign: rack_id; stok_opname_warehouse_details_warehouse_receipt_id_foreign: warehouse_receipt_id.  
**Foreign key:** stok_opname_warehouse_details_header_id_foreign (header_id → stok_opname_warehouses.id); stok_opname_warehouse_details_rack_id_foreign (rack_id → racks.id); stok_opname_warehouse_details_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id).

### `storage_types` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_handling_area` | `int(11)` | NO | `0` | — | — |
| `is_picking_area` | `int(11)` | NO | `0` | — | — |
| `is_stripping_area` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `storings` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `date_check` | `date` | NO | `—` | — | — |
| `officer` | `varchar(191)` | NO | `—` | — | — |
| `location` | `varchar(191)` | YES | `NULL` | — | — |
| `photo_before` | `varchar(191)` | YES | `NULL` | — | — |
| `photo_after` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; storings_company_id_foreign: company_id; storings_vehicle_id_foreign: vehicle_id.  
**Foreign key:** storings_company_id_foreign (company_id → companies.id); storings_vehicle_id_foreign (vehicle_id → vehicles.id).

### `stuffings` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(11)` | NO | `—` | — | — |
| `job_order_id` | `int(11)` | NO | `—` | — | — |
| `vehicle_id` | `int(11)` | NO | `—` | — | — |
| `container_id` | `int(11)` | NO | `—` | — | — |
| `start_time` | `time` | NO | `—` | — | — |
| `end_time` | `time` | NO | `—` | — | — |
| `staff_gudang_name` | `varchar(200)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_overtime` | `int(11)` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `stuffing_vehicles` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `stuffing_id` | `int(11)` | NO | `—` | — | — |
| `space_type` | `varchar(20)` | NO | `—` | — | — |
| `no_seal` | `varchar(20)` | NO | `—` | — | — |
| `carrier_size` | `int(11)` | YES | `NULL` | — | — |
| `driver_name` | `varchar(150)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `carrier_name` | `varchar(100)` | NO | `—` | — | — |
| `no_carrier` | `varchar(100)` | NO | `—` | — | — |
| `no_container` | `varchar(100)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `submission_costs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `relation_cost_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `approve_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cancel_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `date_submission` | `date` | NO | `—` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `date_cancel` | `date` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `type_submission` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `revision_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `approve_revision_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `date_approve_revision` | `datetime` | YES | `NULL` | — | — |
| `journal_posting_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `payable_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `cash_transaction_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `revision_date` | `datetime` | YES | `NULL` | — | — |
| `slug` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `target_rates` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `plan` | `double` | NO | `0` | — | — |
| `realisasi` | `double` | NO | `0` | — | — |
| `period` | `date` | NO | `—` | — | — |
| `username` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `taxes` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `non_npwp` | `decimal(8,2)` | NO | `—` | — | — |
| `npwp` | `decimal(8,2)` | NO | `—` | — | — |
| `pemotong_pemungut` | `int(11)` | NO | `—` | — | — |
| `akun_pembelian` | `int(10) unsigned` | NO | `—` | MUL | — |
| `akun_penjualan` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_default` | `int(10) unsigned` | NO | `0` | MUL | — |
| `is_ppn` | `int(10) unsigned` | NO | `0` | MUL | — |
| `is_pph` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; taxes_akun_pembelian_foreign: akun_pembelian; taxes_akun_penjualan_foreign: akun_penjualan; taxes_is_default_index: is_default; taxes_is_ppn_index: is_ppn.  
**Foreign key:** taxes_akun_pembelian_foreign (akun_pembelian → accounts.id); taxes_akun_penjualan_foreign (akun_penjualan → accounts.id).

### `tax_invoices` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `expiry_date` | `date` | NO | `—` | — | — |
| `invoice_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_active` | `int(11)` | NO | `1` | MUL | — |
| `start_date` | `date` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; tax_invoices_invoice_id_index: invoice_id; tax_invoices_is_active_index: is_active; tax_invoices_start_date_index: start_date.  
**Foreign key:** tax_invoices_invoice_id_foreign (invoice_id → invoices.id).

### `tire_categories` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `tire_manufacturers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `tire_numberings` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `kode_lokasi` | `varchar(191)` | NO | `—` | — | — |
| `tahun_tms` | `varchar(191)` | NO | `—` | — | — |
| `bulan_tms` | `varchar(191)` | NO | `—` | — | — |
| `nomor_terakhir` | `int(11)` | NO | `—` | — | — |
| `company_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; tire_numberings_company_id_foreign: company_id.  
**Foreign key:** tire_numberings_company_id_foreign (company_id → companies.id).

### `tire_on_offs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `tire_on_off_category_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `request_date` | `date` | YES | `NULL` | — | — |
| `approve_date` | `date` | YES | `NULL` | — | — |
| `status` | `tinyint(4)` | NO | `—` | — | — |
| `approved_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `rejected_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `reject_reason` | `text` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; tire_on_offs_approved_by_foreign: approved_by; tire_on_offs_company_id_foreign: company_id; tire_on_offs_rejected_by_foreign: rejected_by; tire_on_offs_tire_on_off_category_id_foreign: tire_on_off_category_id.  
**Foreign key:** tire_on_offs_approved_by_foreign (approved_by → users.id); tire_on_offs_company_id_foreign (company_id → companies.id); tire_on_offs_rejected_by_foreign (rejected_by → users.id); tire_on_offs_tire_on_off_category_id_foreign (tire_on_off_category_id → tire_on_off_categories.id).

### `tire_on_off_categories` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `slug` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `tire_on_off_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vehicle_from_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vehicle_tire_from_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `status_lepas_ban_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `ban_luar_from_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `ban_dalam_from_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `marset_from_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_to_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_tire_to_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `ban_luar_to_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `ban_dalam_to_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `marset_to_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `biaya_jasa` | `int(11)` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; tire_on_off_details_status_lepas_ban_id_foreign: status_lepas_ban_id.  
**Foreign key:** tire_on_off_details_status_lepas_ban_id_foreign (status_lepas_ban_id → tire_statuses.id).

### `tire_sizes` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `tire_statuses` — 4 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `tire_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `type_transactions` — 49 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `slug` | `varchar(150)` | NO | `—` | UNI | — |
| `is_hidden` | `smallint(6)` | NO | `0` | — | — |
| `is_saldo` | `tinyint(1)` | NO | `0` | — | — |
| `is_journal` | `tinyint(1)` | NO | `1` | — | — |
| `is_penyesuaian` | `tinyint(1)` | NO | `0` | — | — |
| `is_lock` | `tinyint(1)` | NO | `0` | — | — |
| `last_date_lock` | `date` | YES | `NULL` | — | — |
| `is_customable_field` | `smallint(6)` | NO | `0` | — | — |
| `table_name` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; type_trx_slug_unique (UNIQUE): slug.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `um_customers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `sales_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `receivable_id` | `bigint(20) unsigned` | YES | `NULL` | — | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; um_customers_account_id_foreign: account_id; um_customers_company_id_foreign: company_id; um_customers_contact_id_foreign: contact_id; um_customers_created_by_foreign: created_by; um_customers_journal_id_foreign: journal_id; um_customers_sales_order_id_foreign: sales_order_id; um_customers_type_transaction_id_foreign: type_transaction_id.  
**Foreign key:** um_customers_account_id_foreign (account_id → accounts.id); um_customers_company_id_foreign (company_id → companies.id); um_customers_contact_id_foreign (contact_id → contacts.id); um_customers_created_by_foreign (created_by → users.id); um_customers_journal_id_foreign (journal_id → journals.id); um_customers_sales_order_id_foreign (sales_order_id → sales_orders.id); um_customers_type_transaction_id_foreign (type_transaction_id → type_transactions.id).

### `um_customer_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `um_customer_paids` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `type_paid` | `int(10) unsigned` | NO | `—` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `reff_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `amount` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `um_suppliers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `contact_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `payable_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `status` | `tinyint(4)` | NO | `1` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; um_suppliers_account_id_foreign: account_id; um_suppliers_company_id_foreign: company_id; um_suppliers_contact_id_foreign: contact_id; um_suppliers_created_by_foreign: created_by; um_suppliers_journal_id_foreign: journal_id; um_suppliers_type_transaction_id_foreign: type_transaction_id.  
**Foreign key:** um_suppliers_account_id_foreign (account_id → accounts.id); um_suppliers_company_id_foreign (company_id → companies.id); um_suppliers_contact_id_foreign (contact_id → contacts.id); um_suppliers_created_by_foreign (created_by → users.id); um_suppliers_journal_id_foreign (journal_id → journals.id); um_suppliers_type_transaction_id_foreign (type_transaction_id → type_transactions.id).

### `um_supplier_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `relation_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `debet` | `double` | NO | `0` | — | — |
| `credit` | `double` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `um_supplier_paids` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `type_paid` | `int(10) unsigned` | NO | `—` | — | — |
| `type_transaction_id` | `int(10) unsigned` | NO | `—` | — | — |
| `reff_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `amount` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `users` — 1 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `email` | `varchar(191)` | NO | `—` | UNI | — |
| `password` | `varchar(191)` | NO | `—` | — | — |
| `api_token` | `varchar(191)` | YES | `NULL` | — | — |
| `remember_token` | `varchar(100)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `contact_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `username` | `varchar(191)` | NO | `—` | UNI | — |
| `city_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `last_login` | `datetime` | YES | `NULL` | — | — |
| `pass_text` | `varchar(191)` | YES | `NULL` | — | — |
| `group_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_admin` | `tinyint(1)` | YES | `0` | — | — |
| `last_login_ip` | `varchar(191)` | YES | `NULL` | — | — |
| `is_customer` | `tinyint(1)` | NO | `0` | — | — |
| `is_vendor` | `tinyint(1)` | NO | `0` | — | — |
| `is_driver` | `tinyint(1)` | NO | `0` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |
| `due_date` | `datetime` | YES | `NULL` | — | — |
| `slug` | `varchar(30)` | YES | `NULL` | MUL | — |
| `fcm_token` | `text` | YES | `NULL` | — | — |
| `dashboard_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_multibranch` | `tinyint(1)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; users_dashboard_id_foreign: dashboard_id; users_email_unique (UNIQUE): email; users_slug_index: slug; users_username_unique (UNIQUE): username.  
**Foreign key:** users_dashboard_id_foreign (dashboard_id → dashboards.id).

### `user_activities` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `user_id` | `varchar(191)` | YES | `NULL` | — | — |
| `relation_id` | `varchar(191)` | YES | `NULL` | — | — |
| `username` | `varchar(191)` | YES | `NULL` | — | — |
| `activity` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `user_roles` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `user_id` | `int(10) unsigned` | NO | `—` | — | — |
| `role_id` | `int(10) unsigned` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `using_items` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_maintenance_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_request` | `date` | NO | `—` | — | — |
| `date_approve` | `date` | NO | `—` | — | — |
| `date_pemakaian` | `date` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `is_equipment` | `tinyint(1)` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `peruntukkan` | `varchar(191)` | YES | `NULL` | — | — |
| `requested_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; using_items_company_id_foreign: company_id; using_items_requested_by_foreign: requested_by; using_items_vehicle_id_index: vehicle_id; using_items_vehicle_maintenance_id_foreign: vehicle_maintenance_id; using_items_warehouse_id_foreign: warehouse_id.  
**Foreign key:** using_items_company_id_foreign (company_id → companies.id); using_items_requested_by_foreign (requested_by → contacts.id); using_items_vehicle_id_foreign (vehicle_id → vehicles.id); using_items_vehicle_maintenance_id_foreign (vehicle_maintenance_id → vehicle_maintenances.id); using_items_warehouse_id_foreign (warehouse_id → warehouses.id).

### `using_item_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_maintenance_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `cost` | `double` | NO | `0` | — | — |
| `total` | `double` | NO | `0` | — | — |
| `used` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `receive` | `double` | NO | `0` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `requested_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `outbound_stock_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; using_item_details_header_id_foreign: header_id; using_item_details_item_id_foreign: item_id; using_item_details_outbound_stock_transaction_id_index: outbound_stock_transaction_id; using_item_details_rack_id_index: rack_id; using_item_details_requested_stock_transaction_id_index: requested_stock_transaction_id; using_item_details_vehicle_maintenance_detail_id_foreign: vehicle_maintenance_detail_id; using_item_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id.  
**Foreign key:** using_item_details_header_id_foreign (header_id → using_items.id); using_item_details_item_id_foreign (item_id → items.id); using_item_details_outbound_stock_transaction_id_foreign (outbound_stock_transaction_id → stock_transactions.id); using_item_details_requested_stock_transaction_id_foreign (requested_stock_transaction_id → stock_transactions.id); using_item_details_vehicle_maintenance_detail_id_foreign (vehicle_maintenance_detail_id → vehicle_maintenance_details.id).

### `using_item_statuses` — 6 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(30)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `using_tires` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_tire_id` | `bigint(20) unsigned` | NO | `—` | MUL | — |
| `date_of_use` | `timestamp` | YES | `NULL` | — | — |
| `date_out` | `timestamp` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `wh_stock_ban_luar_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `wh_stock_ban_dalam_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `wh_stock_marset_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; using_tires_vehicle_id_foreign: vehicle_id; using_tires_vehicle_tire_id_foreign: vehicle_tire_id; using_tires_wh_stock_ban_dalam_id_foreign: wh_stock_ban_dalam_id; using_tires_wh_stock_marset_id_foreign: wh_stock_marset_id.  
**Foreign key:** using_tires_vehicle_id_foreign (vehicle_id → vehicles.id); using_tires_vehicle_tire_id_foreign (vehicle_tire_id → vehicle_tires.id); using_tires_wh_stock_ban_dalam_id_foreign (wh_stock_ban_dalam_id → warehouse_stock_details.id); using_tires_wh_stock_marset_id_foreign (wh_stock_marset_id → warehouse_stock_details.id).

### `vehicles` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_variant_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_owner_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `supplier_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `nopol` | `varchar(191)` | YES | `NULL` | — | — |
| `chassis_no` | `varchar(191)` | YES | `NULL` | — | — |
| `machine_no` | `varchar(191)` | YES | `NULL` | — | — |
| `color` | `varchar(191)` | YES | `NULL` | — | — |
| `date_manufacture` | `date` | YES | `NULL` | — | — |
| `date_operation` | `date` | YES | `NULL` | — | — |
| `is_active` | `tinyint(1)` | NO | `—` | — | — |
| `not_active_reason` | `varchar(191)` | YES | `NULL` | — | — |
| `stnk_no` | `varchar(191)` | YES | `NULL` | — | — |
| `stnk_name` | `varchar(191)` | YES | `NULL` | — | — |
| `stnk_date` | `date` | NO | `—` | — | — |
| `stnk_address` | `varchar(191)` | YES | `NULL` | — | — |
| `bpkb_no` | `varchar(191)` | YES | `NULL` | — | — |
| `kir_date` | `date` | NO | `—` | — | — |
| `initial_km` | `int(11)` | NO | `0` | — | — |
| `initial_km_date` | `date` | YES | `NULL` | — | — |
| `last_km` | `int(11)` | NO | `0` | — | — |
| `last_km_date` | `date` | YES | `NULL` | — | — |
| `daily_distance` | `int(11)` | NO | `0` | — | — |
| `gps_no` | `varchar(191)` | YES | `NULL` | — | — |
| `serep_tire` | `int(11)` | NO | `0` | — | — |
| `is_trailer` | `int(11)` | NO | `1` | — | — |
| `trailer_size` | `int(11)` | YES | `NULL` | — | — |
| `max_tonase` | `int(11)` | YES | `NULL` | — | — |
| `max_volume` | `int(11)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `delivery_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_internal` | `int(11)` | NO | `1` | — | — |
| `image` | `varchar(191)` | YES | `NULL` | — | — |
| `last_longitude` | `varchar(191)` | NO | `'0'` | — | — |
| `last_latitude` | `varchar(191)` | NO | `'0'` | — | — |
| `last_update_latlng` | `datetime` | NO | `'0000-00-00 00:00:00'` | — | — |
| `last_driver_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `last_update_driver` | `datetime` | NO | `'0000-00-00 00:00:00'` | — | — |
| `last_delivery_order_driver_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `last_update_delivery_order_driver` | `datetime` | NO | `'0000-00-00 00:00:00'` | — | — |
| `no_imei` | `varchar(191)` | YES | `NULL` | — | — |
| `gps_provider_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `bbm_capacity` | `int(11)` | NO | `—` | — | — |
| `bbm_usage_ratio` | `int(11)` | NO | `—` | — | — |
| `last_km_gps` | `int(11)` | NO | `0` | — | — |
| `last_km_gps_date` | `timestamp` | YES | `NULL` | — | — |
| `is_use_km_gps` | `tinyint(4)` | NO | `—` | — | — |
| `trailer_id` | `varchar(191)` | YES | `NULL` | — | — |
| `connected_date` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicles_company_id_foreign: company_id; vehicles_delivery_id_foreign: delivery_id; vehicles_gps_provider_id_foreign: gps_provider_id; vehicles_supplier_id_foreign: supplier_id; vehicles_vehicle_owner_id_foreign: vehicle_owner_id; vehicles_vehicle_variant_id_foreign: vehicle_variant_id.  
**Foreign key:** vehicles_company_id_foreign (company_id → companies.id); vehicles_delivery_id_foreign (delivery_id → delivery_order_drivers.id); vehicles_gps_provider_id_foreign (gps_provider_id → contacts.id); vehicles_supplier_id_foreign (supplier_id → contacts.id); vehicles_vehicle_owner_id_foreign (vehicle_owner_id → vehicle_owners.id); vehicles_vehicle_variant_id_foreign (vehicle_variant_id → vehicle_variants.id).

### `vehicle_bodies` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `is_active` | `tinyint(1)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_checklists` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `is_active` | `tinyint(1)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_checklist_detail_bodies` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_body_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `is_exist` | `tinyint(1)` | NO | `—` | — | — |
| `is_function` | `tinyint(1)` | NO | `—` | — | — |
| `condition` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_checklist_detail_bodies_header_id_foreign: header_id; vehicle_checklist_detail_bodies_vehicle_body_id_foreign: vehicle_body_id.  
**Foreign key:** vehicle_checklist_detail_bodies_header_id_foreign (header_id → vehicle_checklist_items.id); vehicle_checklist_detail_bodies_vehicle_body_id_foreign (vehicle_body_id → vehicle_bodies.id).

### `vehicle_checklist_detail_items` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_checklist_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `is_exist` | `tinyint(1)` | NO | `—` | — | — |
| `is_function` | `tinyint(1)` | NO | `—` | — | — |
| `condition` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_checklist_detail_items_header_id_foreign: header_id; vehicle_checklist_detail_items_vehicle_checklist_id_foreign: vehicle_checklist_id.  
**Foreign key:** vehicle_checklist_detail_items_header_id_foreign (header_id → vehicle_checklist_items.id); vehicle_checklist_detail_items_vehicle_checklist_id_foreign (vehicle_checklist_id → vehicle_checklists.id).

### `vehicle_checklist_items` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `officer` | `varchar(191)` | NO | `—` | — | — |
| `date_transaction` | `date` | NO | `—` | — | — |
| `score` | `double` | NO | `0` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `time_transaction` | `time` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_checklist_items_score_index: score.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_contacts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `contact_id` | `int(10) unsigned` | NO | `—` | — | — |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | — | — |
| `last_used` | `date` | YES | `NULL` | — | — |
| `is_active` | `tinyint(1)` | NO | `0` | — | — |
| `driver_status` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_distances` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | — | — |
| `create_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `date_distance` | `date` | NO | `—` | — | — |
| `distance` | `double` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_documents` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `file_name` | `varchar(191)` | NO | `—` | — | — |
| `date_upload` | `date` | NO | `—` | — | — |
| `extension` | `varchar(191)` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `nomor_dokumen` | `varchar(191)` | YES | `NULL` | — | — |
| `expired_date_dokumen` | `date` | YES | `NULL` | — | — |
| `alert_interval` | `int(11)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_documents_vehicle_id_foreign: vehicle_id.  
**Foreign key:** vehicle_documents_vehicle_id_foreign (vehicle_id → vehicles.id).

### `vehicle_drivers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `driver_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_drivers_driver_id_index: driver_id; vehicle_drivers_vehicle_id_index: vehicle_id.  
**Foreign key:** vehicle_drivers_driver_id_foreign (driver_id → contacts.id); vehicle_drivers_vehicle_id_foreign (vehicle_id → vehicles.id).

### `vehicle_insurances` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `insurance_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `account_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `journal_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `payment` | `int(11)` | YES | `NULL` | — | — |
| `termin` | `int(11)` | NO | `0` | — | — |
| `premi` | `double` | NO | `—` | — | — |
| `polis_no` | `varchar(191)` | NO | `—` | — | — |
| `tjh` | `varchar(191)` | NO | `—` | — | — |
| `start_date` | `date` | NO | `—` | — | — |
| `end_date` | `date` | NO | `—` | — | — |
| `date_credit` | `date` | NO | `—` | — | — |
| `is_active` | `tinyint(1)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_insurances_account_id_foreign: account_id; vehicle_insurances_insurance_id_foreign: insurance_id; vehicle_insurances_journal_id_foreign: journal_id; vehicle_insurances_vehicle_id_foreign: vehicle_id.  
**Foreign key:** vehicle_insurances_account_id_foreign (account_id → accounts.id); vehicle_insurances_insurance_id_foreign (insurance_id → contacts.id); vehicle_insurances_journal_id_foreign (journal_id → journals.id); vehicle_insurances_vehicle_id_foreign (vehicle_id → vehicles.id).

### `vehicle_joints` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `tires` | `int(11)` | NO | `—` | — | — |
| `images` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `sumbu` | `int(11)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_joint_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_joint_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `km_ganti` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_joint_details_vehicle_joint_id_foreign: vehicle_joint_id.  
**Foreign key:** vehicle_joint_details_vehicle_joint_id_foreign (vehicle_joint_id → vehicle_joints.id).

### `vehicle_km_gps_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `imei` | `varchar(191)` | YES | `NULL` | — | — |
| `gsm_no` | `varchar(191)` | YES | `NULL` | — | — |
| `log_date` | `date` | NO | `—` | — | — |
| `odometer` | `double(10,2)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `lattitude` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_km_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | — | — |
| `log_date` | `date` | NO | `—` | — | — |
| `update_via` | `tinyint(4)` | NO | `—` | — | — |
| `odometer` | `double(10,2)` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_locations` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `delivery_order_driver_id` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | NO | `'0'` | — | — |
| `latitude` | `varchar(191)` | NO | `'0'` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_maintenances` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `bengkel_id` | `int(11)` | YES | `NULL` | — | — |
| `mechanic_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `po_maintenance_code` | `varchar(191)` | YES | `NULL` | — | — |
| `spk_code` | `varchar(191)` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `saran_penggunaan` | `varchar(191)` | YES | `NULL` | — | — |
| `km_rencana` | `double` | NO | `0` | — | — |
| `cost_rencana` | `double` | NO | `0` | — | — |
| `date_pengajuan` | `date` | NO | `—` | — | — |
| `date_rencana` | `date` | NO | `—` | — | — |
| `date_perawatan` | `date` | YES | `NULL` | — | — |
| `km_realisasi` | `double` | NO | `0` | — | — |
| `cost_realisasi` | `double` | NO | `0` | — | — |
| `date_realisasi` | `date` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `2` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `issue` | `varchar(191)` | YES | `NULL` | — | — |
| `is_internal` | `tinyint(1)` | NO | `1` | — | — |
| `is_head` | `tinyint(4)` | NO | `0` | — | — |
| `is_trailer` | `tinyint(4)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `warehouse_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_maintenances_company_id_foreign: company_id; vehicle_maintenances_mechanic_id_foreign: mechanic_id; vehicle_maintenances_vehicle_id_foreign: vehicle_id; vehicle_maintenances_vendor_id_foreign: vendor_id; vehicle_maintenances_wh_id_foreign: warehouse_id.  
**Foreign key:** vehicle_maintenances_company_id_foreign (company_id → companies.id); vehicle_maintenances_mechanic_id_foreign (mechanic_id → contacts.id); vehicle_maintenances_vehicle_id_foreign (vehicle_id → vehicles.id); vehicle_maintenances_vendor_id_foreign (vendor_id → contacts.id); vehicle_maintenances_wh_id_foreign (warehouse_id → warehouses.id).

### `vehicle_maintenance_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_maintenance_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `tipe_kegiatan` | `int(11)` | NO | `—` | — | — |
| `qty_rencana` | `double` | NO | `0` | — | — |
| `cost_rencana` | `double` | NO | `0` | — | — |
| `total_rencana` | `double` | NO | `0` | — | — |
| `qty_realisasi` | `double` | NO | `0` | — | — |
| `cost_realisasi` | `double` | NO | `0` | — | — |
| `total_realisasi` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_maintenance_details_header_id_foreign: header_id; vehicle_maintenance_details_item_id_foreign: item_id; vehicle_maintenance_details_rack_id_index: rack_id; vehicle_maintenance_details_vehicle_maintenance_type_id_foreign: vehicle_maintenance_type_id; vehicle_maintenance_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id.  
**Foreign key:** vehicle_maintenance_details_header_id_foreign (header_id → vehicle_maintenances.id); vehicle_maintenance_details_item_id_foreign (item_id → items.id); vehicle_maintenance_details_rack_id_foreign (rack_id → racks.id); vehicle_maintenance_details_vehicle_maintenance_type_id_foreign (vehicle_maintenance_type_id → vehicle_maintenance_types.id); vehicle_maintenance_details_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `vehicle_maintenance_documents` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `file_name` | `varchar(191)` | NO | `—` | — | — |
| `extension` | `varchar(191)` | NO | `—` | — | — |
| `upload_date` | `date` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_issue` | `int(11)` | NO | `0` | — | — |
| `is_spk` | `int(11)` | NO | `0` | — | — |
| `is_rencana` | `int(11)` | NO | `0` | — | — |
| `is_vehicle` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_maintenance_items` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_maintenance_id` | `int(10) unsigned` | NO | `—` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | — | — |
| `qty` | `int(11)` | NO | `0` | — | — |
| `price` | `int(11)` | NO | `0` | — | — |
| `total_price` | `int(11)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `price_realisasi` | `int(11)` | NO | `0` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_maintenance_logs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `description` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `title` | `varchar(191)` | NO | `—` | — | — |
| `vehicle_checklist_items_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_maintenance_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_maintenance_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `interval` | `int(11)` | NO | `—` | — | — |
| `cost` | `double` | NO | `—` | — | — |
| `is_repeat` | `tinyint(1)` | NO | `—` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_manufacturers` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_mutation_ins` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `sender_company_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `receiver_company_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `date_send` | `date` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `approve_ho_by` | `bigint(20) unsigned` | YES | `NULL` | — | — |
| `approve_ho_at` | `datetime` | YES | `NULL` | — | — |
| `vehicle_mutation_request_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_mutation_in_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_variant_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_owner_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `last_km` | `int(11)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_mutation_outs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `sender_company_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `receiver_company_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `date_send` | `date` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `approve_ho_by` | `bigint(20) unsigned` | YES | `NULL` | — | — |
| `approve_ho_at` | `datetime` | YES | `NULL` | — | — |
| `vehicle_mutation_request_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_mutation_out_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_variant_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_owner_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `last_km` | `int(11)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_mutation_requests` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `date_request` | `date` | NO | `—` | — | — |
| `date_needed` | `date` | NO | `—` | — | — |
| `sender_company_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `receiver_company_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `requested_by` | `bigint(20) unsigned` | NO | `—` | — | — |
| `file` | `varchar(191)` | YES | `NULL` | — | — |
| `approve_ho_by` | `bigint(20) unsigned` | YES | `NULL` | — | — |
| `approve_ho_at` | `datetime` | YES | `NULL` | — | — |
| `approve_hq_by` | `bigint(20) unsigned` | YES | `NULL` | — | — |
| `approve_hq_at` | `datetime` | YES | `NULL` | — | — |
| `mutation_out_code` | `varchar(191)` | YES | `'0'` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_mutation_request_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_variant_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `vehicle_owner_id` | `bigint(20) unsigned` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `last_km` | `int(11)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_owners` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `owner` | `enum('internal','vendor','sewa','pihak_ketiga','bagi_hasil')` | NO | `'internal'` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_tires` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_joint_detail_id` | `int(10) unsigned` | NO | `—` | — | — |
| `description` | `varchar(191)` | NO | `—` | — | — |
| `date_mutation` | `date` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `wh_stock_ban_luar_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `wh_stock_ban_dalam_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `wh_stock_marset_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_tires_vehicle_id_foreign: vehicle_id; vehicle_tires_warehouse_stock_detail_id_foreign: wh_stock_ban_luar_id; vehicle_tires_wh_stock_ban_dalam_id_foreign: wh_stock_ban_dalam_id; vehicle_tires_wh_stock_marset_id_foreign: wh_stock_marset_id.  
**Foreign key:** vehicle_tires_vehicle_id_foreign (vehicle_id → vehicles.id); vehicle_tires_warehouse_stock_detail_id_foreign (wh_stock_ban_luar_id → warehouse_stock_details.id); vehicle_tires_wh_stock_ban_dalam_id_foreign (wh_stock_ban_dalam_id → warehouse_stock_details.id); vehicle_tires_wh_stock_marset_id_foreign (wh_stock_marset_id → warehouse_stock_details.id).

### `vehicle_trailer_connections` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `requested_date` | `date` | NO | `—` | — | — |
| `approved_date` | `date` | YES | `NULL` | — | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `status` | `int(11)` | NO | `—` | — | — |
| `vehicle_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `trailer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_trailer_connections_company_id_foreign: company_id; vehicle_trailer_connections_trailer_id_foreign: trailer_id; vehicle_trailer_connections_vehicle_id_foreign: vehicle_id.  
**Foreign key:** vehicle_trailer_connections_company_id_foreign (company_id → companies.id); vehicle_trailer_connections_trailer_id_foreign (trailer_id → vehicles.id); vehicle_trailer_connections_vehicle_id_foreign (vehicle_id → vehicles.id).

### `vehicle_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | YES | `NULL` | — | — |
| `type` | `int(11)` | NO | `1` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vehicle_variants` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vehicle_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_manufacturer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `bbm_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `vehicle_joint_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `tire_size_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `transmission` | `int(10) unsigned` | NO | `—` | — | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `year_manufacture` | `int(11)` | YES | `NULL` | — | — |
| `cylinder` | `int(11)` | YES | `NULL` | — | — |
| `cc_capacity` | `int(11)` | YES | `NULL` | — | — |
| `bbm_capacity` | `int(11)` | YES | `NULL` | — | — |
| `joints` | `int(11)` | NO | `—` | — | — |
| `seat` | `int(11)` | YES | `NULL` | — | — |
| `first_km_initial` | `int(11)` | YES | `0` | — | — |
| `next_km_initial` | `int(11)` | YES | `0` | — | — |
| `cost` | `int(11)` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `bbm_usage_ratio` | `int(11)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vehicle_variants_bbm_type_id_foreign: bbm_type_id; vehicle_variants_tire_size_id_foreign: tire_size_id; vehicle_variants_vehicle_joint_id_foreign: vehicle_joint_id; vehicle_variants_vehicle_manufacturer_id_foreign: vehicle_manufacturer_id; vehicle_variants_vehicle_type_id_foreign: vehicle_type_id.  
**Foreign key:** vehicle_variants_bbm_type_id_foreign (bbm_type_id → bbm_types.id); vehicle_variants_tire_size_id_foreign (tire_size_id → tire_sizes.id); vehicle_variants_vehicle_joint_id_foreign (vehicle_joint_id → vehicle_joints.id); vehicle_variants_vehicle_manufacturer_id_foreign (vehicle_manufacturer_id → vehicle_manufacturers.id); vehicle_variants_vehicle_type_id_foreign (vehicle_type_id → vehicle_types.id).

### `vendor_job_statuses` — 3 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `priority` | `smallint(6)` | NO | `1` | MUL | — |
| `editable` | `smallint(6)` | NO | `0` | MUL | — |
| `name` | `varchar(50)` | NO | `—` | MUL | — |
| `slug` | `varchar(50)` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vendor_job_statuses_editable_index: editable; vendor_job_statuses_name_index: name; vendor_job_statuses_priority_index: priority; vendor_job_statuses_slug_index: slug.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vendor_prices` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vendor_id` | `int(10) unsigned` | NO | `—` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `route_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `service_id` | `int(10) unsigned` | NO | `—` | — | — |
| `service_type_id` | `int(10) unsigned` | NO | `—` | — | — |
| `commodity_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `moda_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `container_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `rack_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `created_by` | `int(10) unsigned` | NO | `—` | — | — |
| `updated_by` | `int(10) unsigned` | YES | `NULL` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `min_tonase` | `double` | YES | `NULL` | — | — |
| `price_tonase` | `double` | YES | `NULL` | — | — |
| `min_volume` | `double` | YES | `NULL` | — | — |
| `price_volume` | `double` | YES | `NULL` | — | — |
| `min_item` | `double` | YES | `NULL` | — | — |
| `price_item` | `double` | YES | `NULL` | — | — |
| `price_full` | `double` | YES | `NULL` | — | — |
| `piece_name` | `varchar(191)` | YES | `NULL` | — | — |
| `is_active` | `tinyint(1)` | NO | `1` | — | — |
| `imposition` | `int(11)` | YES | `0` | — | — |
| `price_imposition` | `double` | YES | `NULL` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `price_handling_tonase` | `double` | YES | `NULL` | — | — |
| `price_handling_volume` | `double` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `cost_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `date` | `date` | NO | `—` | MUL | — |
| `cost_category` | `int(11)` | NO | `0` | MUL | — |
| `is_used` | `int(11)` | NO | `1` | MUL | — |
| `is_approve` | `tinyint(1)` | NO | `0` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; vendor_prices_cost_category_index: cost_category; vendor_prices_cost_type_id_index: cost_type_id; vendor_prices_date_index: date; vendor_prices_is_used_index: is_used.  
**Foreign key:** vendor_prices_cost_type_id_foreign (cost_type_id → cost_types.id).

### `vendor_types` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vessels` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `vendor_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; vessel_vendor_id_for: vendor_id.  
**Foreign key:** vessel_vendor_id_for (vendor_id → contacts.id).

### `voyage_receipts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `voyage_schedule_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_receipt_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; voyage_receipts_voyage_schedule_id_index: voyage_schedule_id; voyage_receipts_warehouse_receipt_id_index: warehouse_receipt_id.  
**Foreign key:** voyage_receipts_voyage_schedule_id_foreign (voyage_schedule_id → voyage_schedules.id); voyage_receipts_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id).

### `voyage_schedules` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `vessel_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `pol_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `pod_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `voyage` | `varchar(191)` | NO | `—` | — | — |
| `total_container` | `int(11)` | NO | `—` | — | — |
| `etd` | `timestamp` | NO | `current_timestamp()` | — | — |
| `eta` | `datetime` | NO | `'0000-00-00 00:00:00'` | — | — |
| `departure` | `datetime` | YES | `NULL` | — | — |
| `arrival` | `datetime` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `countries_id` | `int(11)` | YES | `NULL` | — | — |
| `pcode` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; voyage_schedules_create_by_foreign: create_by; voyage_schedules_pod_id_foreign: pod_id; voyage_schedules_pol_id_foreign: pol_id; voyage_schedules_vessel_id_foreign: vessel_id.  
**Foreign key:** voyage_schedules_create_by_foreign (create_by → users.id); voyage_schedules_pod_id_foreign (pod_id → ports.id); voyage_schedules_pol_id_foreign (pol_id → ports.id); voyage_schedules_vessel_id_foreign (vessel_id → vessels.id).

### `vulkanisir_requests` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `vulkanisir_status` | `int(10) unsigned` | YES | `NULL` | — | — |
| `date_request` | `date` | YES | `NULL` | — | — |
| `date_approve` | `date` | YES | `NULL` | — | — |
| `date_needed` | `date` | YES | `NULL` | — | — |
| `total_price` | `int(11)` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `vulkanisir_request_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `wh_stock_ban_luar_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `km_used` | `double(20,2)` | NO | `0.00` | — | — |
| `qty` | `int(11)` | NO | `0` | — | — |
| `price_plan` | `int(11)` | NO | `0` | — | — |
| `price_jasa` | `int(11)` | NO | `0` | — | — |
| `description` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `warehouserents` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(11)` | NO | `—` | — | — |
| `job_order_id` | `int(11)` | NO | `—` | — | — |
| `description` | `text` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `staff_gudang_name` | `varchar(200)` | YES | `NULL` | — | — |
| `start_time` | `time` | YES | `NULL` | — | — |
| `end_time` | `time` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `0` | — | — |
| `is_over_storage_cost` | `int(11)` | NO | `0` | — | — |
| `start_date` | `date` | YES | `NULL` | MUL | — |
| `end_date` | `date` | YES | `NULL` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; warehouserents_end_date_index: end_date; warehouserents_start_date_index: start_date.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `warehouses` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `city_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_type_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | NO | `—` | — | — |
| `name` | `varchar(191)` | NO | `—` | — | — |
| `address` | `varchar(191)` | YES | `NULL` | — | — |
| `latitude` | `varchar(191)` | YES | `NULL` | — | — |
| `longitude` | `varchar(191)` | YES | `NULL` | — | — |
| `capacity` | `int(11)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `capacity_volume` | `double` | YES | `0` | — | — |
| `capacity_tonase` | `double` | YES | `0` | — | — |
| `is_active` | `int(11)` | NO | `1` | — | — |
| `luas_lahan` | `int(11)` | NO | `0` | — | — |
| `luas_bangunan` | `int(11)` | NO | `0` | — | — |
| `luas_gudang` | `int(11)` | NO | `0` | — | — |
| `row` | `int(11)` | NO | `0` | — | — |
| `column` | `int(11)` | NO | `0` | — | — |
| `level` | `int(11)` | NO | `0` | — | — |
| `is_transit` | `tinyint(1)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; warehouses_city_id_foreign: city_id; warehouses_company_id_foreign: company_id; warehouses_warehouse_type_id_foreign: warehouse_type_id.  
**Foreign key:** warehouses_city_id_foreign (city_id → cities.id); warehouses_company_id_foreign (company_id → companies.id); warehouses_warehouse_type_id_foreign (warehouse_type_id → warehouse_types.id).

### `warehouse_maps` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `row` | `int(11)` | NO | `0` | MUL | — |
| `column` | `int(11)` | NO | `0` | MUL | — |
| `level` | `int(11)` | NO | `0` | MUL | — |
| `code` | `varchar(30)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; warehouse_maps_column_index: column; warehouse_maps_level_index: level; warehouse_maps_row_index: row; warehouse_maps_warehouse_id_index: warehouse_id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `warehouse_receipts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `sender_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `receiver_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `collectible_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_staff_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `type_transaction_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `create_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `receive_date` | `timestamp` | NO | `current_timestamp()` | — | — |
| `stripping_done` | `datetime` | YES | `NULL` | — | — |
| `total_qty` | `double` | NO | `0` | — | — |
| `is_export` | `int(10) unsigned` | YES | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `work_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `stripping_type` | `int(10) unsigned` | YES | `1` | — | — |
| `is_overtime` | `int(10) unsigned` | YES | `0` | — | — |
| `nopol` | `varchar(191)` | YES | `NULL` | — | — |
| `driver` | `varchar(191)` | YES | `NULL` | — | — |
| `phone_number` | `varchar(191)` | YES | `NULL` | — | — |
| `city_to` | `varchar(191)` | YES | `NULL` | — | — |
| `city_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `departure_date` | `date` | YES | `NULL` | — | — |
| `company_id` | `int(11)` | NO | `—` | — | — |
| `sender` | `varchar(100)` | YES | `NULL` | — | — |
| `receiver` | `varchar(100)` | YES | `NULL` | — | — |
| `ttd` | `varchar(1000)` | YES | `NULL` | — | — |
| `ttd_driver` | `text` | YES | `NULL` | — | — |
| `package` | `varchar(191)` | YES | `NULL` | — | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `job_order_pengiriman_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `deleted_at` | `timestamp` | YES | `NULL` | MUL | — |
| `receipt_type_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `purchase_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_seen` | `int(11)` | NO | `1` | — | — |
| `user_id` | `varchar(191)` | YES | `NULL` | — | — |
| `jabatan` | `varchar(191)` | YES | `NULL` | — | — |
| `item_condition` | `varchar(191)` | YES | `NULL` | — | — |
| `vulkanisir_request_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `no_invoice_vendor` | `varchar(191)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; warehouse_receipts_city_id_foreign: city_id; warehouse_receipts_collectible_id_foreign: collectible_id; warehouse_receipts_create_by_foreign: create_by; warehouse_receipts_customer_id_foreign: customer_id; warehouse_receipts_deleted_at_index: deleted_at; warehouse_receipts_job_order_pengiriman_id_index: job_order_pengiriman_id; warehouse_receipts_purchase_order_id_index: purchase_order_id; warehouse_receipts_receipt_type_id_index: receipt_type_id; warehouse_receipts_receiver_id_foreign: receiver_id; warehouse_receipts_type_transaction_id_foreign: type_transaction_id; warehouse_receipts_vehicle_type_id_index: vehicle_type_id; warehouse_receipts_warehouse_id_foreign: warehouse_id; warehouse_receipts_warehouse_staff_id_foreign: warehouse_staff_id; warehouse_receipts_work_order_id_foreign: work_order_id.  
**Foreign key:** warehouse_receipts_city_id_foreign (city_id → cities.id); warehouse_receipts_collectible_id_foreign (collectible_id → contacts.id); warehouse_receipts_create_by_foreign (create_by → users.id); warehouse_receipts_customer_id_foreign (customer_id → contacts.id); warehouse_receipts_job_order_pengiriman_id_foreign (job_order_pengiriman_id → job_orders.id); warehouse_receipts_receipt_type_id_foreign (receipt_type_id → receipt_types.id); warehouse_receipts_receiver_id_foreign (receiver_id → contacts.id); warehouse_receipts_type_transaction_id_foreign (type_transaction_id → type_transactions.id); warehouse_receipts_vehicle_type_id_foreign (vehicle_type_id → vehicle_types.id); warehouse_receipts_warehouse_id_foreign (warehouse_id → warehouses.id); warehouse_receipts_warehouse_staff_id_foreign (warehouse_staff_id → users.id); warehouse_receipts_work_order_id_foreign (work_order_id → work_orders.id).

### `warehouse_receipt_billings` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `bigint(20) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_receipt_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `job_order_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `billing_date` | `datetime` | YES | `NULL` | — | — |
| `new_receive_date` | `datetime` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; warehouse_receipt_billings_job_order_id_index: job_order_id; warehouse_receipt_billings_warehouse_receipt_id_index: warehouse_receipt_id.  
**Foreign key:** warehouse_receipt_billings_job_order_id_foreign (job_order_id → job_orders.id); warehouse_receipt_billings_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id).

### `warehouse_receipt_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | — | — |
| `rack_id` | `int(10) unsigned` | NO | `—` | — | — |
| `piece_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `vehicle_type_id` | `int(10) unsigned` | YES | `NULL` | — | — |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `storage_date` | `date` | YES | `NULL` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `weight` | `double` | NO | `0` | — | — |
| `volume` | `double` | NO | `0` | — | — |
| `long` | `double` | NO | `0` | — | — |
| `wide` | `double` | NO | `0` | — | — |
| `high` | `double` | NO | `0` | — | — |
| `item_name` | `varchar(191)` | YES | `NULL` | — | — |
| `barcode` | `varchar(80)` | NO | `—` | — | — |
| `imposition` | `int(11)` | NO | `1` | — | — |
| `nopol` | `varchar(191)` | YES | `NULL` | — | — |
| `driver_name` | `varchar(191)` | YES | `NULL` | — | — |
| `phone_number` | `varchar(191)` | YES | `NULL` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `leftover_warehouse` | `double` | NO | `0` | — | — |
| `leftover_stuffing` | `double` | NO | `0` | — | — |
| `weight_per_kg` | `double` | NO | `0` | — | — |
| `volume_per_meter` | `double` | NO | `0` | — | — |
| `date_out` | `date` | YES | `NULL` | — | — |
| `storage_type` | `varchar(20)` | NO | `'RACK'` | — | — |
| `is_exists` | `int(11)` | NO | `0` | — | — |
| `item_id` | `int(11)` | YES | `NULL` | — | — |
| `is_use_pallet` | `int(11)` | NO | `0` | — | — |
| `pallet_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `pallet_qty` | `int(11)` | NO | `0` | — | — |
| `kemasan` | `varchar(100)` | YES | `NULL` | — | — |
| `piece_id_2` | `int(10) unsigned` | YES | `NULL` | — | — |
| `is_good` | `smallint(6)` | NO | `1` | MUL | — |
| `qty_2` | `double` | NO | `0` | — | — |
| `receipt_quality_status` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `return_qty` | `int(11)` | NO | `0` | — | — |
| `return_receipt_qty` | `int(11)` | NO | `0` | — | — |
| `old_warehouse_stock_detail_id` | `int(10) unsigned` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; warehouse_receipt_details_is_good_index: is_good; warehouse_receipt_details_pallet_id_foreign: pallet_id; warehouse_receipt_details_receipt_quality_status_index: receipt_quality_status.  
**Foreign key:** warehouse_receipt_details_pallet_id_foreign (pallet_id → items.id); warehouse_receipt_details_receipt_quality_status_foreign (receipt_quality_status → receipt_quality_statuses.id).

### `warehouse_stocks` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `warehouse_id` | `int(10) unsigned` | NO | `—` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `transit` | `double` | NO | `0` | — | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |

**Indeks:** PRIMARY (UNIQUE): id; warehouse_stocks_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id.  
**Foreign key:** warehouse_stocks_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id).

### `warehouse_stock_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `rack_id` | `int(10) unsigned` | NO | `—` | — | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `pending_item_qty` | `int(11)` | NO | `0` | — | — |
| `no_surat_jalan` | `varchar(100)` | YES | `NULL` | — | — |
| `customer_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_receipt_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `qty` | `double` | NO | `0` | — | — |
| `onhand_qty` | `double` | NO | `0` | — | — |
| `available_qty` | `double` | NO | `0` | — | — |
| `reff_no` | `varchar(191)` | YES | `NULL` | — | — |
| `tire_batch_no` | `varchar(191)` | YES | `NULL` | — | — |
| `tire_last_km` | `double(10,2)` | NO | `0.00` | — | — |
| `tire_last_km_gps` | `double(10,2)` | NO | `0.00` | — | — |
| `tire_status_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `is_vulkanisir` | `tinyint(1)` | YES | `NULL` | — | — |
| `serial_no` | `varchar(191)` | YES | `NULL` | — | — |
| `total_km_tempuh` | `int(11)` | YES | `NULL` | — | — |
| `vendor_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `stock_initial_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `vulkanisir_count` | `int(11)` | NO | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; warehouse_stock_details_customer_id_foreign: customer_id; warehouse_stock_details_item_id_foreign: item_id; warehouse_stock_details_stock_initial_id_foreign: stock_initial_id; warehouse_stock_details_tire_status_id_foreign: tire_status_id; warehouse_stock_details_vendor_id_foreign: vendor_id; warehouse_stock_details_warehouse_receipt_detail_id_index: warehouse_receipt_detail_id; warehouse_stock_details_warehouse_receipt_id_index: warehouse_receipt_id.  
**Foreign key:** warehouse_stock_details_customer_id_foreign (customer_id → contacts.id); warehouse_stock_details_item_id_foreign (item_id → items.id); warehouse_stock_details_stock_initial_id_foreign (stock_initial_id → stock_initials.id); warehouse_stock_details_tire_status_id_foreign (tire_status_id → tire_statuses.id); warehouse_stock_details_vendor_id_foreign (vendor_id → contacts.id); warehouse_stock_details_warehouse_receipt_id_foreign (warehouse_receipt_id → warehouse_receipts.id).

### `warehouse_types` — 2 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(191)` | NO | `—` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `widgets` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `name` | `varchar(100)` | NO | `—` | MUL | — |
| `query_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `type` | `enum('tabel','grafik','nilai')` | NO | `—` | — | — |
| `width` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; widgets_name_index: name; widgets_query_id_index: query_id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `work_orders` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `customer_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `quotation_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `updated_by` | `int(10) unsigned` | NO | `—` | MUL | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `total_job_order` | `int(11)` | NO | `0` | — | — |
| `status` | `int(11)` | NO | `1` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `quotation_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price_list_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `name` | `varchar(191)` | YES | `NULL` | — | — |
| `date` | `date` | YES | `NULL` | — | — |
| `company_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `qty` | `double(20,2)` | NO | `0.00` | — | — |
| `is_invoice` | `tinyint(1)` | NO | `0` | — | — |
| `no_bl` | `varchar(191)` | YES | `NULL` | — | — |
| `aju_number` | `varchar(191)` | YES | `NULL` | — | — |
| `is_job_packet` | `int(11)` | NO | `0` | MUL | — |
| `invoice_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `additional` | `longtext` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; work_orders_company_id_foreign: company_id; work_orders_customer_id_foreign: customer_id; work_orders_invoice_id_index: invoice_id; work_orders_is_job_packet_index: is_job_packet; work_orders_price_list_id_foreign: price_list_id; work_orders_quotation_detail_id_foreign: quotation_detail_id; work_orders_quotation_id_foreign: quotation_id; work_orders_updated_by_foreign: updated_by.  
**Foreign key:** work_orders_company_id_foreign (company_id → companies.id); work_orders_customer_id_foreign (customer_id → contacts.id); work_orders_price_list_id_foreign (price_list_id → price_lists.id); work_orders_quotation_detail_id_foreign (quotation_detail_id → quotation_details.id); work_orders_quotation_id_foreign (quotation_id → quotations.id); work_orders_updated_by_foreign (updated_by → users.id).

### `work_order_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `quotation_detail_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `price_list_id` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `total_job_order` | `int(11)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `is_done` | `tinyint(1)` | NO | `0` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `qty` | `double` | NO | `0` | — | — |
| `qty_leftover` | `double` | NO | `0` | — | — |
| `customer_price_id` | `int(11)` | NO | `—` | — | — |
| `price_full` | `double` | NO | `—` | — | — |
| `service_name` | `varchar(100)` | NO | `—` | — | — |
| `service_type_name` | `varchar(100)` | NO | `—` | — | — |
| `piece_name` | `varchar(100)` | YES | `NULL` | — | — |
| `container_type_name` | `varchar(100)` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; work_order_details_header_id_foreign: header_id; work_order_details_price_list_id_foreign: price_list_id; work_order_details_quotation_detail_id_foreign: quotation_detail_id.  
**Foreign key:** work_order_details_header_id_foreign (header_id → work_orders.id); work_order_details_price_list_id_foreign (price_list_id → price_lists.id); work_order_details_quotation_detail_id_foreign (quotation_detail_id → quotation_details.id).

### `work_order_drafts` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `create_by` | `int(10) unsigned` | NO | `—` | — | — |
| `company_id` | `int(10) unsigned` | NO | `—` | — | — |
| `customer_id` | `int(10) unsigned` | NO | `—` | — | — |
| `name` | `varchar(191)` | YES | `NULL` | — | — |
| `no_bl` | `varchar(191)` | YES | `NULL` | — | — |
| `aju_number` | `varchar(191)` | YES | `NULL` | — | — |
| `description` | `text` | YES | `NULL` | — | — |
| `date` | `date` | YES | `NULL` | — | — |
| `is_done` | `tinyint(1)` | NO | `0` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id.  
**Foreign key:** Tidak ditemukan constraint FK deklaratif.

### `write_offs` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `company_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `remark` | `varchar(255)` | NO | `—` | — | — |
| `code` | `varchar(191)` | YES | `NULL` | — | — |
| `type` | `int(11)` | NO | `—` | — | — |
| `requested_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `requested_at` | `date` | NO | `—` | — | — |
| `approved_by` | `int(10) unsigned` | YES | `NULL` | MUL | — |
| `approved_at` | `datetime` | YES | `NULL` | — | — |
| `status` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |
| `journal_id` | `int(11)` | YES | `NULL` | — | — |
| `customer_id` | `int(11)` | YES | `NULL` | — | — |
| `is_tire` | `int(11)` | YES | `0` | — | — |
| `termin` | `int(11)` | YES | `0` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; write_offs_approved_by_foreign: approved_by; write_offs_company_id_foreign: company_id; write_offs_requested_by_foreign: requested_by.  
**Foreign key:** write_offs_approved_by_foreign (approved_by → users.id); write_offs_company_id_foreign (company_id → companies.id); write_offs_requested_by_foreign (requested_by → users.id).

### `write_off_details` — 0 baris

| Kolom | Tipe | NULL | Default | Key | Extra |
|---|---|---|---|---|---|
| `id` | `int(10) unsigned` | NO | `—` | PRI | auto_increment |
| `header_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `item_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `rack_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_stock_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `warehouse_receipt_detail_id` | `int(10) unsigned` | NO | `—` | MUL | — |
| `requested_qty` | `int(11)` | NO | `—` | — | — |
| `approved_qty` | `int(11)` | NO | `—` | — | — |
| `requested_price` | `int(11)` | NO | `—` | — | — |
| `approved_price` | `int(11)` | NO | `—` | — | — |
| `created_at` | `timestamp` | YES | `NULL` | — | — |
| `updated_at` | `timestamp` | YES | `NULL` | — | — |

**Indeks:** PRIMARY (UNIQUE): id; write_off_details_header_id_foreign: header_id; write_off_details_item_id_foreign: item_id; write_off_details_rack_id_foreign: rack_id; write_off_details_warehouse_receipt_detail_id_foreign: warehouse_receipt_detail_id; write_off_details_warehouse_stock_detail_id_foreign: warehouse_stock_detail_id.  
**Foreign key:** write_off_details_header_id_foreign (header_id → write_offs.id); write_off_details_item_id_foreign (item_id → items.id); write_off_details_rack_id_foreign (rack_id → racks.id); write_off_details_warehouse_receipt_detail_id_foreign (warehouse_receipt_detail_id → warehouse_receipt_details.id); write_off_details_warehouse_stock_detail_id_foreign (warehouse_stock_detail_id → warehouse_stock_details.id).

## View

- `notif_type_17`
- `notif_type_18`
- `notif_type_19`
- `notif_type_20`
- `notif_type_21`
- `notif_type_22`
- `notif_type_23`
- `notif_type_24`
- `notif_type_25`
- `notif_type_26`
- `notif_type_27`
- `notif_type_28`
- `notif_type_30`
- `notif_type_31`
- `notif_type_32`
- `notif_type_6`
- `notif_type_7`
- `notif_type_8`

## Foreign key deklaratif

- `accounts.company_id` → `companies.id` (`accounts_company_id_foreign`).
- `accounts.parent_id` → `accounts.id` (`accounts_parent_id_foreign`).
- `accounts.type_id` → `account_types.id` (`accounts_type_foreign`).
- `account_defaults.account_cash` → `accounts.id` (`account_defaults_account_cash_foreign`).
- `account_defaults.account_kasbon_id` → `accounts.id` (`account_defaults_account_kasbon_id_foreign`).
- `account_defaults.biaya_klaim` → `accounts.id` (`account_defaults_biaya_klaim_foreign`).
- `account_defaults.bukti_potong` → `accounts.id` (`account_defaults_bukti_potong_foreign`).
- `account_defaults.bukti_potong_hutang` → `accounts.id` (`account_defaults_bukti_potong_hutang_foreign`).
- `account_defaults.cek_giro_keluar` → `accounts.id` (`account_defaults_cek_giro_keluar_foreign`).
- `account_defaults.cek_giro_masuk` → `accounts.id` (`account_defaults_cek_giro_masuk_foreign`).
- `account_defaults.deposit_customer` → `accounts.id` (`account_defaults_deposit_customer_foreign`).
- `account_defaults.deposit_vendor` → `accounts.id` (`account_defaults_deposit_vendor_foreign`).
- `account_defaults.diskon_penjualan` → `accounts.id` (`account_defaults_diskon_penjualan_foreign`).
- `account_defaults.hutang` → `accounts.id` (`account_defaults_hutang_foreign`).
- `account_defaults.hutang_klaim` → `accounts.id` (`account_defaults_hutang_klaim_foreign`).
- `account_defaults.inventory` → `accounts.id` (`account_defaults_inventory_foreign`).
- `account_defaults.laba_bulan_berjalan` → `accounts.id` (`account_defaults_laba_bulan_berjalan_foreign`).
- `account_defaults.laba_ditahan` → `accounts.id` (`account_defaults_laba_ditahan_foreign`).
- `account_defaults.laba_tahun_berjalan` → `accounts.id` (`account_defaults_laba_tahun_berjalan_foreign`).
- `account_defaults.lebih_bayar_hutang` → `accounts.id` (`account_defaults_lebih_bayar_hutang_foreign`).
- `account_defaults.lebih_bayar_piutang` → `accounts.id` (`account_defaults_lebih_bayar_piutang_foreign`).
- `account_defaults.pendapatan_hibah` → `accounts.id` (`account_defaults_pendapatan_hibah_foreign`).
- `account_defaults.pendapatan_klaim` → `accounts.id` (`account_defaults_pendapatan_klaim_foreign`).
- `account_defaults.pendapatan_reimburse` → `accounts.id` (`account_defaults_pendapatan_reimburse_foreign`).
- `account_defaults.penjualan` → `accounts.id` (`account_defaults_penjualan_foreign`).
- `account_defaults.perawatan` → `accounts.id` (`account_defaults_perawatan_foreign`).
- `account_defaults.piutang` → `accounts.id` (`account_defaults_piutang_foreign`).
- `account_defaults.ppn_in` → `accounts.id` (`account_defaults_ppn_in_foreign`).
- `account_defaults.ppn_out` → `accounts.id` (`account_defaults_ppn_out_foreign`).
- `account_defaults.retur_barang` → `accounts.id` (`account_defaults_retur_barang_foreign`).
- `account_defaults.saldo_awal` → `accounts.id` (`account_defaults_saldo_awal_foreign`).
- `account_defaults.selisih_timbang` → `accounts.id` (`account_defaults_selisih_timbang_foreign`).
- `assets.account_accumulation_id` → `accounts.id` (`assets_account_accumulation_id_foreign`).
- `assets.account_asset_id` → `accounts.id` (`assets_account_asset_id_foreign`).
- `assets.account_depreciation_id` → `accounts.id` (`assets_account_depreciation_id_foreign`).
- `assets.asset_group_id` → `asset_groups.id` (`assets_asset_group_id_foreign`).
- `assets.company_id` → `companies.id` (`assets_company_id_foreign`).
- `assets.create_by` → `users.id` (`assets_create_by_foreign`).
- `assets.journal_id` → `journals.id` (`assets_journal_id_foreign`).
- `assets.vehicle_id` → `vehicles.id` (`assets_vehicle_id_foreign`).
- `asset_afkirs.account_loss_id` → `accounts.id` (`asset_afkirs_account_loss_id_foreign`).
- `asset_afkirs.approve_by` → `users.id` (`asset_afkirs_approve_by_foreign`).
- `asset_afkirs.asset_id` → `assets.id` (`asset_afkirs_asset_id_foreign`).
- `asset_afkirs.company_id` → `companies.id` (`asset_afkirs_company_id_foreign`).
- `asset_afkirs.create_by` → `users.id` (`asset_afkirs_create_by_foreign`).
- `asset_afkirs.journal_id` → `journals.id` (`asset_afkirs_journal_id_foreign`).
- `asset_depreciations.approve_by` → `users.id` (`asset_depreciations_approve_by_foreign`).
- `asset_depreciations.header_id` → `assets.id` (`asset_depreciations_header_id_foreign`).
- `asset_depreciations.journal_id` → `journals.id` (`asset_depreciations_journal_id_foreign`).
- `asset_groups.account_accumulation_id` → `accounts.id` (`asset_groups_account_accumulation_id_foreign`).
- `asset_groups.account_asset_id` → `accounts.id` (`asset_groups_account_asset_id_foreign`).
- `asset_groups.account_depreciation_id` → `accounts.id` (`asset_groups_account_depreciation_id_foreign`).
- `asset_purchases.approve_by` → `users.id` (`asset_purchases_approve_by_foreign`).
- `asset_purchases.cash_account_id` → `accounts.id` (`asset_purchases_cash_account_id_foreign`).
- `asset_purchases.company_id` → `companies.id` (`asset_purchases_company_id_foreign`).
- `asset_purchases.create_by` → `users.id` (`asset_purchases_create_by_foreign`).
- `asset_purchases.journal_id` → `journals.id` (`asset_purchases_journal_id_foreign`).
- `asset_purchases.supplier_id` → `contacts.id` (`asset_purchases_supplier_id_foreign`).
- `asset_purchase_details.asset_id` → `assets.id` (`asset_purchase_details_asset_id_foreign`).
- `asset_purchase_details.header_id` → `asset_purchases.id` (`asset_purchase_details_header_id_foreign`).
- `asset_sales.approve_by` → `users.id` (`asset_sales_approve_by_foreign`).
- `asset_sales.cash_account_id` → `accounts.id` (`asset_sales_cash_account_id_foreign`).
- `asset_sales.company_id` → `companies.id` (`asset_sales_company_id_foreign`).
- `asset_sales.costumer_id` → `contacts.id` (`asset_sales_costumer_id_foreign`).
- `asset_sales.create_by` → `users.id` (`asset_sales_create_by_foreign`).
- `asset_sales.journal_id` → `journals.id` (`asset_sales_journal_id_foreign`).
- `asset_sales.sales_account_id` → `accounts.id` (`asset_sales_sales_account_id_foreign`).
- `asset_sales_details.asset_id` → `assets.id` (`asset_sales_details_asset_id_foreign`).
- `asset_sales_details.header_id` → `asset_sales.id` (`asset_sales_details_header_id_foreign`).
- `bills.cancel_by` → `users.id` (`bills_cancel_by_foreign`).
- `bills.company_id` → `companies.id` (`bills_company_id_foreign`).
- `bills.create_by` → `users.id` (`bills_create_by_foreign`).
- `bills.customer_id` → `contacts.id` (`bills_customer_id_foreign`).
- `bills.journal_id` → `journals.id` (`bills_journal_id_foreign`).
- `bill_files.bill_id` → `bills.id` (`bill_files_bill_id_foreign`).
- `budgets.approved_by` → `users.id` (`budgets_approved_by_foreign`).
- `budgets.company_id` → `companies.id` (`budgets_company_id_foreign`).
- `budgets.created_by` → `users.id` (`budgets_created_by_foreign`).
- `budgets.rejected_by` → `users.id` (`budgets_rejected_by_foreign`).
- `budget_details.account_id` → `accounts.id` (`budget_details_account_id_foreign`).
- `budget_details.header_id` → `budgets.id` (`budget_details_header_id_foreign`).
- `budget_files.header_id` → `budgets.id` (`budget_files_header_id_foreign`).
- `budget_files.uploaded_by` → `users.id` (`budget_files_uploaded_by_foreign`).
- `business.business_city_id` → `cities.id` (`business_business_city_id_foreign`).
- `business.contact_id` → `contacts.id` (`business_contact_id_foreign`).
- `cashplan_transactions.approved_by` → `users.id` (`cashplan_transactions_approved_by_foreign`).
- `cashplan_transactions.company_id` → `companies.id` (`cashplan_transactions_company_id_foreign`).
- `cashplan_transactions.created_by` → `users.id` (`cashplan_transactions_created_by_foreign`).
- `cashplan_transaction_details.account_id` → `accounts.id` (`cashplan_transaction_details_account_id_foreign`).
- `cashplan_transaction_details.cashplan_transaction_id` → `cashplan_transactions.id` (`cashplan_transaction_details_cashplan_transaction_id_foreign`).
- `cashplan_transaction_details.contact_id` → `contacts.id` (`cashplan_transaction_details_contact_id_foreign`).
- `cashplan_transaction_details.cost_id` → `cost_types.id` (`cashplan_transaction_details_cost_id_foreign`).
- `cashplan_transaction_details.department_id` → `departments.id` (`cashplan_transaction_details_department_id_foreign`).
- `cashplan_transaction_weeks.cashplan_transaction_detail_id` → `cashplan_transaction_details.id` (`fk_cashplan_detail_week`).
- `cash_advances.account_advance_id` → `accounts.id` (`cash_advances_account_advance_id_foreign`).
- `cash_advances.account_cash_id` → `accounts.id` (`cash_advances_account_cash_id_foreign`).
- `cash_advances.approve_by` → `users.id` (`cash_advances_approve_by_foreign`).
- `cash_advances.cancel_by` → `users.id` (`cash_advances_cancel_by_foreign`).
- `cash_advances.cash_transaction_id` → `cash_transactions.id` (`cash_advances_cash_transaction_id_foreign`).
- `cash_advances.company_id` → `companies.id` (`cash_advances_company_id_foreign`).
- `cash_advances.create_by` → `users.id` (`cash_advances_create_by_foreign`).
- `cash_advances.employee_id` → `contacts.id` (`cash_advances_driver_id_foreign`).
- `cash_advances.journal_id` → `journals.id` (`cash_advances_journal_id_foreign`).
- `cash_advances.paid_by` → `users.id` (`cash_advances_paid_by_foreign`).
- `cash_advances.realisation_id` → `cash_advances.id` (`cash_advances_realisation_id_foreign`).
- `cash_advances.update_by` → `users.id` (`cash_advances_update_by_foreign`).
- `cash_advance_statuses.header_id` → `cash_advances.id` (`cash_advance_statuses_header_id_foreign`).
- `cash_advance_statuses.user_id` → `users.id` (`cash_advance_statuses_user_id_foreign`).
- `cash_advance_transactions.cash_advance_id` → `cash_advances.id` (`cash_advance_transactions_cash_advance_id_foreign`).
- `cash_advance_transactions.cash_transaction_id` → `cash_transactions.id` (`cash_advance_transactions_cash_transaction_id_foreign`).
- `cash_categories.parent_id` → `cash_categories.id` (`cash_categories_parent_id_foreign`).
- `cash_category_details.header_id` → `cash_categories.id` (`cash_category_details_header_id_foreign`).
- `cash_category_details.type_transaction_id` → `type_transactions.id` (`cash_category_details_type_transaction_id_foreign`).
- `cash_counts.approved_by_id` → `users.id` (`cash_counts_approved_by_id_foreign`).
- `cash_counts.company_id` → `companies.id` (`cash_counts_company_id_foreign`).
- `cash_counts.create_by` → `users.id` (`cash_counts_create_by_foreign`).
- `cash_count_details.header_id` → `cash_counts.id` (`cash_count_details_header_id_foreign`).
- `cash_transactions.account_id` → `accounts.id` (`cash_transactions_account_id_foreign`).
- `cash_transactions.company_id` → `companies.id` (`cash_transactions_company_id_foreign`).
- `cash_transactions.created_by` → `users.id` (`cash_transactions_created_by_foreign`).
- `cash_transactions.customer_order_id` → `customer_orders.id` (`cash_transactions_customer_order_id_foreign`).
- `cash_transactions.journal_id` → `journals.id` (`cash_transactions_journal_id_foreign`).
- `cash_transactions.parent_id` → `cash_transactions.id` (`cash_transactions_parent_id_foreign`).
- `cash_transactions.type_transaction_id` → `type_transactions.id` (`cash_transactions_type_transaction_id_foreign`).
- `categories.default_rack_id` → `racks.id` (`categories_default_rack_id_foreign`).
- `categories.parent_id` → `categories.id` (`categories_parent_id_foreign`).
- `cek_giros.account_bank_id` → `accounts.id` (`cek_giros_account_bank_id_foreign`).
- `cek_giros.bank_id` → `banks.id` (`cek_giros_bank_id_foreign`).
- `cek_giros.company_id` → `companies.id` (`cek_giros_company_id_foreign`).
- `cek_giros.journal_id` → `journals.id` (`cek_giros_journal_id_foreign`).
- `cek_giros.kliring_account_id` → `accounts.id` (`cek_giros_kliring_account_id_foreign`).
- `cek_giros.penerbit_id` → `contacts.id` (`cek_giros_penerbit_id_foreign`).
- `cek_giros.penerima_id` → `contacts.id` (`cek_giros_penerima_id_foreign`).
- `cities.province_id` → `provinces.id` (`cities_province_id_foreign`).
- `claims.collectible_id` → `contacts.id` (`claims_collectible_id_foreign`).
- `claims.company_id` → `companies.id` (`claims_company_id_foreign`).
- `claims.customer_id` → `contacts.id` (`claims_customer_id_foreign`).
- `claims.driver_id` → `contacts.id` (`claims_driver_id_foreign`).
- `claims.job_order_id` → `job_orders.id` (`claims_job_order_id_foreign`).
- `claims.journal_id` → `journals.id` (`claims_journal_id_foreign`).
- `claims.payable_id` → `payables.id` (`claims_payable_id_foreign`).
- `claims.receivable_id` → `receivables.id` (`claims_receivable_id_foreign`).
- `claims.sales_order_id` → `sales_orders.id` (`claims_sales_order_id_foreign`).
- `claims.vendor_id` → `contacts.id` (`claims_vendor_id_foreign`).
- `claim_category_details.category_id` → `claim_categories.id` (`claim_category_details_category_id_foreign`).
- `claim_category_details.claim_detail_id` → `claim_details.id` (`claim_category_details_claim_detail_id_foreign`).
- `claim_details.commodity_id` → `commodities.id` (`claim_details_commodity_id_foreign`).
- `claim_details.header_id` → `claims.id` (`claim_details_header_id_foreign`).
- `claim_details.job_order_detail_id` → `job_order_details.id` (`claim_details_job_order_detail_id_foreign`).
- `claim_sales.account_id` → `accounts.id` (`claim_sales_account_id_foreign`).
- `claim_sales.cash_transaction_id` → `cash_transactions.id` (`claim_sales_cash_transaction_id_foreign`).
- `claim_sales.claim_id` → `claims.id` (`claim_sales_claim_id_foreign`).
- `claim_sales.company_id` → `companies.id` (`claim_sales_company_id_foreign`).
- `claim_sales.customer_id` → `contacts.id` (`claim_sales_customer_id_foreign`).
- `claim_sales.journal_id` → `journals.id` (`claim_sales_journal_id_foreign`).
- `claim_sales.receivable_id` → `receivables.id` (`claim_sales_receivable_id_foreign`).
- `claim_sale_details.claim_detail_id` → `claim_details.id` (`claim_sale_details_claim_detail_id_foreign`).
- `claim_sale_details.commodity_id` → `commodities.id` (`claim_sale_details_commodity_id_foreign`).
- `claim_sale_details.header_id` → `claim_sales.id` (`claim_sale_details_header_id_foreign`).
- `closing.company_id` → `companies.id` (`closing_company_id_foreign`).
- `closing.journal_id` → `journals.id` (`closing_journal_id_foreign`).
- `combined_prices.company_id` → `companies.id` (`combined_prices_company_id_foreign`).
- `combined_prices.created_by` → `users.id` (`combined_prices_created_by_foreign`).
- `combined_prices.service_id` → `services.id` (`combined_prices_service_id_foreign`).
- `combined_price_details.header_id` → `combined_prices.id` (`combined_price_details_header_id_foreign`).
- `combined_price_details.service_id` → `services.id` (`combined_price_details_service_id_foreign`).
- `companies.account_kasbon_id` → `accounts.id` (`companies_account_kasbon_id_foreign`).
- `companies.area_id` → `areas.id` (`companies_area_id_foreign`).
- `companies.bank_account_id` → `accounts.id` (`companies_bank_for`).
- `companies.cash_account_id` → `accounts.id` (`companies_cash_for`).
- `companies.city_id` → `cities.id` (`companies_city_id_foreign`).
- `companies.mutation_account_id` → `accounts.id` (`companies_mut_for`).
- `contacts.akun_hutang_belum_tertagih` → `accounts.id` (`contacts_akun_hutang_belum_tertagih_foreign`).
- `contacts.akun_hutang` → `accounts.id` (`contacts_akun_hutang_foreign`).
- `contacts.akun_piutang` → `accounts.id` (`contacts_akun_piutang_foreign`).
- `contacts.akun_um_customer` → `accounts.id` (`contacts_akun_um_customer_foreign`).
- `contacts.akun_um_supplier` → `accounts.id` (`contacts_akun_um_supplier_foreign`).
- `contacts.city_id` → `cities.id` (`contacts_city_id_foreign`).
- `contacts.company_id` → `companies.id` (`contacts_company_id_foreign`).
- `contacts.customer_service_id` → `contacts.id` (`contacts_customer_service_id_foreign`).
- `contacts.parent_id` → `contacts.id` (`contacts_parent_id_foreign`).
- `contacts.rek_bank_id` → `banks.id` (`contacts_rek_bank_id_foreign`).
- `contacts.sales_id` → `contacts.id` (`contacts_sales_id_foreign`).
- `contacts.tax_id` → `taxes.id` (`contacts_tax_id_foreign`).
- `contacts.vendor_type_id` → `vendor_types.id` (`contacts_vendor_type_id_foreign`).
- `contact_documents.contact_id` → `contacts.id` (`contact_documents_contact_id_foreign`).
- `contact_files.contact_id` → `contacts.id` (`contact_files_contact_id_foreign`).
- `contact_locations.contact_id` → `contacts.id` (`contact_locations_contact_id_foreign`).
- `containers.commodity_id` → `commodities.id` (`containers_commodity_id_foreign`).
- `containers.company_id` → `companies.id` (`containers_company_id_foreign`).
- `containers.container_type_id` → `container_types.id` (`containers_container_type_id_foreign`).
- `containers.customer_id` → `contacts.id` (`containers_customer_id_foreign`).
- `containers.manifest_id` → `manifests.id` (`containers_manifest_id_foreign`).
- `containers.vendor_id` → `contacts.id` (`containers_vendor_id_foreign`).
- `containers.vessel_id` → `vessels.id` (`containers_vessel_id_foreign`).
- `containers.voyage_schedule_id` → `voyage_schedules.id` (`containers_voyage_schedule_id_foreign`).
- `container_inspections.checker_id` → `contacts.id` (`container_inspections_checker_id_foreign`).
- `container_inspections.created_by` → `users.id` (`container_inspections_created_by_foreign`).
- `container_inspection_details.container_part_id` → `items.id` (`container_inspection_details_container_part_id_foreign`).
- `container_inspection_details.item_condition_id` → `item_conditions.id` (`container_inspection_details_item_condition_id_foreign`).
- `cost_types.akun_biaya` → `accounts.id` (`cost_types_akun_biaya_foreign`).
- `cost_types.akun_kas_hutang` → `accounts.id` (`cost_types_akun_kas_hutang_foreign`).
- `cost_types.akun_uang_muka` → `accounts.id` (`cost_types_akun_uang_muka_foreign`).
- `cost_types.cash_category_id` → `cash_categories.id` (`cost_types_cash_category_id_foreign`).
- `cost_types.company_id` → `companies.id` (`cost_types_company_id_foreign`).
- `cost_types.cost_route_type_id` → `cost_route_types.id` (`cost_types_cost_route_type_id_foreign`).
- `cost_types.created_by` → `users.id` (`cost_types_created_by_foreign`).
- `cost_types.item_id` → `items.id` (`cost_types_item_id_foreign`).
- `cost_types.parent_id` → `cost_types.id` (`cost_types_parent_id_foreign`).
- `cost_types.vendor_id` → `contacts.id` (`cost_types_vendor_id_foreign`).
- `customer_orders.customer_id` → `contacts.id` (`customer_orders_customer_id_foreign`).
- `customer_orders.customer_order_status_id` → `customer_order_statuses.id` (`customer_orders_customer_order_status_id_foreign`).
- `customer_orders.quotation_id` → `quotations.id` (`customer_orders_quotation_id_foreign`).
- `customer_order_details.header_id` → `customer_orders.id` (`customer_order_details_header_id_foreign`).
- `customer_order_details.item_id` → `items.id` (`customer_order_details_item_id_foreign`).
- `customer_order_details.rack_id` → `racks.id` (`customer_order_details_rack_id_foreign`).
- `customer_order_details.requested_stock_transaction_id` → `stock_transactions.id` (`customer_order_details_requested_stock_transaction_id_foreign`).
- `customer_order_details.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`customer_order_details_warehouse_receipt_detail_id_foreign`).
- `customer_order_files.header_id` → `customer_orders.id` (`customer_order_files_header_id_foreign`).
- `customer_prices.combined_price_id` → `combined_prices.id` (`customer_prices_combined_price_id_foreign`).
- `customer_price_details.header_id` → `customer_prices.id` (`customer_price_details_header_id_foreign`).
- `customer_price_details.service_id` → `services.id` (`customer_price_details_service_id_foreign`).
- `dashboard_details.header_id` → `dashboards.id` (`dashboard_details_header_id_foreign`).
- `dashboard_details.widget_id` → `widgets.id` (`dashboard_details_widget_id_foreign`).
- `debts.akun_selisih` → `accounts.id` (`debts_akun_selisih_foreign`).
- `debts.cancel_by` → `users.id` (`debts_cancel_by_foreign`).
- `debts.company_id` → `companies.id` (`debts_company_id_foreign`).
- `debts.create_by` → `users.id` (`debts_create_by_foreign`).
- `debts.journal_id` → `journals.id` (`debts_journal_id_foreign`).
- `debt_details.create_by` → `users.id` (`debt_details_create_by_foreign`).
- `debt_details.header_id` → `debts.id` (`debt_details_header_id_foreign`).
- `debt_details.nota_credit_id` → `nota_credits.id` (`debt_details_nota_credit_id_foreign`).
- `debt_details.nota_debet_id` → `nota_debets.id` (`debt_details_nota_debet_id_foreign`).
- `debt_details.payable_detail_id` → `payable_details.id` (`debt_details_payable_detail_id_foreign`).
- `debt_details.payable_id` → `payables.id` (`debt_details_payable_id_foreign`).
- `debt_details.type_transaction_id` → `type_transactions.id` (`debt_details_type_transaction_id_foreign`).
- `debt_details.um_supplier_id` → `um_suppliers.id` (`debt_details_um_supplier_id_foreign`).
- `debt_payments.cash_account_id` → `accounts.id` (`debt_payments_cash_account_id_foreign`).
- `debt_payments.cek_giro_id` → `cek_giros.id` (`debt_payments_cek_giro_id_foreign`).
- `debt_payments.create_by` → `users.id` (`debt_payments_create_by_foreign`).
- `debt_payments.header_id` → `debts.id` (`debt_payments_header_id_foreign`).
- `debt_payments.journal_id` → `journals.id` (`debt_payments_journal_id_foreign`).
- `delivery_order_drivers.cancelled_by` → `users.id` (`delivery_order_drivers_cancelled_by_foreign`).
- `delivery_order_drivers.create_by` → `users.id` (`delivery_order_drivers_create_by_foreign`).
- `delivery_order_drivers.depo_awal_id` → `depo_containers.id` (`delivery_order_drivers_depo_awal_id_foreign`).
- `delivery_order_drivers.depo_tujuan_id` → `depo_containers.id` (`delivery_order_drivers_depo_tujuan_id_foreign`).
- `delivery_order_drivers.dock_awal_id` → `docks.id` (`delivery_order_drivers_dock_awal_id_foreign`).
- `delivery_order_drivers.dock_tujuan_id` → `docks.id` (`delivery_order_drivers_dock_tujuan_id_foreign`).
- `delivery_order_drivers.driver_id` → `contacts.id` (`delivery_order_drivers_driver_id_foreign`).
- `delivery_order_drivers.from_address_id` → `contacts.id` (`delivery_order_drivers_from_address_id_foreign`).
- `delivery_order_drivers.from_id` → `contacts.id` (`delivery_order_drivers_from_id_foreign`).
- `delivery_order_drivers.to_address_id` → `contacts.id` (`delivery_order_drivers_to_address_id_foreign`).
- `delivery_order_drivers.to_id` → `contacts.id` (`delivery_order_drivers_to_id_foreign`).
- `delivery_order_drivers.vehicle_id` → `vehicles.id` (`delivery_order_drivers_vehicle_id_foreign`).
- `delivery_order_drivers.vendor_id` → `contacts.id` (`delivery_order_drivers_vendor_id_foreign`).
- `delivery_order_driver_documents.delivery_order_driver_id` → `delivery_order_drivers.id` (`delivery_order_driver_documents_delivery_order_driver_id_foreign`).
- `delivery_order_ongoing_jobs.delivery_order_driver_id` → `delivery_order_drivers.id` (`delivery_order_ongoing_jobs_delivery_order_driver_id_foreign`).
- `delivery_order_ongoing_jobs.job_order_id` → `job_orders.id` (`delivery_order_ongoing_jobs_job_order_id_foreign`).
- `delivery_order_status_logs.created_by` → `users.id` (`delivery_order_status_logs_created_by_foreign`).
- `delivery_order_status_logs.delivery_order_driver_id` → `delivery_order_drivers.id` (`delivery_order_status_logs_delivery_order_driver_id_foreign`).
- `delivery_order_status_logs.job_status_id` → `job_statuses.id` (`delivery_order_status_logs_job_status_id_foreign`).
- `delivery_reject_histories.delivery_order_id` → `delivery_order_drivers.id` (`delivery_reject_histories_delivery_order_id_foreign`).
- `delivery_reject_histories.driver_id` → `contacts.id` (`delivery_reject_histories_driver_id_foreign`).
- `depo_containers.port_id` → `ports.id` (`depo_containers_port_id_foreign`).
- `docks.port_id` → `ports.id` (`docks_port_id_foreign`).
- `driver_messages.driver_id` → `contacts.id` (`driver_messages_driver_id_foreign`).
- `gate_in_containers.company_id` → `companies.id` (`gate_in_containers_company_id_foreign`).
- `gate_in_containers.container_type_id` → `container_types.id` (`gate_in_containers_container_type_id_foreign`).
- `gate_in_containers.created_by` → `users.id` (`gate_in_containers_created_by_foreign`).
- `gate_in_containers.owner_id` → `contacts.id` (`gate_in_containers_owner_id_foreign`).
- `generate_costs.company_id` → `companies.id` (`generate_costs_company_id_foreign`).
- `generate_costs.cost_type_id` → `cost_types.id` (`generate_costs_cost_type_id_foreign`).
- `generate_costs.driver_id` → `contacts.id` (`generate_costs_driver_id_foreign`).
- `generate_costs.helper_id` → `contacts.id` (`generate_costs_helper_id_foreign`).
- `generate_costs.journal_id` → `journals.id` (`generate_costs_journal_id_foreign`).
- `generate_costs.vehicle_id` → `vehicles.id` (`generate_costs_vehicle_id_foreign`).
- `generate_costs.vendor_id` → `contacts.id` (`generate_costs_vendor_id_foreign`).
- `group_roles.group_type_id` → `group_types.id` (`group_roles_group_type_id_foreign`).
- `group_roles.role_id` → `roles.id` (`group_roles_role_id_foreign`).
- `group_types.dashboard_id` → `dashboards.id` (`group_types_dashboard_id_foreign`).
- `industries.create_by` → `users.id` (`industries_create_by_foreign`).
- `inqueries.cancel_inquery_by` → `users.id` (`inqueries_cancel_inquery_by_foreign`).
- `inqueries.cancel_opportunity_by` → `users.id` (`inqueries_cancel_opportunity_by_foreign`).
- `inqueries.company_id` → `companies.id` (`inqueries_company_id_foreign`).
- `inqueries.create_by` → `users.id` (`inqueries_create_by_foreign`).
- `inqueries.customer_id` → `contacts.id` (`inqueries_customer_id_foreign`).
- `inqueries.customer_stage_id` → `customer_stages.id` (`inqueries_customer_stage_id_foreign`).
- `inqueries.inquery_by` → `users.id` (`inqueries_inquery_by_foreign`).
- `inqueries.inquery_customer_id` → `inquery_customers.id` (`inqueries_inquery_customer_id_foreign`).
- `inqueries.lead_id` → `leads.id` (`inqueries_lead_id_foreign`).
- `inqueries.opportunity_id` → `inqueries.id` (`inqueries_opportunity_id_foreign`).
- `inqueries.quotation_id` → `quotations.id` (`inqueries_quotation_id_foreign`).
- `inqueries.sales_inquery_id` → `contacts.id` (`inqueries_sales_inquery_id_foreign`).
- `inqueries.sales_opportunity_id` → `contacts.id` (`inqueries_sales_opportunity_id_foreign`).
- `inquery_customers.customer_id` → `contacts.id` (`inquery_customers_customer_id_foreign`).
- `invoices.account_cash_id` → `accounts.id` (`invoices_account_cash_id_foreign`).
- `invoices.account_receivable_id` → `accounts.id` (`invoices_account_receivable_id_foreign`).
- `invoices.account_selling_id` → `accounts.id` (`invoices_account_selling_id_foreign`).
- `invoices.approve_by` → `users.id` (`invoices_approve_by_foreign`).
- `invoices.company_id` → `companies.id` (`invoices_company_id_foreign`).
- `invoices.create_by` → `users.id` (`invoices_create_by_foreign`).
- `invoices.customer_id` → `contacts.id` (`invoices_customer_id_foreign`).
- `invoices.journal_id` → `journals.id` (`invoices_journal_id_foreign`).
- `invoices.receivable_id` → `receivables.id` (`invoices_receivable_id_foreign`).
- `invoices.tax_id` → `taxes.id` (`invoices_tax_id_foreign`).
- `invoices.type_transaction_id` → `type_transactions.id` (`invoices_type_transaction_id_foreign`).
- `invoice_details.cost_type_id` → `cost_types.id` (`invoice_details_cost_type_id_foreign`).
- `invoice_details.create_by` → `users.id` (`invoice_details_create_by_foreign`).
- `invoice_details.header_id` → `invoices.id` (`invoice_details_header_id_foreign`).
- `invoice_details.job_order_detail_id` → `job_order_details.id` (`invoice_details_job_order_detail_id_foreign`).
- `invoice_details.job_order_id` → `job_orders.id` (`invoice_details_job_order_id_foreign`).
- `invoice_details.manifest_id` → `manifests.id` (`invoice_details_manifest_id_foreign`).
- `invoice_details.service_id` → `services.id` (`invoice_details_service_id_foreign`).
- `invoice_details.work_order_id` → `work_orders.id` (`invoice_details_work_order_id_foreign`).
- `invoice_job_order.invoice_id` → `invoices.id` (`invoice_job_order_invoice_id_foreign`).
- `invoice_job_order.job_order_id` → `job_orders.id` (`invoice_job_order_job_order_id_foreign`).
- `invoice_vendors.company_id` → `companies.id` (`invoice_vendors_company_id_foreign`).
- `invoice_vendors.create_by` → `users.id` (`invoice_vendors_create_by_foreign`).
- `invoice_vendors.journal_id` → `journals.id` (`invoice_vendors_journal_id_foreign`).
- `invoice_vendors.payable_id` → `payables.id` (`invoice_vendors_payable_id_foreign`).
- `invoice_vendors.vendor_id` → `contacts.id` (`invoice_vendors_vendor_id_foreign`).
- `invoice_vendor_details.header_id` → `invoice_vendors.id` (`invoice_vendor_details_header_id_foreign`).
- `invoice_vendor_details.job_order_cost_id` → `job_order_costs.id` (`invoice_vendor_details_job_order_cost_id_foreign`).
- `invoice_vendor_details.manifest_cost_id` → `manifest_costs.id` (`invoice_vendor_details_manifest_cost_id_foreign`).
- `invoice_vendor_details.payable_detail_id` → `payable_details.id` (`invoice_vendor_details_payable_detail_id_foreign`).
- `invoice_vendor_details.vehicle_maintenance_id` → `vehicle_maintenances.id` (`invoice_vendor_details_vehicle_maintenance_id_foreign`).
- `invoice_vendor_taxes.detail_id` → `invoice_vendor_details.id` (`invoice_vendor_taxes_detail_id_foreign`).
- `invoice_vendor_taxes.header_id` → `invoice_vendors.id` (`invoice_vendor_taxes_header_id_foreign`).
- `invoice_vendor_taxes.tax_id` → `taxes.id` (`invoice_vendor_taxes_tax_id_foreign`).
- `items.account_cash_id` → `accounts.id` (`items_account_cash_id_foreign`).
- `items.account_id` → `accounts.id` (`items_account_id_foreign`).
- `items.account_payable_id` → `accounts.id` (`items_account_payable_id_foreign`).
- `items.account_purchase_id` → `accounts.id` (`items_account_purchase_id_foreign`).
- `items.account_purchase_retur_id` → `accounts.id` (`items_account_purchase_retur_id_foreign`).
- `items.account_sale_id` → `accounts.id` (`items_account_sale_id_foreign`).
- `items.account_sale_retur_id` → `accounts.id` (`items_account_sale_retur_id_foreign`).
- `items.category_id` → `categories.id` (`items_category_id_foreign`).
- `items.default_rack_id` → `racks.id` (`items_default_rack_id_foreign`).
- `items.main_supplier_id` → `contacts.id` (`items_main_supplier_id_foreign`).
- `items.piece_id` → `pieces.id` (`items_piece_id_foreign`).
- `items.tire_category_id` → `tire_categories.id` (`items_tire_category_id_foreign`).
- `items.tire_manufacture_id` → `tire_manufacturers.id` (`items_tire_manufacture_id_foreign`).
- `items.tire_size_id` → `tire_sizes.id` (`items_tire_size_id_foreign`).
- `items.tire_type_id` → `tire_types.id` (`items_tire_type_id_foreign`).
- `item_deletions.approve_by` → `users.id` (`item_deletions_approve_by_foreign`).
- `item_deletions.cancel_by` → `users.id` (`item_deletions_cancel_by_foreign`).
- `item_deletions.create_by` → `users.id` (`item_deletions_create_by_foreign`).
- `item_deletions.journal_id` → `journals.id` (`item_deletions_journal_id_foreign`).
- `item_deletions.warehouse_id` → `warehouses.id` (`item_deletions_warehouse_id_foreign`).
- `item_deletion_details.item_id` → `items.id` (`item_deletion_details_item_id_foreign`).
- `item_deletion_details.outbound_stock_transaction_id` → `stock_transactions.id` (`item_deletion_details_outbound_stock_transaction_id_foreign`).
- `item_deletion_details.rack_id` → `racks.id` (`item_deletion_details_rack_id_foreign`).
- `item_deletion_details.requested_stock_transaction_id` → `stock_transactions.id` (`item_deletion_details_requested_stock_transaction_id_foreign`).
- `item_deletion_details.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`item_deletion_details_warehouse_receipt_detail_id_foreign`).
- `item_details.item_id` → `items.id` (`item_details_item_id_foreign`).
- `item_details.po_id` → `purchase_orders.id` (`item_details_po_id_foreign`).
- `item_details.rack_id` → `racks.id` (`item_details_rack_id_foreign`).
- `item_details.warehouse_id` → `warehouses.id` (`item_details_warehouse_id_foreign`).
- `item_migrations.approve_by` → `users.id` (`item_migrations_approve_by_foreign`).
- `item_migrations.cancel_by` → `users.id` (`item_migrations_cancel_by_foreign`).
- `item_migrations.create_by` → `users.id` (`item_migrations_create_by_foreign`).
- `item_migrations.item_migration_type_id` → `item_migration_types.id` (`item_migrations_item_migration_type_id_foreign`).
- `item_migrations.rack_from_id` → `racks.id` (`item_migrations_rack_from_id_foreign`).
- `item_migrations.rack_to_id` → `racks.id` (`item_migrations_rack_to_id_foreign`).
- `item_migrations.warehouse_from_id` → `warehouses.id` (`item_migrations_warehouse_from_id_foreign`).
- `item_migrations.warehouse_receipt_id` → `warehouse_receipts.id` (`item_migrations_warehouse_receipt_id_foreign`).
- `item_migrations.warehouse_to_id` → `warehouses.id` (`item_migrations_warehouse_to_id_foreign`).
- `item_migration_details.destination_warehouse_id` → `warehouses.id` (`item_migration_details_destination_warehouse_id_foreign`).
- `item_migration_details.inbound_stock_transaction_id` → `stock_transactions.id` (`item_migration_details_inbound_stock_transaction_id_foreign`).
- `item_migration_details.outbound_stock_transaction_id` → `stock_transactions.id` (`item_migration_details_outbound_stock_transaction_id_foreign`).
- `item_migration_details.requested_stock_transaction_id` → `stock_transactions.id` (`item_migration_details_requested_stock_transaction_id_foreign`).
- `item_migration_details.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`item_migration_details_warehouse_receipt_detail_id_foreign`).
- `item_migration_receipts.item_migration_id` → `item_migrations.id` (`item_migration_receipts_item_migration_id_foreign`).
- `item_migration_receipts.warehouse_receipt_id` → `warehouse_receipts.id` (`item_migration_receipts_warehouse_receipt_id_foreign`).
- `item_pictures.item_id` → `items.id` (`item_pictures_item_id_foreign`).
- `job_orders.cancel_by` → `users.id` (`job_orders_cancel_by_foreign`).
- `job_orders.collectible_id` → `contacts.id` (`job_orders_collectible_id_foreign`).
- `job_orders.commodity_id` → `commodities.id` (`job_orders_commodity_id_foreign`).
- `job_orders.company_id` → `companies.id` (`job_orders_company_id_foreign`).
- `job_orders.container_type_id` → `container_types.id` (`job_orders_container_type_id_foreign`).
- `job_orders.create_by` → `users.id` (`job_orders_create_by_foreign`).
- `job_orders.customer_id` → `contacts.id` (`job_orders_customer_id_foreign`).
- `job_orders.depo_awal_id` → `depo_containers.id` (`job_orders_depo_awal_id_foreign`).
- `job_orders.depo_tujuan_id` → `depo_containers.id` (`job_orders_depo_tujuan_id_foreign`).
- `job_orders.dock_awal_id` → `docks.id` (`job_orders_dock_awal_id_foreign`).
- `job_orders.dock_tujuan_id` → `docks.id` (`job_orders_dock_tujuan_id_foreign`).
- `job_orders.journal_id` → `journals.id` (`job_orders_journal_id_foreign`).
- `job_orders.journal_temp_id` → `journals.id` (`job_orders_journal_temp_id_foreign`).
- `job_orders.kpi_id` → `kpi_statuses.id` (`job_orders_kpi_id_foreign`).
- `job_orders.moda_id` → `modas.id` (`job_orders_moda_id_foreign`).
- `job_orders.piece_id` → `pieces.id` (`job_orders_piece_id_foreign`).
- `job_orders.quotation_detail_id` → `quotation_details.id` (`job_orders_quotation_detail_id_foreign`).
- `job_orders.quotation_id` → `quotations.id` (`job_orders_quotation_id_foreign`).
- `job_orders.receivable_id` → `receivables.id` (`job_orders_receivable_id_foreign`).
- `job_orders.receiver_id` → `contacts.id` (`job_orders_receiver_id_foreign`).
- `job_orders.route_id` → `routes.id` (`job_orders_route_id_foreign`).
- `job_orders.sender_id` → `contacts.id` (`job_orders_sender_id_foreign`).
- `job_orders.service_id` → `services.id` (`job_orders_service_id_foreign`).
- `job_orders.service_type_id` → `service_types.id` (`job_orders_service_type_id_foreign`).
- `job_orders.transaction_type_id` → `type_transactions.id` (`job_orders_transaction_type_id_foreign`).
- `job_orders.vehicle_type_id` → `vehicle_types.id` (`job_orders_vehicle_type_id_foreign`).
- `job_orders.warehouse_id` → `warehouses.id` (`job_orders_warehouse_id_foreign`).
- `job_orders.warehouse_receipt_id` → `warehouse_receipts.id` (`job_orders_warehouse_receipt_id_foreign`).
- `job_orders.warehouse_staff_id` → `users.id` (`job_orders_warehouse_staff_id_foreign`).
- `job_orders.work_order_detail_id` → `work_order_details.id` (`job_orders_work_order_detail_id_foreign`).
- `job_order_containers.container_id` → `containers.id` (`job_order_containers_container_id_foreign`).
- `job_order_containers.job_order_id` → `job_orders.id` (`job_order_containers_job_order_id_foreign`).
- `job_order_costs.company_id` → `companies.id` (`job_order_costs_company_id_foreign`).
- `job_order_costs.generate_id` → `generate_costs.id` (`job_order_costs_generate_id_foreign`).
- `job_order_costs.manifest_cost_id` → `manifest_costs.id` (`job_order_costs_manifest_cost_id_foreign`).
- `job_order_costs.vendor_job_status_id` → `vendor_job_statuses.id` (`job_order_costs_vendor_job_status_id_foreign`).
- `job_order_details.commodity_id` → `commodities.id` (`job_order_details_commodity_id_foreign`).
- `job_order_details.create_by` → `users.id` (`job_order_details_create_by_foreign`).
- `job_order_details.header_id` → `job_orders.id` (`job_order_details_header_id_foreign`).
- `job_order_details.manifest_id` → `manifests.id` (`job_order_details_manifest_id_foreign`).
- `job_order_details.piece_id` → `pieces.id` (`job_order_details_piece_id_foreign`).
- `job_order_details.price_list_id` → `price_lists.id` (`job_order_details_price_list_id_foreign`).
- `job_order_details.quotation_detail_id` → `quotation_details.id` (`job_order_details_quotation_detail_id_foreign`).
- `job_order_details.quotation_id` → `quotations.id` (`job_order_details_quotation_id_foreign`).
- `job_order_details.receiver_id` → `contacts.id` (`job_order_details_receiver_id_foreign`).
- `job_order_details.requested_stock_transaction_id` → `stock_transactions.id` (`job_order_details_requested_stock_transaction_id_foreign`).
- `job_order_details.sender_id` → `contacts.id` (`job_order_details_sender_id_foreign`).
- `job_order_details.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`job_order_details_warehouse_receipt_detail_id_foreign`).
- `job_order_details.warehouse_receipt_id` → `warehouse_receipts.id` (`job_order_details_warehouse_receipt_id_foreign`).
- `job_order_detail_outputs.job_order_detail_id` → `job_order_details.id` (`job_order_detail_outputs_job_order_detail_id_foreign`).
- `job_order_receivers.create_by` → `users.id` (`job_order_receivers_create_by_foreign`).
- `job_order_receivers.header_id` → `job_orders.id` (`job_order_receivers_header_id_foreign`).
- `job_order_transits.header_id` → `job_orders.id` (`job_order_transits_header_id_foreign`).
- `job_packets.job_order_id` → `job_orders.id` (`job_packets_job_order_id_foreign`).
- `job_packets.work_order_detail_id` → `work_order_details.id` (`job_packets_work_order_detail_id_foreign`).
- `job_status_histories.delivery_id` → `delivery_order_drivers.id` (`job_status_histories_delivery_id_foreign`).
- `job_status_histories.job_status_id` → `job_statuses.id` (`job_status_histories_job_status_id_foreign`).
- `journals.company_id` → `companies.id` (`journals_company_id_foreign`).
- `journals.created_by` → `users.id` (`journals_created_by_foreign`).
- `journals.posting_by` → `users.id` (`journals_posting_by_foreign`).
- `journals.type_transaction_id` → `type_transactions.id` (`journals_type_transaction_id_foreign`).
- `journals.unposting_by` → `users.id` (`journals_unposting_by_foreign`).
- `journal_favorites.created_by` → `users.id` (`journal_favorites_created_by_foreign`).
- `km_tires.company_id` → `companies.id` (`km_tires_company_id_foreign`).
- `kpi_statuses.create_by` → `users.id` (`kpi_statuses_create_by_foreign`).
- `kpi_statuses.service_id` → `services.id` (`kpi_statuses_service_id_foreign`).
- `leads.cancel_by` → `users.id` (`leads_cancel_by_foreign`).
- `leads.city_id` → `cities.id` (`leads_city_id_foreign`).
- `leads.company_id` → `companies.id` (`leads_company_id_foreign`).
- `leads.create_by` → `users.id` (`leads_create_by_foreign`).
- `leads.industry_id` → `industries.id` (`leads_industry_id_foreign`).
- `leads.inquery_id` → `inqueries.id` (`leads_inquery_id_foreign`).
- `leads.lead_source_id` → `lead_sources.id` (`leads_lead_source_id_foreign`).
- `leads.lead_status_id` → `lead_statuses.id` (`leads_lead_status_id_foreign`).
- `leads.quotation_id` → `quotations.id` (`leads_quotation_id_foreign`).
- `leads.sales_id` → `contacts.id` (`leads_sales_id_foreign`).
- `manifests.cancel_id` → `users.id` (`manifests_cancel_id_foreign`).
- `manifests.commodity_id` → `commodities.id` (`manifests_commodity_id_foreign`).
- `manifests.company_id` → `companies.id` (`manifests_company_id_foreign`).
- `manifests.container_id` → `containers.id` (`manifests_container_id_foreign`).
- `manifests.container_type_id` → `container_types.id` (`manifests_container_type_id_foreign`).
- `manifests.create_by` → `users.id` (`manifests_create_by_foreign`).
- `manifests.driver_id` → `contacts.id` (`manifests_driver_id_foreign`).
- `manifests.helper_id` → `contacts.id` (`manifests_helper_id_foreign`).
- `manifests.moda_id` → `modas.id` (`manifests_moda_id_foreign`).
- `manifests.route_id` → `routes.id` (`manifests_route_id_foreign`).
- `manifests.transaction_type_id` → `type_transactions.id` (`manifests_transaction_type_id_foreign`).
- `manifests.vehicle_id` → `vehicles.id` (`manifests_vehicle_id_foreign`).
- `manifests.vehicle_type_id` → `vehicle_types.id` (`manifests_vehicle_type_id_foreign`).
- `manifest_costs.generate_id` → `generate_costs.id` (`manifest_costs_generate_id_foreign`).
- `manifest_costs.job_order_cost_id` → `job_order_costs.id` (`manifest_costs_job_order_cost_id_foreign`).
- `manifest_costs.vendor_job_status_id` → `vendor_job_statuses.id` (`manifest_costs_vendor_job_status_id_foreign`).
- `manifest_details.header_id` → `manifests.id` (`manifest_details_header_id_foreign`).
- `manifest_details.outbound_stock_transaction_id` → `stock_transactions.id` (`manifest_details_outbound_stock_transaction_id_foreign`).
- `manifest_status_logs.created_by` → `users.id` (`manifest_status_logs_created_by_foreign`).
- `manifest_status_logs.job_status_id` → `job_statuses.id` (`manifest_status_logs_job_status_id_foreign`).
- `manifest_status_logs.manifest_id` → `manifests.id` (`manifest_status_logs_manifest_id_foreign`).
- `movement_containers.company_id` → `companies.id` (`movement_containers_company_id_foreign`).
- `movement_containers.created_by` → `users.id` (`movement_containers_created_by_foreign`).
- `movement_containers.operator_id` → `contacts.id` (`movement_containers_operator_id_foreign`).
- `nota_credits.cash_transaction_id` → `cash_transactions.id` (`nota_credits_cash_transaction_id_foreign`).
- `nota_credits.company_id` → `companies.id` (`nota_credits_company_id_foreign`).
- `nota_credits.contact_id` → `contacts.id` (`nota_credits_contact_id_foreign`).
- `nota_credits.journal_id` → `journals.id` (`nota_credits_journal_id_foreign`).
- `nota_credits.receivable_id` → `receivables.id` (`nota_credits_receivable_id_foreign`).
- `nota_debets.cash_transaction_id` → `cash_transactions.id` (`nota_debets_cash_transaction_id_foreign`).
- `nota_debets.company_id` → `companies.id` (`nota_debets_company_id_foreign`).
- `nota_debets.contact_id` → `contacts.id` (`nota_debets_contact_id_foreign`).
- `nota_debets.journal_id` → `journals.id` (`nota_debets_journal_id_foreign`).
- `nota_debets.payable_id` → `payables.id` (`nota_debets_payable_id_foreign`).
- `notifications.notification_type_id` → `notification_types.id` (`notifications_notification_type_id_foreign`).
- `packagings.company_id` → `companies.id` (`packagings_company_id_foreign`).
- `packagings.created_by` → `users.id` (`packagings_created_by_foreign`).
- `packagings.customer_id` → `contacts.id` (`packagings_customer_id_foreign`).
- `packagings.warehouse_id` → `warehouses.id` (`packagings_warehouse_id_foreign`).
- `packaging_new_items.approved_stock_transaction_id` → `stock_transactions.id` (`packaging_new_items_approved_stock_transaction_id_foreign`).
- `packaging_new_items.item_id` → `items.id` (`packaging_new_items_item_id_foreign`).
- `packaging_new_items.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`packaging_new_items_warehouse_receipt_detail_id_foreign`).
- `packaging_old_items.approved_stock_transaction_id` → `stock_transactions.id` (`packaging_old_items_approved_stock_transaction_id_foreign`).
- `packaging_old_items.rack_id` → `racks.id` (`packaging_old_items_rack_id_foreign`).
- `packaging_old_items.requested_stock_transaction_id` → `stock_transactions.id` (`packaging_old_items_requested_stock_transaction_id_foreign`).
- `packaging_old_items.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`packaging_old_items_warehouse_receipt_detail_id_foreign`).
- `pallet_usages.create_by` → `users.id` (`pallet_usages_create_by_foreign`).
- `pallet_usages.customer_id` → `contacts.id` (`pallet_usages_customer_id_foreign`).
- `pallet_usages.shipping_by` → `users.id` (`pallet_usages_shipping_by_foreign`).
- `pallet_usages.warehouse_id` → `warehouses.id` (`pallet_usages_warehouse_id_foreign`).
- `pallet_usage_details.header_id` → `pallet_usages.id` (`pallet_usage_details_header_id_foreign`).
- `pallet_usage_details.item_id` → `items.id` (`pallet_usage_details_item_id_foreign`).
- `payables.account_id` → `accounts.id` (`payables_account_id_foreign`).
- `payables.company_id` → `companies.id` (`payables_company_id_foreign`).
- `payables.contact_id` → `contacts.id` (`payables_contact_id_foreign`).
- `payables.created_by` → `users.id` (`payables_created_by_foreign`).
- `payables.journal_id` → `journals.id` (`payables_journal_id_foreign`).
- `payables.type_transaction_id` → `type_transactions.id` (`payables_type_transaction_id_foreign`).
- `pickings.staff_id` → `contacts.id` (`pickings_staff_id_foreign`).
- `picking_details.approved_stock_transaction_id` → `stock_transactions.id` (`picking_details_approved_stock_transaction_id_foreign`).
- `picking_details.category_id` → `categories.id` (`picking_details_category_id_foreign`).
- `picking_details.requested_stock_transaction_id` → `stock_transactions.id` (`picking_details_requested_stock_transaction_id_foreign`).
- `picking_details.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`picking_details_warehouse_receipt_detail_id_foreign`).
- `ports.country_id` → `countries.id` (`ports_country_id_foreign`).
- `price_lists.combined_price_id` → `combined_prices.id` (`price_lists_combined_price_id_foreign`).
- `price_lists.commodity_id` → `commodities.id` (`price_lists_commodity_id_foreign`).
- `price_lists.company_id` → `companies.id` (`price_lists_company_id_foreign`).
- `price_lists.created_by` → `users.id` (`price_lists_created_by_foreign`).
- `price_lists.depo_awal_id` → `depo_containers.id` (`price_lists_depo_awal_id_foreign`).
- `price_lists.depo_tujuan_id` → `depo_containers.id` (`price_lists_depo_tujuan_id_foreign`).
- `price_lists.dock_awal_id` → `docks.id` (`price_lists_dock_awal_id_foreign`).
- `price_lists.dock_tujuan_id` → `docks.id` (`price_lists_dock_tujuan_id_foreign`).
- `price_lists.moda_id` → `modas.id` (`price_lists_moda_id_foreign`).
- `price_lists.piece_id` → `pieces.id` (`price_lists_piece_id_foreign`).
- `price_lists.route_id` → `routes.id` (`price_lists_route_id_foreign`).
- `price_lists.service_id` → `services.id` (`price_lists_service_id_foreign`).
- `price_lists.vehicle_type_id` → `vehicle_types.id` (`price_lists_vehicle_type_id_foreign`).
- `price_lists.warehouse_id` → `warehouses.id` (`price_lists_warehouse_id_foreign`).
- `price_lists.container_type_id` → `container_types.id` (`price_list_ctype_for`).
- `price_lists.rack_id` → `racks.id` (`price_list_rack_id_for`).
- `price_lists.service_type_id` → `service_types.id` (`price_list_service_type_for`).
- `price_list_costs.cost_type_id` → `cost_types.id` (`price_list_costs_cost_type_id_foreign`).
- `price_list_costs.create_by` → `users.id` (`price_list_costs_create_by_foreign`).
- `price_list_costs.header_id` → `price_lists.id` (`price_list_costs_header_id_foreign`).
- `price_list_costs.journal_id` → `journals.id` (`price_list_costs_journal_id_foreign`).
- `price_list_costs.vendor_id` → `contacts.id` (`price_list_costs_vendor_id_foreign`).
- `price_list_details.header_id` → `price_lists.id` (`price_list_details_header_id_foreign`).
- `price_list_details.service_id` → `services.id` (`price_list_details_service_id_foreign`).
- `provinces.country_id` → `countries.id` (`provinces_country_id_foreign`).
- `purchase_orders.cash_transaction_id` → `cash_transactions.id` (`purchase_orders_cash_transaction_id_foreign`).
- `purchase_orders.company_id` → `companies.id` (`purchase_orders_company_id_foreign`).
- `purchase_orders.journal_id` → `journals.id` (`purchase_orders_journal_id_foreign`).
- `purchase_orders.payable_id` → `payables.id` (`purchase_orders_payable_id_foreign`).
- `purchase_orders.po_by` → `users.id` (`purchase_orders_po_by_foreign`).
- `purchase_orders.status` → `purchase_order_statuses.id` (`purchase_orders_status_foreign`).
- `purchase_orders.supplier_id` → `contacts.id` (`purchase_orders_supplier_id_foreign`).
- `purchase_orders.vehicle_maintenance_id` → `vehicle_maintenances.id` (`purchase_orders_vm_id_foreign`).
- `purchase_orders.warehouse_id` → `warehouses.id` (`purchase_orders_warehouse_id_foreign`).
- `purchase_order_details.header_id` → `purchase_orders.id` (`purchase_order_details_header_id_foreign`).
- `purchase_order_details.item_id` → `items.id` (`purchase_order_details_item_id_foreign`).
- `purchase_order_details.purchase_request_detail_id` → `purchase_request_details.id` (`purchase_order_details_purchase_request_detail_id_foreign`).
- `purchase_order_purchase_request.po_id` → `purchase_orders.id` (`purchase_order_purchase_request_po_id_foreign`).
- `purchase_order_purchase_request.pr_id` → `purchase_requests.id` (`purchase_order_purchase_request_pr_id_foreign`).
- `purchase_order_returns.account_return_id` → `accounts.id` (`purchase_order_returns_account_return_id_foreign`).
- `purchase_order_returns.approve_by` → `users.id` (`purchase_order_returns_approve_by_foreign`).
- `purchase_order_returns.cancel_by` → `users.id` (`purchase_order_returns_cancel_by_foreign`).
- `purchase_order_returns.create_by` → `users.id` (`purchase_order_returns_create_by_foreign`).
- `purchase_order_returns.journal_id` → `journals.id` (`purchase_order_returns_journal_id_foreign`).
- `purchase_order_returns.purchase_order_id` → `purchase_orders.id` (`purchase_order_returns_purchase_order_id_foreign`).
- `purchase_order_returns.warehouse_id` → `warehouses.id` (`purchase_order_returns_warehouse_id_foreign`).
- `purchase_order_return_details.header_id` → `purchase_order_returns.id` (`purchase_order_return_details_header_id_foreign`).
- `purchase_order_return_details.item_id` → `items.id` (`purchase_order_return_details_item_id_foreign`).
- `purchase_order_return_details.po_detail_id` → `purchase_order_details.id` (`purchase_order_return_details_po_detail_id_foreign`).
- `purchase_requests.approve_by` → `users.id` (`purchase_requests_approve_by_foreign`).
- `purchase_requests.company_id` → `companies.id` (`purchase_requests_company_id_foreign`).
- `purchase_requests.create_by` → `users.id` (`purchase_requests_create_by_foreign`).
- `purchase_requests.reject_by` → `users.id` (`purchase_requests_reject_by_foreign`).
- `purchase_requests.vehicle_maintenance_id` → `vehicle_maintenances.id` (`purchase_requests_vm_id_foreign`).
- `purchase_requests.warehouse_id` → `warehouses.id` (`purchase_requests_warehouse_id_foreign`).
- `purchase_request_details.department_id` → `departments.id` (`purchase_request_details_department_id_foreign`).
- `purchase_request_details.header_id` → `purchase_requests.id` (`purchase_request_details_header_id_foreign`).
- `purchase_request_details.item_id` → `items.id` (`purchase_request_details_item_id_foreign`).
- `purchase_request_details.project_id` → `projects.id` (`purchase_request_details_project_id_foreign`).
- `purchase_request_details.vehicle_id` → `vehicles.id` (`purchase_request_details_vehicle_id_foreign`).
- `purchase_request_details.vehicle_maintenance_detail_id` → `vehicle_maintenance_details.id` (`purchase_request_details_vmd_id_foreign`).
- `quotations.approve_by` → `users.id` (`quotations_approve_by_foreign`).
- `quotations.approve_direction_by` → `users.id` (`quotations_approve_direction_by_foreign`).
- `quotations.approve_manager_by` → `users.id` (`quotations_approve_manager_by_foreign`).
- `quotations.cancel_by` → `users.id` (`quotations_cancel_by_foreign`).
- `quotations.cancel_quotation_by` → `users.id` (`quotations_cancel_quotation_by_foreign`).
- `quotations.company_id` → `companies.id` (`quotations_company_id_foreign`).
- `quotations.contract_by` → `users.id` (`quotations_contract_by_foreign`).
- `quotations.created_by` → `users.id` (`quotations_created_by_foreign`).
- `quotations.customer_id` → `contacts.id` (`quotations_customer_id_foreign`).
- `quotations.customer_stage_id` → `customer_stages.id` (`quotations_customer_stage_id_foreign`).
- `quotations.lead_id` → `leads.id` (`quotations_lead_id_foreign`).
- `quotations.parent_id` → `quotations.id` (`quotations_parent_id_foreign`).
- `quotations.piece_id` → `pieces.id` (`quotations_piece_id_foreign`).
- `quotations.sales_id` → `contacts.id` (`quotations_sales_id_foreign`).
- `quotations.stop_contract_by` → `users.id` (`quotations_stop_contract_by_foreign`).
- `quotations.submit_by` → `users.id` (`quotations_submit_by_foreign`).
- `quotation_details.approve_by` → `users.id` (`quotation_details_approve_by_foreign`).
- `quotation_details.combined_price_id` → `combined_prices.id` (`quotation_details_combined_price_id_foreign`).
- `quotation_details.commodity_id` → `commodities.id` (`quotation_details_commodity_id_foreign`).
- `quotation_details.depo_awal_id` → `depo_containers.id` (`quotation_details_depo_awal_id_foreign`).
- `quotation_details.depo_tujuan_id` → `depo_containers.id` (`quotation_details_depo_tujuan_id_foreign`).
- `quotation_details.dock_awal_id` → `docks.id` (`quotation_details_dock_awal_id_foreign`).
- `quotation_details.dock_tujuan_id` → `docks.id` (`quotation_details_dock_tujuan_id_foreign`).
- `quotation_details.header_id` → `quotations.id` (`quotation_details_header_id_foreign`).
- `quotation_details.moda_id` → `modas.id` (`quotation_details_moda_id_foreign`).
- `quotation_details.piece_id` → `pieces.id` (`quotation_details_piece_id_foreign`).
- `quotation_details.price_list_id` → `price_lists.id` (`quotation_details_price_list_id_foreign`).
- `quotation_details.route_id` → `routes.id` (`quotation_details_route_id_foreign`).
- `quotation_details.service_id` → `services.id` (`quotation_details_service_id_foreign`).
- `quotation_details.vehicle_type_id` → `vehicle_types.id` (`quotation_details_vehicle_type_id_foreign`).
- `quotation_details.warehouse_id` → `warehouses.id` (`quotation_details_warehouse_id_foreign`).
- `quotation_details.container_type_id` → `container_types.id` (`quot_det_cont_type_for`).
- `quotation_details.rack_id` → `racks.id` (`quot_det_rack_id_for`).
- `quotation_details.service_type_id` → `service_types.id` (`quot_det_ser_type_for`).
- `quotation_files.header_id` → `quotations.id` (`quotation_files_header_id_foreign`).
- `quotation_items.item_id` → `items.id` (`quotation_items_item_id_foreign`).
- `quotation_items.quotation_id` → `quotations.id` (`quotation_items_quotation_id_foreign`).
- `quotation_items.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`quotation_items_warehouse_receipt_detail_id_foreign`).
- `quotation_price_details.header_id` → `quotation_details.id` (`quotation_price_details_header_id_foreign`).
- `quotation_price_details.service_id` → `services.id` (`quotation_price_details_service_id_foreign`).
- `racks.storage_type_id` → `storage_types.id` (`racks_storage_type_id_foreign`).
- `racks.warehouse_id` → `warehouses.id` (`racks_warehouse_id_foreign`).
- `receipts.account_item_id` → `accounts.id` (`receipts_account_item_id_foreign`).
- `receipts.company_id` → `companies.id` (`receipts_company_id_foreign`).
- `receipts.item_migration_id` → `item_migrations.id` (`receipts_item_migration_id_foreign`).
- `receipts.journal_id` → `journals.id` (`receipts_journal_id_foreign`).
- `receipts.po_id` → `purchase_orders.id` (`receipts_po_id_foreign`).
- `receipts.po_return_id` → `purchase_order_returns.id` (`receipts_po_return_id_foreign`).
- `receipts.sales_return_id` → `sales_order_returns.id` (`receipts_sales_return_id_foreign`).
- `receipts.usage_return_id` → `using_items.id` (`receipts_usage_return_id_foreign`).
- `receipt_details.header_id` → `receipts.id` (`receipt_details_header_id_foreign`).
- `receipt_details.item_id` → `items.id` (`receipt_details_item_id_foreign`).
- `receipt_lists.cash_account_id` → `accounts.id` (`receipt_lists_cash_account_id_foreign`).
- `receipt_lists.header_id` → `receipts.id` (`receipt_lists_header_id_foreign`).
- `receipt_lists.warehouse_id` → `warehouses.id` (`receipt_lists_warehouse_id_foreign`).
- `receipt_list_details.header_id` → `receipt_lists.id` (`receipt_list_details_header_id_foreign`).
- `receipt_list_details.item_id` → `items.id` (`receipt_list_details_item_id_foreign`).
- `receivables.account_id` → `accounts.id` (`receivables_account_id_foreign`).
- `receivables.company_id` → `companies.id` (`receivables_company_id_foreign`).
- `receivables.contact_id` → `contacts.id` (`receivables_contact_id_foreign`).
- `receivables.created_by` → `users.id` (`receivables_created_by_foreign`).
- `receivables.journal_id` → `journals.id` (`receivables_journal_id_foreign`).
- `receivables.type_transaction_id` → `type_transactions.id` (`receivables_type_transaction_id_foreign`).
- `register_bbm.manifests_id` → `manifests.id` (`register_bbm_manifests_id_foreign`).
- `register_bbm.requested_by` → `contacts.id` (`register_bbm_requested_by_foreign`).
- `register_bbm.spbu_id` → `contacts.id` (`register_bbm_spbu_id_foreign`).
- `register_bbm.warehouse_id` → `warehouses.id` (`register_bbm_warehouse_id_foreign`).
- `register_bbm_details.cost_id` → `cost_types.id` (`register_bbm_details_cost_id_foreign`).
- `register_bbm_details.header_id` → `register_bbm.id` (`register_bbm_details_header_id_foreign`).
- `register_bbm_details.item_id` → `items.id` (`register_bbm_details_item_id_foreign`).
- `register_bbm_details.outbound_stock_transaction_id` → `stock_transactions.id` (`register_bbm_details_outbound_stock_transaction_id_foreign`).
- `register_bbm_details.requested_stock_transaction_id` → `stock_transactions.id` (`register_bbm_details_requested_stock_transaction_id_foreign`).
- `register_bbm_details.vehicle_maintenance_detail_id` → `vehicle_maintenance_details.id` (`register_bbm_details_vehicle_maintenance_detail_id_foreign`).
- `returs.account_cash_id` → `accounts.id` (`returs_account_cash_id_foreign`).
- `returs.company_id` → `companies.id` (`returs_company_id_foreign`).
- `returs.create_by` → `users.id` (`returs_create_by_foreign`).
- `returs.journal_id` → `journals.id` (`returs_journal_id_foreign`).
- `returs.supplier_id` → `contacts.id` (`returs_supplier_id_foreign`).
- `returs.warehouse_id` → `warehouses.id` (`returs_warehouse_id_foreign`).
- `retur_details.header_id` → `returs.id` (`retur_details_header_id_foreign`).
- `retur_details.item_id` → `items.id` (`retur_details_item_id_foreign`).
- `retur_receipts.company_id` → `companies.id` (`retur_receipts_company_id_foreign`).
- `retur_receipts.create_by` → `users.id` (`retur_receipts_create_by_foreign`).
- `retur_receipts.header_id` → `returs.id` (`retur_receipts_header_id_foreign`).
- `retur_receipts.warehouse_id` → `warehouses.id` (`retur_receipts_warehouse_id_foreign`).
- `retur_receipt_details.header_id` → `retur_receipts.id` (`retur_receipt_details_header_id_foreign`).
- `retur_receipt_details.item_id` → `items.id` (`retur_receipt_details_item_id_foreign`).
- `retur_receipt_details.retur_detail_id` → `retur_details.id` (`retur_receipt_details_retur_detail_id_foreign`).
- `roles.parent_id` → `roles.id` (`roles_parent_id_foreign`).
- `routes.city_from` → `cities.id` (`routes_city_from_foreign`).
- `routes.city_to_2` → `cities.id` (`routes_city_to_2_foreign`).
- `routes.city_to` → `cities.id` (`routes_city_to_foreign`).
- `routes.company_id` → `companies.id` (`routes_company_id_foreign`).
- `routes.created_by` → `users.id` (`routes_created_by_foreign`).
- `route_costs.commodity_id` → `commodities.id` (`route_costs_commodity_id_foreign`).
- `route_costs.container_type_id` → `container_types.id` (`route_costs_container_type_id_foreign`).
- `route_costs.created_by` → `users.id` (`route_costs_created_by_foreign`).
- `route_costs.route_id` → `routes.id` (`route_costs_route_id_foreign`).
- `sales_orders.job_order_id` → `job_orders.id` (`sales_orders_job_order_id_foreign`).
- `sales_orders.journal_id` → `journals.id` (`sales_orders_journal_id_foreign`).
- `sales_order_details.header_id` → `sales_orders.id` (`sales_order_details_header_id_foreign`).
- `sales_order_details.item_id` → `items.id` (`sales_order_details_item_id_foreign`).
- `sales_order_returns.approve_by` → `users.id` (`sales_order_returns_approve_by_foreign`).
- `sales_order_returns.cancel_by` → `users.id` (`sales_order_returns_cancel_by_foreign`).
- `sales_order_returns.create_by` → `users.id` (`sales_order_returns_create_by_foreign`).
- `sales_order_returns.journal_id` → `journals.id` (`sales_order_returns_journal_id_foreign`).
- `sales_order_returns.sales_order_id` → `sales_orders.id` (`sales_order_returns_sales_order_id_foreign`).
- `sales_order_returns.warehouse_id` → `warehouses.id` (`sales_order_returns_warehouse_id_foreign`).
- `sales_order_return_details.header_id` → `sales_order_returns.id` (`sales_order_return_details_header_id_foreign`).
- `sales_order_return_details.item_id` → `items.id` (`sales_order_return_details_item_id_foreign`).
- `sales_order_return_details.job_order_detail_id` → `job_order_details.id` (`sales_order_return_details_job_order_detail_id_foreign`).
- `sales_order_return_receipts.sales_order_return_detail_id` → `sales_order_return_details.id` (`sales_order_return_receipts_sales_order_return_detail_id_foreign`).
- `sales_order_return_receipts.sales_order_return_id` → `sales_order_returns.id` (`sales_order_return_receipts_sales_order_return_id_foreign`).
- `sales_order_return_receipts.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`sales_order_return_receipts_warehouse_receipt_detail_id_foreign`).
- `sales_order_return_receipts.warehouse_receipt_id` → `warehouse_receipts.id` (`sales_order_return_receipts_warehouse_receipt_id_foreign`).
- `services.account_sale_id` → `accounts.id` (`services_account_sale_id_foreign`).
- `services.kpi_status_id` → `kpi_statuses.id` (`services_kpi_status_id_foreign`).
- `services.service_group_id` → `service_groups.id` (`services_service_group_id_foreign`).
- `services.service_type_id` → `service_types.id` (`service_type_for_id`).
- `stock_adjustments.company_id` → `companies.id` (`stock_adjustments_company_id_foreign`).
- `stock_adjustments.create_by` → `users.id` (`stock_adjustments_create_by_foreign`).
- `stock_adjustments.warehouse_id` → `warehouses.id` (`stock_adjustments_warehouse_id_foreign`).
- `stock_adjustment_details.header_id` → `stock_adjustments.id` (`stock_adjustment_details_header_id_foreign`).
- `stock_adjustment_details.item_id` → `items.id` (`stock_adjustment_details_item_id_foreign`).
- `stock_transactions.customer_id` → `contacts.id` (`stock_transactions_customer_id_foreign`).
- `stock_transactions.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`stock_transactions_warehouse_receipt_detail_id_foreign`).
- `stock_transactions_report.header_id` → `stock_transactions.id` (`stock_transactions_report_header_id_foreign`).
- `stok_opname_warehouses.created_by` → `users.id` (`stok_opname_warehouses_created_by_foreign`).
- `stok_opname_warehouses.customer_id` → `contacts.id` (`stok_opname_warehouses_customer_id_foreign`).
- `stok_opname_warehouses.warehouse_id` → `warehouses.id` (`stok_opname_warehouses_warehouse_id_foreign`).
- `stok_opname_warehouses.warehouse_receipt_id` → `warehouse_receipts.id` (`stok_opname_warehouses_warehouse_receipt_id_foreign`).
- `stok_opname_warehouse_details.header_id` → `stok_opname_warehouses.id` (`stok_opname_warehouse_details_header_id_foreign`).
- `stok_opname_warehouse_details.rack_id` → `racks.id` (`stok_opname_warehouse_details_rack_id_foreign`).
- `stok_opname_warehouse_details.warehouse_receipt_id` → `warehouse_receipts.id` (`stok_opname_warehouse_details_warehouse_receipt_id_foreign`).
- `storings.company_id` → `companies.id` (`storings_company_id_foreign`).
- `storings.vehicle_id` → `vehicles.id` (`storings_vehicle_id_foreign`).
- `taxes.akun_pembelian` → `accounts.id` (`taxes_akun_pembelian_foreign`).
- `taxes.akun_penjualan` → `accounts.id` (`taxes_akun_penjualan_foreign`).
- `tax_invoices.invoice_id` → `invoices.id` (`tax_invoices_invoice_id_foreign`).
- `tire_numberings.company_id` → `companies.id` (`tire_numberings_company_id_foreign`).
- `tire_on_offs.approved_by` → `users.id` (`tire_on_offs_approved_by_foreign`).
- `tire_on_offs.company_id` → `companies.id` (`tire_on_offs_company_id_foreign`).
- `tire_on_offs.rejected_by` → `users.id` (`tire_on_offs_rejected_by_foreign`).
- `tire_on_offs.tire_on_off_category_id` → `tire_on_off_categories.id` (`tire_on_offs_tire_on_off_category_id_foreign`).
- `tire_on_off_details.status_lepas_ban_id` → `tire_statuses.id` (`tire_on_off_details_status_lepas_ban_id_foreign`).
- `um_customers.account_id` → `accounts.id` (`um_customers_account_id_foreign`).
- `um_customers.company_id` → `companies.id` (`um_customers_company_id_foreign`).
- `um_customers.contact_id` → `contacts.id` (`um_customers_contact_id_foreign`).
- `um_customers.created_by` → `users.id` (`um_customers_created_by_foreign`).
- `um_customers.journal_id` → `journals.id` (`um_customers_journal_id_foreign`).
- `um_customers.sales_order_id` → `sales_orders.id` (`um_customers_sales_order_id_foreign`).
- `um_customers.type_transaction_id` → `type_transactions.id` (`um_customers_type_transaction_id_foreign`).
- `um_suppliers.account_id` → `accounts.id` (`um_suppliers_account_id_foreign`).
- `um_suppliers.company_id` → `companies.id` (`um_suppliers_company_id_foreign`).
- `um_suppliers.contact_id` → `contacts.id` (`um_suppliers_contact_id_foreign`).
- `um_suppliers.created_by` → `users.id` (`um_suppliers_created_by_foreign`).
- `um_suppliers.journal_id` → `journals.id` (`um_suppliers_journal_id_foreign`).
- `um_suppliers.type_transaction_id` → `type_transactions.id` (`um_suppliers_type_transaction_id_foreign`).
- `users.dashboard_id` → `dashboards.id` (`users_dashboard_id_foreign`).
- `using_items.company_id` → `companies.id` (`using_items_company_id_foreign`).
- `using_items.requested_by` → `contacts.id` (`using_items_requested_by_foreign`).
- `using_items.vehicle_id` → `vehicles.id` (`using_items_vehicle_id_foreign`).
- `using_items.vehicle_maintenance_id` → `vehicle_maintenances.id` (`using_items_vehicle_maintenance_id_foreign`).
- `using_items.warehouse_id` → `warehouses.id` (`using_items_warehouse_id_foreign`).
- `using_item_details.header_id` → `using_items.id` (`using_item_details_header_id_foreign`).
- `using_item_details.item_id` → `items.id` (`using_item_details_item_id_foreign`).
- `using_item_details.outbound_stock_transaction_id` → `stock_transactions.id` (`using_item_details_outbound_stock_transaction_id_foreign`).
- `using_item_details.requested_stock_transaction_id` → `stock_transactions.id` (`using_item_details_requested_stock_transaction_id_foreign`).
- `using_item_details.vehicle_maintenance_detail_id` → `vehicle_maintenance_details.id` (`using_item_details_vehicle_maintenance_detail_id_foreign`).
- `using_tires.vehicle_id` → `vehicles.id` (`using_tires_vehicle_id_foreign`).
- `using_tires.vehicle_tire_id` → `vehicle_tires.id` (`using_tires_vehicle_tire_id_foreign`).
- `using_tires.wh_stock_ban_dalam_id` → `warehouse_stock_details.id` (`using_tires_wh_stock_ban_dalam_id_foreign`).
- `using_tires.wh_stock_marset_id` → `warehouse_stock_details.id` (`using_tires_wh_stock_marset_id_foreign`).
- `vehicles.company_id` → `companies.id` (`vehicles_company_id_foreign`).
- `vehicles.delivery_id` → `delivery_order_drivers.id` (`vehicles_delivery_id_foreign`).
- `vehicles.gps_provider_id` → `contacts.id` (`vehicles_gps_provider_id_foreign`).
- `vehicles.supplier_id` → `contacts.id` (`vehicles_supplier_id_foreign`).
- `vehicles.vehicle_owner_id` → `vehicle_owners.id` (`vehicles_vehicle_owner_id_foreign`).
- `vehicles.vehicle_variant_id` → `vehicle_variants.id` (`vehicles_vehicle_variant_id_foreign`).
- `vehicle_checklist_detail_bodies.header_id` → `vehicle_checklist_items.id` (`vehicle_checklist_detail_bodies_header_id_foreign`).
- `vehicle_checklist_detail_bodies.vehicle_body_id` → `vehicle_bodies.id` (`vehicle_checklist_detail_bodies_vehicle_body_id_foreign`).
- `vehicle_checklist_detail_items.header_id` → `vehicle_checklist_items.id` (`vehicle_checklist_detail_items_header_id_foreign`).
- `vehicle_checklist_detail_items.vehicle_checklist_id` → `vehicle_checklists.id` (`vehicle_checklist_detail_items_vehicle_checklist_id_foreign`).
- `vehicle_documents.vehicle_id` → `vehicles.id` (`vehicle_documents_vehicle_id_foreign`).
- `vehicle_drivers.driver_id` → `contacts.id` (`vehicle_drivers_driver_id_foreign`).
- `vehicle_drivers.vehicle_id` → `vehicles.id` (`vehicle_drivers_vehicle_id_foreign`).
- `vehicle_insurances.account_id` → `accounts.id` (`vehicle_insurances_account_id_foreign`).
- `vehicle_insurances.insurance_id` → `contacts.id` (`vehicle_insurances_insurance_id_foreign`).
- `vehicle_insurances.journal_id` → `journals.id` (`vehicle_insurances_journal_id_foreign`).
- `vehicle_insurances.vehicle_id` → `vehicles.id` (`vehicle_insurances_vehicle_id_foreign`).
- `vehicle_joint_details.vehicle_joint_id` → `vehicle_joints.id` (`vehicle_joint_details_vehicle_joint_id_foreign`).
- `vehicle_maintenances.company_id` → `companies.id` (`vehicle_maintenances_company_id_foreign`).
- `vehicle_maintenances.mechanic_id` → `contacts.id` (`vehicle_maintenances_mechanic_id_foreign`).
- `vehicle_maintenances.vehicle_id` → `vehicles.id` (`vehicle_maintenances_vehicle_id_foreign`).
- `vehicle_maintenances.vendor_id` → `contacts.id` (`vehicle_maintenances_vendor_id_foreign`).
- `vehicle_maintenances.warehouse_id` → `warehouses.id` (`vehicle_maintenances_wh_id_foreign`).
- `vehicle_maintenance_details.header_id` → `vehicle_maintenances.id` (`vehicle_maintenance_details_header_id_foreign`).
- `vehicle_maintenance_details.item_id` → `items.id` (`vehicle_maintenance_details_item_id_foreign`).
- `vehicle_maintenance_details.rack_id` → `racks.id` (`vehicle_maintenance_details_rack_id_foreign`).
- `vehicle_maintenance_details.vehicle_maintenance_type_id` → `vehicle_maintenance_types.id` (`vehicle_maintenance_details_vehicle_maintenance_type_id_foreign`).
- `vehicle_maintenance_details.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`vehicle_maintenance_details_warehouse_receipt_detail_id_foreign`).
- `vehicle_tires.vehicle_id` → `vehicles.id` (`vehicle_tires_vehicle_id_foreign`).
- `vehicle_tires.wh_stock_ban_luar_id` → `warehouse_stock_details.id` (`vehicle_tires_warehouse_stock_detail_id_foreign`).
- `vehicle_tires.wh_stock_ban_dalam_id` → `warehouse_stock_details.id` (`vehicle_tires_wh_stock_ban_dalam_id_foreign`).
- `vehicle_tires.wh_stock_marset_id` → `warehouse_stock_details.id` (`vehicle_tires_wh_stock_marset_id_foreign`).
- `vehicle_trailer_connections.company_id` → `companies.id` (`vehicle_trailer_connections_company_id_foreign`).
- `vehicle_trailer_connections.trailer_id` → `vehicles.id` (`vehicle_trailer_connections_trailer_id_foreign`).
- `vehicle_trailer_connections.vehicle_id` → `vehicles.id` (`vehicle_trailer_connections_vehicle_id_foreign`).
- `vehicle_variants.bbm_type_id` → `bbm_types.id` (`vehicle_variants_bbm_type_id_foreign`).
- `vehicle_variants.tire_size_id` → `tire_sizes.id` (`vehicle_variants_tire_size_id_foreign`).
- `vehicle_variants.vehicle_joint_id` → `vehicle_joints.id` (`vehicle_variants_vehicle_joint_id_foreign`).
- `vehicle_variants.vehicle_manufacturer_id` → `vehicle_manufacturers.id` (`vehicle_variants_vehicle_manufacturer_id_foreign`).
- `vehicle_variants.vehicle_type_id` → `vehicle_types.id` (`vehicle_variants_vehicle_type_id_foreign`).
- `vendor_prices.cost_type_id` → `cost_types.id` (`vendor_prices_cost_type_id_foreign`).
- `vessels.vendor_id` → `contacts.id` (`vessel_vendor_id_for`).
- `voyage_receipts.voyage_schedule_id` → `voyage_schedules.id` (`voyage_receipts_voyage_schedule_id_foreign`).
- `voyage_receipts.warehouse_receipt_id` → `warehouse_receipts.id` (`voyage_receipts_warehouse_receipt_id_foreign`).
- `voyage_schedules.create_by` → `users.id` (`voyage_schedules_create_by_foreign`).
- `voyage_schedules.pod_id` → `ports.id` (`voyage_schedules_pod_id_foreign`).
- `voyage_schedules.pol_id` → `ports.id` (`voyage_schedules_pol_id_foreign`).
- `voyage_schedules.vessel_id` → `vessels.id` (`voyage_schedules_vessel_id_foreign`).
- `warehouses.city_id` → `cities.id` (`warehouses_city_id_foreign`).
- `warehouses.company_id` → `companies.id` (`warehouses_company_id_foreign`).
- `warehouses.warehouse_type_id` → `warehouse_types.id` (`warehouses_warehouse_type_id_foreign`).
- `warehouse_receipts.city_id` → `cities.id` (`warehouse_receipts_city_id_foreign`).
- `warehouse_receipts.collectible_id` → `contacts.id` (`warehouse_receipts_collectible_id_foreign`).
- `warehouse_receipts.create_by` → `users.id` (`warehouse_receipts_create_by_foreign`).
- `warehouse_receipts.customer_id` → `contacts.id` (`warehouse_receipts_customer_id_foreign`).
- `warehouse_receipts.job_order_pengiriman_id` → `job_orders.id` (`warehouse_receipts_job_order_pengiriman_id_foreign`).
- `warehouse_receipts.receipt_type_id` → `receipt_types.id` (`warehouse_receipts_receipt_type_id_foreign`).
- `warehouse_receipts.receiver_id` → `contacts.id` (`warehouse_receipts_receiver_id_foreign`).
- `warehouse_receipts.type_transaction_id` → `type_transactions.id` (`warehouse_receipts_type_transaction_id_foreign`).
- `warehouse_receipts.vehicle_type_id` → `vehicle_types.id` (`warehouse_receipts_vehicle_type_id_foreign`).
- `warehouse_receipts.warehouse_id` → `warehouses.id` (`warehouse_receipts_warehouse_id_foreign`).
- `warehouse_receipts.warehouse_staff_id` → `users.id` (`warehouse_receipts_warehouse_staff_id_foreign`).
- `warehouse_receipts.work_order_id` → `work_orders.id` (`warehouse_receipts_work_order_id_foreign`).
- `warehouse_receipt_billings.job_order_id` → `job_orders.id` (`warehouse_receipt_billings_job_order_id_foreign`).
- `warehouse_receipt_billings.warehouse_receipt_id` → `warehouse_receipts.id` (`warehouse_receipt_billings_warehouse_receipt_id_foreign`).
- `warehouse_receipt_details.pallet_id` → `items.id` (`warehouse_receipt_details_pallet_id_foreign`).
- `warehouse_receipt_details.receipt_quality_status` → `receipt_quality_statuses.id` (`warehouse_receipt_details_receipt_quality_status_foreign`).
- `warehouse_stocks.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`warehouse_stocks_warehouse_receipt_detail_id_foreign`).
- `warehouse_stock_details.customer_id` → `contacts.id` (`warehouse_stock_details_customer_id_foreign`).
- `warehouse_stock_details.item_id` → `items.id` (`warehouse_stock_details_item_id_foreign`).
- `warehouse_stock_details.stock_initial_id` → `stock_initials.id` (`warehouse_stock_details_stock_initial_id_foreign`).
- `warehouse_stock_details.tire_status_id` → `tire_statuses.id` (`warehouse_stock_details_tire_status_id_foreign`).
- `warehouse_stock_details.vendor_id` → `contacts.id` (`warehouse_stock_details_vendor_id_foreign`).
- `warehouse_stock_details.warehouse_receipt_id` → `warehouse_receipts.id` (`warehouse_stock_details_warehouse_receipt_id_foreign`).
- `work_orders.company_id` → `companies.id` (`work_orders_company_id_foreign`).
- `work_orders.customer_id` → `contacts.id` (`work_orders_customer_id_foreign`).
- `work_orders.price_list_id` → `price_lists.id` (`work_orders_price_list_id_foreign`).
- `work_orders.quotation_detail_id` → `quotation_details.id` (`work_orders_quotation_detail_id_foreign`).
- `work_orders.quotation_id` → `quotations.id` (`work_orders_quotation_id_foreign`).
- `work_orders.updated_by` → `users.id` (`work_orders_updated_by_foreign`).
- `work_order_details.header_id` → `work_orders.id` (`work_order_details_header_id_foreign`).
- `work_order_details.price_list_id` → `price_lists.id` (`work_order_details_price_list_id_foreign`).
- `work_order_details.quotation_detail_id` → `quotation_details.id` (`work_order_details_quotation_detail_id_foreign`).
- `write_offs.approved_by` → `users.id` (`write_offs_approved_by_foreign`).
- `write_offs.company_id` → `companies.id` (`write_offs_company_id_foreign`).
- `write_offs.requested_by` → `users.id` (`write_offs_requested_by_foreign`).
- `write_off_details.header_id` → `write_offs.id` (`write_off_details_header_id_foreign`).
- `write_off_details.item_id` → `items.id` (`write_off_details_item_id_foreign`).
- `write_off_details.rack_id` → `racks.id` (`write_off_details_rack_id_foreign`).
- `write_off_details.warehouse_receipt_detail_id` → `warehouse_receipt_details.id` (`write_off_details_warehouse_receipt_detail_id_foreign`).
- `write_off_details.warehouse_stock_detail_id` → `warehouse_stock_details.id` (`write_off_details_warehouse_stock_detail_id_foreign`).

## Batas interpretasi

- Data pada tabel tidak ditampilkan. Jumlah baris dapat berubah setelah waktu audit.
- Bootstrap Laravel 5.6 gagal pada PHP 8.2 karena kompatibilitas return type `ArrayAccess`; inventaris database diambil langsung melalui PDO dengan query baca-saja setelah konfigurasi dan identitas target diverifikasi. Karena itu, perilaku runtime aplikasi tidak diuji; model/migrasi hanya ditelaah secara statis.
- `NULL` pada metadata default berarti tidak ada default eksplisit terlapor; interpretasi rinci bergantung versi MySQL.
- Relasi aplikasi yang tidak dideklarasikan sebagai FK perlu ditelaah pada model/business rules dan tidak dinyatakan tervalidasi hanya dari nama kolom.
- Target berisi seed/config dan baris sistem, termasuk tabel `migrations`, `roles`, serta tabel master. Data yang ada harus dipertahankan; tidak ada yang dihapus atau diubah.

