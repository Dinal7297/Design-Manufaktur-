# Cara Menambah Hasil Pekerjaan Baru

Website ini sekarang bekerja seperti Blogspot: untuk menambah 1 hasil pekerjaan baru,
kamu **hanya perlu 2 langkah** lewat GitHub web (tanpa install apa pun, tanpa edit
`index.html`, `template.html`, atau `generate.py`).

## Langkah 1 — Upload foto
Buka folder `assets/pekerjaan/<kategori>/images/` sesuai kategori pekerjaannya
(`pagar`, `pintu`, `teralis`, `railing`, `kanopi`, `tenda`), lalu klik **Add file →
Upload files** di GitHub, upload foto hasil pekerjaan.

Contoh path setelah upload:
```
assets/pekerjaan/kanopi/images/kanopi-cibinong-002.jpg
```

## Langkah 2 — Tambah data di `data/pekerjaan.json`
Buka file `data/pekerjaan.json`, klik ikon pensil (edit) di GitHub, lalu tambahkan
satu objek baru **di dalam tanda kurung siku `[ ]`** (pisahkan dengan koma dari
objek sebelumnya). Contoh:

```json
{
  "slug": "kanopi-cibinong-002",
  "title": "Pembuatan Kanopi Baja Ringan di Cibinong",
  "description": "Hasil pekerjaan pembuatan kanopi baja ringan oleh DESIGN MANUFAKTUR di Cibinong.",
  "date": "1 September 2026",
  "dateISO": "2026-09-01",
  "category": "Kanopi",
  "image": "/assets/pekerjaan/kanopi/images/kanopi-cibinong-002.jpg",
  "imageAlt": "Kanopi baja ringan hasil pekerjaan DESIGN MANUFAKTUR di Cibinong",
  "url": "/pekerjaan/kanopi-cibinong-002/",
  "content": "<p>Deskripsi lengkap pekerjaan di sini, boleh beberapa paragraf.</p>"
}
```

Catatan penting:
- `slug` harus unik (tidak boleh sama dengan pekerjaan lain), pakai huruf kecil dan tanda `-`.
- `image` harus persis sama dengan path foto yang diupload di Langkah 1.
- `dateISO` format `YYYY-MM-DD` (dipakai untuk sitemap, bukan yang tampil ke pengunjung).

Klik **Commit changes**.

## Setelah itu otomatis
Begitu perubahan di-commit ke branch `main`, GitHub Action
(`.github/workflows/generate-pekerjaan.yml`) otomatis:
1. Menjalankan `pekerjaan/generate.py`
2. Membuat halaman baru di `/pekerjaan/<slug>/`
3. Memperbarui daftar di `/pekerjaan/`
4. Memperbarui `sitemap.xml`
5. Meng-commit hasilnya kembali ke repo

Vercel lalu otomatis deploy ulang seperti biasa. Kamu tidak perlu menjalankan
apa pun secara manual, dan tidak perlu menyentuh kode HTML/Python lain.

## Kalau ingin ganti tampilan
- Tampilan **halaman daftar** `/pekerjaan/` → edit `pekerjaan/list-template.html`
- Tampilan **halaman detail** satu pekerjaan → edit `pekerjaan/template.html`
- `pekerjaan/generate.py` cukup sekali disiapkan, tidak perlu diedit lagi kecuali
  ingin mengubah logika (misalnya menambah field data baru).
