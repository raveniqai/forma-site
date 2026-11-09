#!/usr/bin/env python3
"""Render the Forma 360 site into docs/.  Python standard library only, deterministic.

    python3 build.py

Inputs : site.config.json (every owner-specific value), templates/*.html, content/*.md, assets/*, static/*
Output : docs/   (committed, because GitHub Pages serves it)
"""
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "docs"
CFG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))
TOKEN = re.compile(r"\{\{\s*([a-z_]+)\s*\}\}")


def fill(text: str, extra: dict | None = None, where: str = "") -> str:
    """Replace {{key}} with config values. An unknown key is a build error, never silent."""
    values = {k: v for k, v in CFG.items() if isinstance(v, (str, int))}
    values.update(extra or {})

    def sub(m):
        key = m.group(1)
        if key not in values:
            sys.exit(f"build error: unknown placeholder {{{{{key}}}}} in {where}")
        return str(values[key])

    return TOKEN.sub(sub, text)


# ---------- tiny markdown (headings, lists, steps, tips, tables, images, code, paragraphs, bold, italic, links) ----------
def inline(s: str, root: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)

    def link(m):
        text, url = m.group(1), m.group(2)
        if url.startswith("/"):
            url = root + url.lstrip("/")
        return f'<a href="{url}">{text}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def markdown(src: str, root: str, img_root: str = "") -> tuple[str, str]:
    """Return (title from the first # heading, body html)."""
    title, out = "", []
    para, items, ordered, quote, table, code = [], [], [], [], [], None

    def flush():
        nonlocal para, items, ordered, quote, table
        if para:
            out.append("<p>" + inline(" ".join(para), root) + "</p>")
            para = []
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i, root)}</li>" for i in items) + "</ul>")
            items = []
        if ordered:
            out.append('<ol class="steps">' + "".join(f"<li>{inline(i, root)}</li>" for i in ordered) + "</ol>")
            ordered = []
        if quote:
            text = " ".join(quote)
            kind = "note"
            m = re.match(r"\*\*(Tip|Note|Careful|Example|Limit)[:.]?\*\*", text)
            if m:
                kind = m.group(1).lower()
            out.append(f'<aside class="callout {kind}"><p>{inline(text, root)}</p></aside>')
            quote = []
        if table:
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in table if not re.match(r"^\s*\|?\s*:?-{2,}", r)]
            head, body = rows[0], rows[1:]
            out.append('<div class="table"><table><thead><tr>' + "".join(f"<th>{inline(c, root)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{inline(c, root)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>")
            table = []

    for line in src.splitlines():
        line = line.rstrip()
        if code is not None:
            if line.startswith("```"):
                out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
                code = None
            else:
                code.append(line)
            continue
        if line.startswith("```"):
            flush()
            code = []
        elif not line:
            flush()
        elif line.startswith("<!--"):
            flush()
            out.append(line)  # TODO-OWNER comments stay visible in the page source on purpose
        elif line.startswith("# "):
            flush()
            title = line[2:].strip()
        elif line.startswith("## "):
            flush()
            h = line[3:].strip()
            out.append(f'<h2 id="{slug(h)}">{inline(h, root)}</h2>')
        elif line.startswith("### "):
            flush()
            h = line[4:].strip()
            out.append(f'<h3 id="{slug(h)}">{inline(h, root)}</h3>')
        elif re.match(r"^!\[[^\]]*\]\([^)]+\)$", line):
            flush()
            m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line)
            alt, src_ = m.group(1), m.group(2)
            out.append(f'<figure><img src="{img_root}{src_}" alt="{html.escape(alt, quote=True)}" loading="lazy"><figcaption>{inline(alt, root)}</figcaption></figure>')
        elif line.startswith("|"):
            if para or items or ordered or quote:
                flush()
            table.append(line)
        elif line.startswith("> "):
            if para or items or ordered or table:
                flush()
            quote.append(line[2:].strip())
        elif re.match(r"^\d+\. ", line):
            if para or items or quote or table:
                flush()
            ordered.append(re.sub(r"^\d+\. ", "", line).strip())
        elif line.startswith("- "):
            if para or ordered or quote or table:
                flush()
            items.append(line[2:].strip())
        else:
            if items or ordered or quote or table:
                flush()
            para.append(line.strip())
    flush()
    return title, "\n".join(out)


# ---------- pages ----------
def render(page_path: str, title: str, description: str, body: str, root: str, current: str = "", wide: bool = False) -> None:
    base = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    nav = []
    for key, label, href in (("guide", "Guide", "guide/"), ("support", "Support", "support/"), ("privacy", "Privacy", "privacy/"), ("terms", "Terms", "terms/")):
        cur = ' aria-current="page"' if key == current else ""
        nav.append(f'<a href="{root}{href}"{cur}>{label}</a>')
    page = fill(
        base,
        {
            "title": html.escape(title),
            "description": html.escape(description, quote=True),
            "content": body,
            "root": root,
            "nav": "\n".join(nav),
            "canonical": CFG["site_url"].rstrip("/") + "/" + ("" if page_path == "index.html" else page_path.replace("index.html", "")),
            "year_note": "",
            "main_class": "wrap wide" if wide else "wrap",
        },
        where="base.html",
    )
    dest = OUT / page_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Internal owner notes live in the SOURCE (templates/content) and README, never in the published HTML.
    page = re.sub(r"[ \t]*<!--(?:(?!-->).)*?TODO-OWNER(?:(?!-->).)*?-->[ \t]*\n?", "", page, flags=re.S)
    dest.write_text(page, encoding="utf-8")


def fragment(name: str, root: str) -> str:
    extra = {"root": root}
    if CFG.get("app_store_url"):
        extra["store"] = f'<a class="button" href="{html.escape(CFG["app_store_url"])}">View on the App Store</a>'
    else:
        extra["store"] = '<p class="soon"><strong>Coming to the App Store</strong></p>'
    return fill((ROOT / "templates" / name).read_text(encoding="utf-8"), extra, where=name)


def legal(md_name: str, root: str) -> tuple[str, str]:
    raw = fill((ROOT / "content" / md_name).read_text(encoding="utf-8"), where=md_name)
    visible = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    left = re.findall(r"\[[^\]]+\](?!\()", visible)
    if left:
        sys.exit(f"build error: unreplaced [bracket] placeholder(s) in {md_name}: {left}")
    title, body = markdown(raw, root)
    return title, body


# ---------- guide ----------
GUIDE = ROOT / "content" / "guide"
SEARCH_JS = r"""(function () {
  var menu = document.querySelector('.guide-menu');
  if (menu && window.matchMedia('(max-width: 52rem)').matches) menu.removeAttribute('open');
  var box = document.getElementById('guide-search'), out = document.getElementById('guide-results');
  if (!box || !out) return;
  var index = null;
  function load(cb) {
    if (index) return cb();
    fetch(box.dataset.index).then(function (r) { return r.json(); }).then(function (j) { index = j; cb(); });
  }
  function run() {
    var q = box.value.trim().toLowerCase();
    out.textContent = '';
    if (q.length < 2) return;
    var words = q.split(/\s+/);
    var hits = index.map(function (p) {
      var score = 0;
      words.forEach(function (w) {
        if (p.title.toLowerCase().indexOf(w) >= 0) score += 5;
        if (p.summary.toLowerCase().indexOf(w) >= 0) score += 2;
        if (p.text.indexOf(w) >= 0) score += 1; else score -= 100;
      });
      return { p: p, score: score };
    }).filter(function (h) { return h.score > 0; }).sort(function (a, b) { return b.score - a.score; }).slice(0, 12);
    if (!hits.length) { var li = document.createElement('li'); li.textContent = 'Nothing found. Try another word.'; out.appendChild(li); return; }
    hits.forEach(function (h) {
      var li = document.createElement('li'), a = document.createElement('a'), sm = document.createElement('span');
      a.href = box.dataset.root + h.p.url; a.textContent = h.p.title; sm.textContent = ' ' + h.p.summary; sm.className = 'small';
      li.appendChild(a); li.appendChild(sm); out.appendChild(li);
    });
  }
  box.addEventListener('input', function () { load(run); });
})();
"""


def front_matter(raw: str, where: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        sys.exit(f"build error: {where} has no front matter")
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    for need in ("title", "summary", "order"):
        if need not in meta:
            sys.exit(f"build error: {where} front matter lacks '{need}'")
    return meta, m.group(2)


def build_guide() -> list[str]:
    """Render content/guide into docs/guide. Returns the URLs for the sitemap."""
    if not GUIDE.exists():
        return []
    sections = json.loads((GUIDE / "sections.json").read_text(encoding="utf-8"))
    pages = []
    for sec in sections:
        d = GUIDE / sec["id"]
        if not d.exists():
            continue
        items = []
        for f in sorted(d.glob("*.md")):
            raw = fill(f.read_text(encoding="utf-8"), where=str(f.relative_to(ROOT)))
            meta, body = front_matter(raw, str(f.relative_to(ROOT)))
            left = re.findall(r"\[VERIFY[^\]]*\]|TODO|\[bracket\]", body)
            if left:
                sys.exit(f"build error: unresolved marker(s) {left} in {f.relative_to(ROOT)}")
            items.append((int(meta["order"]), f.stem, meta, body))
        items.sort(key=lambda x: (x[0], x[1]))
        for _, stem, meta, body in items:
            pages.append({"section": sec, "slug": stem, "meta": meta, "body": body, "url": f"guide/{sec['id']}/{stem}/"})
    if not pages:
        return []
    app = CFG["app_name"]
    root_for = lambda depth: "../" * depth

    def sidebar(current_url: str, root: str) -> str:
        out = ['<details class="guide-menu" open><summary>Browse the guide</summary>', '<div class="guide-nav" role="navigation" aria-label="Guide">', f'<a class="guide-home" href="{root}guide/">All topics</a>']
        for sec in sections:
            mine = [p for p in pages if p["section"]["id"] == sec["id"]]
            if not mine:
                continue
            open_ = " open" if any(p["url"] == current_url for p in mine) else ""
            out.append(f'<details{open_}><summary>{html.escape(sec["title"])}</summary><ul>')
            for p in mine:
                cur = ' aria-current="page"' if p["url"] == current_url else ""
                out.append(f'<li><a href="{root}{p["url"]}"{cur}>{html.escape(p["meta"]["title"])}</a></li>')
            out.append("</ul></details>")
        out.append("</div></details>")
        return "\n".join(out)

    index_rows = []
    for i, p in enumerate(pages):
        root = root_for(4)
        title, body_html = markdown(p["body"], root, img_root=root + "guide/img/")
        h2s = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)
        toc = ""
        if len(h2s) > 2:
            toc = '<div class="on-page" role="navigation" aria-label="On this page"><strong>On this page</strong><ul>' + "".join(f'<li><a href="#{a}">{b}</a></li>' for a, b in h2s) + "</ul></div>"
        prev_ = pages[i - 1] if i > 0 else None
        next_ = pages[i + 1] if i + 1 < len(pages) else None
        pager = '<div class="pager" role="navigation" aria-label="Previous and next">'
        pager += f'<a rel="prev" href="{root}{prev_["url"]}">&larr; {html.escape(prev_["meta"]["title"])}</a>' if prev_ else "<span></span>"
        pager += f'<a rel="next" href="{root}{next_["url"]}">{html.escape(next_["meta"]["title"])} &rarr;</a>' if next_ else "<span></span>"
        pager += "</div>"
        article = (f'<article class="prose guide-page"><p class="crumb"><a href="{root}guide/">Guide</a> &rsaquo; {html.escape(p["section"]["title"])}</p>'
                   f'<h1>{html.escape(p["meta"]["title"])}</h1><p class="lead-in">{inline(p["meta"]["summary"], root)}</p>{toc}{body_html}'
                   f'<p class="small">Something unclear or missing? Write to <span class="email">{CFG["support_email"]}</span> and say which page.</p>{pager}</article>')
        page_html = f'<div class="guide-layout">{sidebar(p["url"], root)}{article}</div><script src="{root}guide/search.js" defer></script>'
        render(p["url"] + "index.html", f"{p['meta']['title']} - {app} guide", p["meta"]["summary"], page_html, root, "guide", wide=True)
        plain = re.sub(r"<[^>]+>", " ", body_html)
        plain = re.sub(r"\s+", " ", html.unescape(plain)).lower()
        index_rows.append({"title": p["meta"]["title"], "summary": p["meta"]["summary"], "url": p["url"], "text": plain})

    # the guide home
    root = "../"
    cards = []
    for sec in sections:
        mine = [p for p in pages if p["section"]["id"] == sec["id"]]
        if not mine:
            continue
        lis = "".join(f'<li><a href="{root}{p["url"]}">{html.escape(p["meta"]["title"])}</a><span class="small"> {inline(p["meta"]["summary"], root)}</span></li>' for p in mine)
        cards.append(f'<section class="card guide-card" id="{sec["id"]}"><h2>{html.escape(sec["title"])}</h2><p class="small">{html.escape(sec.get("blurb", ""))}</p><ul class="guide-list">{lis}</ul></section>')
    home = (f'<article class="prose"><h1>{html.escape(app)} guide</h1><p class="lead-in">What every part of {html.escape(CFG["short_name"])} does and how to use it, in plain words, '
            f'with worked examples. Every example uses invented people and numbers.</p>'
            f'<label class="search"><span>Search the guide</span><input id="guide-search" type="search" placeholder="for example: forecast, card, backup" autocomplete="off" data-index="{root}guide/search.json" data-root="{root}"></label>'
            f'<ul id="guide-results" class="results" aria-live="polite"></ul>{"".join(cards)}</article><script src="{root}guide/search.js" defer></script>')
    render("guide/index.html", f"{app} guide: how to use every feature", f"A detailed guide to {app}: what each feature does, how to use it, and worked examples.", home, root, "guide", wide=True)
    (OUT / "guide").mkdir(exist_ok=True)
    (OUT / "guide" / "search.json").write_text(json.dumps(index_rows, ensure_ascii=False), encoding="utf-8")
    (OUT / "guide" / "search.js").write_text(SEARCH_JS, encoding="utf-8")
    if (GUIDE / "img").exists():
        shutil.copytree(GUIDE / "img", OUT / "guide" / "img")
    return ["guide/"] + [p["url"] for p in pages]


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    app = CFG["app_name"]

    render("index.html", f"{app}: training coach and diet coach for iPhone",
           f"{app} is a training coach and a diet coach that run on your iPhone, keep your data private, and work alone or together.",
           fragment("index.html", "./"), "./")

    for key, md in (("privacy", "privacy.md"), ("terms", "terms.md")):
        title, body = legal(md, "../")
        head = f'<h1>{html.escape(title)}</h1>'
        # the "Last updated" paragraph is the first <p>; give it a class for styling
        body = body.replace("<p>Last updated:", '<p class="updated">Last updated:', 1)
        desc = {"privacy": f"How {app} handles your data: no accounts, no analytics, data on your phone.",
                "terms": f"The terms for using {app}, including the subscription and the medical disclaimer."}[key]
        render(f"{key}/index.html", f"{title} - {app}", desc, f'<article class="prose">\n{head}\n{body}\n</article>', "../", key)

    render("support/index.html", f"Support - {app}", f"How to contact support for {app}, and answers to common questions.",
           fragment("support.html", "../"), "../", "support")

    guide_urls = build_guide()
    render("404.html", f"Page not found - {app}", "This page does not exist.", fragment("404.html", "/"), "/")

    # static files
    shutil.copy(ROOT / "static" / "style.css", OUT / "style.css")
    for name in ("favicon.ico", "favicon-32.png", "apple-touch-icon.png", "icon-192.png"):
        shutil.copy(ROOT / "assets" / name, OUT / name)
    host = CFG["site_url"].split("://", 1)[1].rstrip("/")
    (OUT / "CNAME").write_text(host + "\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    base = CFG["site_url"].rstrip("/")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    urls = ["", "support/", "privacy/", "terms/"] + guide_urls
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{base}/{u}</loc><lastmod>{CFG['effective_date']}</lastmod></url>\n" for u in urls)
        + "</urlset>\n", encoding="utf-8")

    # loud warnings
    n = 0
    for f in sorted(OUT.rglob("*.html")):
        n += len(re.findall(r"TODO-OWNER", f.read_text(encoding="utf-8")))
    if not CFG.get("support_email_confirmed"):
        print("WARNING: support email is not confirmed (site.config.json: support_email_confirmed=false).")
    if not CFG.get("app_store_url"):
        print("NOTE: no App Store URL yet; the home page says 'Coming to the App Store' and shows no link.")
    print(f"built {sum(1 for _ in OUT.rglob('*') if _.is_file())} files into {OUT.name}/ ; {n} TODO-OWNER marker(s) left in the published HTML (should be 0)")


if __name__ == "__main__":
    main()
