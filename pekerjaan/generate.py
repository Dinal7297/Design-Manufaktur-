"""
Generator halaman "Hasil Pekerjaan" untuk website DESIGN MANUFAKTUR.

CARA MENAMBAH HASIL PEKERJAAN BARU (tanpa mengedit file ini / index.html / template.html):
1. Upload foto ke folder assets/pekerjaan/<kategori>/images/
2. Tambahkan satu objek baru di data/pekerjaan.json (contoh sudah ada di file itu)
3. Push ke GitHub -> GitHub Action otomatis menjalankan skrip ini dan
   men-generate ulang seluruh halaman /pekerjaan/ beserta sitemap.xml.

Jangan mengedit file ini kecuali memang ingin mengubah LOGIKA generator.
Untuk mengubah TAMPILAN halaman, cukup edit:
- pekerjaan/template.html       (halaman detail satu pekerjaan)
- pekerjaan/list-template.html  (halaman daftar /pekerjaan/)
"""
import json
import os
import html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = "https://design-manufaktur.vercel.app"

DATA_FILE = os.path.join(ROOT, "data", "pekerjaan.json")
PEKERJAAN_DIR = os.path.join(ROOT, "pekerjaan")
DETAIL_TEMPLATE_FILE = os.path.join(PEKERJAAN_DIR, "template.html")
LIST_TEMPLATE_FILE = os.path.join(PEKERJAAN_DIR, "list-template.html")
SITEMAP_FILE = os.path.join(ROOT, "sitemap.xml")


def esc(x):
    return html.escape(str(x or ""))


def load_items():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        items = json.load(f)
    slugs = [i["slug"] for i in items]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Ada slug yang duplikat di data/pekerjaan.json — setiap pekerjaan harus punya slug unik.")
    return items


def render_card(item):
    slug = item["slug"]
    title = esc(item["title"])
    desc = esc(item.get("description", ""))
    image = esc(item.get("image", ""))
    url = item.get("url", f"/pekerjaan/{slug}/")
    return f"""
    <article class="card">
      <a href="{url}">
        <img src="{image}" alt="{esc(item.get('imageAlt', title))}" loading="lazy">
        <div class="card-body">
          <h2>{title}</h2>
          <p>{desc}</p>
          <span>Lihat pekerjaan &rarr;</span>
        </div>
      </a>
    </article>
    """


def build_list_page(items):
    with open(LIST_TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    if items:
        cards_html = "".join(render_card(i) for i in items)
    else:
        cards_html = '<p class="empty">Belum ada hasil pekerjaan yang ditampilkan.</p>'

    page = template.replace("{{CARDS}}", cards_html)

    with open(os.path.join(PEKERJAAN_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)


def build_detail_pages(items):
    with open(DETAIL_TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    for item in items:
        slug = item["slug"]
        folder = os.path.join(PEKERJAAN_DIR, slug)
        os.makedirs(folder, exist_ok=True)

        url = item.get("url", f"/pekerjaan/{slug}/")
        page = (
            template
            .replace("{{TITLE}}", esc(item["title"]))
            .replace("{{DESCRIPTION}}", esc(item.get("description", "")))
            .replace("{{URL}}", esc(f"{SITE_URL}{url}" if url.startswith("/") else url))
            .replace("{{IMAGE}}", esc(item.get("image", "")))
            .replace("{{IMAGE_ALT}}", esc(item.get("imageAlt", item["title"])))
            .replace("{{CATEGORY}}", esc(item.get("category", "")))
            .replace("{{DATE}}", esc(item.get("date", "")))
            .replace("{{CONTENT}}", item.get("content", ""))
        )

        with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)


def build_sitemap(items):
    today = date.today().isoformat()
    urls = [
        (f"{SITE_URL}/", today),
        (f"{SITE_URL}/pekerjaan/", today),
    ]
    for item in items:
        url = item.get("url", f"/pekerjaan/{item['slug']}/")
        loc = f"{SITE_URL}{url}" if url.startswith("/") else url
        # "date" di data/pekerjaan.json berupa teks tampilan (mis. "26 Agustus 2026"),
        # sitemap butuh format ISO, jadi pakai field opsional "dateISO" kalau ada.
        urls.append((loc, item.get("dateISO", today)))

    entries = "\n".join(
        f"  <url>\n    <loc>{esc(loc)}</loc>\n    <lastmod>{esc(lastmod)}</lastmod>\n  </url>"
        for loc, lastmod in urls
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
    with open(SITEMAP_FILE, "w", encoding="utf-8") as f:
        f.write(sitemap)


def main():
    items = load_items()
    build_list_page(items)
    build_detail_pages(items)
    build_sitemap(items)
    print(f"Berhasil membuat {len(items)} halaman pekerjaan + sitemap.xml.")


if __name__ == "__main__":
    main()
