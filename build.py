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


# ---------- tiny markdown (headings, lists, paragraphs, bold, italic, links, raw HTML comments) ----------
def inline(s: str, root: str) -> str:
    s = html.escape(s, quote=False)
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


def markdown(src: str, root: str) -> tuple[str, str]:
    """Return (title from the first # heading, body html)."""
    title, out, para, items = "", [], [], []

    def flush():
        nonlocal para, items
        if para:
            out.append("<p>" + inline(" ".join(para), root) + "</p>")
            para = []
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i, root)}</li>" for i in items) + "</ul>")
            items = []

    for line in src.splitlines():
        line = line.rstrip()
        if not line:
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
        elif line.startswith("- "):
            if para:
                flush()
            items.append(line[2:].strip())
        else:
            if items:
                flush()
            para.append(line.strip())
    flush()
    return title, "\n".join(out)


# ---------- pages ----------
def render(page_path: str, title: str, description: str, body: str, root: str, current: str = "") -> None:
    base = (ROOT / "templates" / "base.html").read_text(encoding="utf-8")
    nav = []
    for key, label, href in (("support", "Support", "support/"), ("privacy", "Privacy", "privacy/"), ("terms", "Terms", "terms/")):
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
    urls = ["", "support/", "privacy/", "terms/"]
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
