import json, os, html

with open("data/pekerjaan.json", "r", encoding="utf-8") as f:
    items = json.load(f)

def esc(x):
    return html.escape(str(x or ""))

os.makedirs("pekerjaan", exist_ok=True)

# =========================
# HALAMAN DAFTAR PEKERJAAN
# =========================
cards = []

for item in items:
    slug = item["slug"]
    title = esc(item["title"])
    desc = esc(item.get("description", ""))
    image = esc(item.get("image", ""))
    url = item.get("url", f"/pekerjaan/{slug}/")

    cards.append(f"""
    <article class="card">
      <a href="{url}">
        <img src="{image}" alt="{esc(item.get('imageAlt', title))}" loading="lazy">
        <div class="card-body">
          <h2>{title}</h2>
          <p>{desc}</p>
          <span>Lihat pekerjaan →</span>
        </div>
      </a>
    </article>
    """)

index_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hasil Pekerjaan DESIGN MANUFAKTUR</title>
<meta name="description" content="Kumpulan hasil pekerjaan DESIGN MANUFAKTUR meliputi pagar besi, kanopi, tenda, teralis, pintu, railing dan fabrikasi besi di Cibinong Bogor.">
<link rel="canonical" href="/pekerjaan/">
<style>
body{{font-family:Arial,sans-serif;margin:0;background:#f5f5f5;color:#222}}
header{{background:#111;color:white;padding:35px 20px}}
main{{max-width:1100px;margin:auto;padding:30px 20px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:22px}}
.card{{background:white;border-radius:14px;overflow:hidden;box-shadow:0 3px 15px #0001}}
.card img{{width:100%;height:220px;object-fit:cover}}
.card-body{{padding:18px}}
.card h2{{margin-top:0}}
.card p{{line-height:1.6;color:#555}}
.card a{{color:inherit;text-decoration:none}}
.card span{{font-weight:bold}}
</style>
</head>
<body>
<header>
<h1>Hasil Pekerjaan DESIGN MANUFAKTUR</h1>
<p>Dokumentasi pekerjaan fabrikasi besi dan konstruksi custom di Cibinong, Bogor.</p>
</header>
<main>
<div class="grid">
{''.join(cards)}
</div>
</main>
</body>
</html>
"""

with open("pekerjaan/index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

# =========================
# HALAMAN DETAIL SETIAP JOB
# =========================
for item in items:
    slug = item["slug"]
    folder = f"pekerjaan/{slug}"
    os.makedirs(folder, exist_ok=True)

    title = esc(item["title"])
    description = esc(item.get("description", ""))
    content = item.get("content", "")
    image = esc(item.get("image", ""))
    image_alt = esc(item.get("imageAlt", title))
    date = esc(item.get("date", ""))
    category = esc(item.get("category", ""))

    page = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>{title} | DESIGN MANUFAKTUR</title>

<meta name="description" content="{description}">
<meta name="robots" content="index,follow">

<link rel="canonical" href="/pekerjaan/{slug}/">

<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{image}">
<meta property="og:type" content="article">

<style>
body{{font-family:Arial,sans-serif;margin:0;background:#f5f5f5;color:#222}}
header{{background:#111;color:#fff;padding:30px 20px}}
main{{max-width:900px;margin:auto;background:#fff;padding:25px 20px}}
.hero{{width:100%;max-height:600px;object-fit:cover;border-radius:12px}}
.meta{{color:#777;margin:15px 0}}
.content{{font-size:18px;line-height:1.8}}
.back{{display:inline-block;margin-top:30px;font-weight:bold}}
</style>
</head>

<body>

<header>
<h1>{title}</h1>
<p>DESIGN MANUFAKTUR — Bengkel Las & Fabrikasi Besi Cibinong Bogor</p>
</header>

<main>

<img class="hero" src="{image}" alt="{image_alt}">

<div class="meta">
Kategori: {category} · {date}
</div>

<h2>{title}</h2>

<p>{description}</p>

<div class="content">
{content}
</div>

<a class="back" href="/pekerjaan/">← Kembali ke semua pekerjaan</a>

</main>

</body>
</html>
"""

    with open(f"{folder}/index.html", "w", encoding="utf-8") as f:
        f.write(page)

print(f"Berhasil membuat {len(items)} halaman pekerjaan.")
