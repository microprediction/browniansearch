"""Assemble docs/*.html from tools/pages/*.html with one canonical header.

Each page source starts with a line `<!-- title: ... | math -->` (the `| math` flag loads KaTeX).
Run `python3 tools/assemble.py && node docs/header-check.js` after editing any page.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
HEADER = """<header class="site-header">
  <div class="nav-inner">
    <a class="brand" href="./index.html">browniansearch</a>
    <nav>
      <a href="./introduction.html">Introduction</a>
      <span class="menu"><span class="menu-label" tabindex="0" role="button" aria-expanded="false" aria-controls="menu-research">Research</span><span class="drop" id="menu-research">
        <a href="./line-search.html">The rule as a line search</a>
        <a href="./wifi.html">WiFi case study</a>
      </span></span>
      <a href="./papers.html">Papers</a>
      <a href="./bibliography.html">Bibliography</a>
      <a href="https://github.com/microprediction/browniansearch">GitHub</a>
    </nav>
  </div>
  <script>
    (function () {
      var hdr = document.querySelector('.site-header'), menus = [].slice.call(hdr.querySelectorAll('.menu'));
      hdr.classList.add('js-menus');
      function label(m) { return m.querySelector('.menu-label'); }
      function links(m) { return [].slice.call(m.querySelectorAll('.drop a')); }
      function isOpen(m) { return m.classList.contains('open'); }
      function set(m, open, pin) {
        m.classList.toggle('open', open); m.pinned = open && !!pin;
        label(m).setAttribute('aria-expanded', open ? 'true' : 'false');
        if (open) menus.forEach(function (o) { if (o !== m && isOpen(o)) set(o, false); });
      }
      menus.forEach(function (m) {
        var b = label(m);
        b.addEventListener('click', function (e) { e.stopPropagation(); set(m, !(isOpen(m) && m.pinned), true); });
        b.addEventListener('keydown', function (e) {
          if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'ArrowDown') return;
          e.preventDefault();
          if (e.key !== 'ArrowDown' && isOpen(m) && m.pinned) { set(m, false); return; }
          set(m, true, true); links(m)[0].focus();
        });
        m.querySelector('.drop').addEventListener('keydown', function (e) {
          var a = links(m), i = a.indexOf(document.activeElement), n = a.length;
          if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); a[(i + (e.key === 'ArrowDown' ? 1 : n - 1)) % n].focus(); }
          else if (e.key === 'Home' || e.key === 'End') { e.preventDefault(); a[e.key === 'Home' ? 0 : n - 1].focus(); }
        });
        m.addEventListener('mouseenter', function () { if (!isOpen(m)) set(m, true, false); });
        m.addEventListener('mouseleave', function () { if (isOpen(m) && !m.pinned) set(m, false); });
        m.addEventListener('focusout', function (e) { if (isOpen(m) && !m.contains(e.relatedTarget)) set(m, false); });
      });
      document.addEventListener('click', function (e) { menus.forEach(function (m) { if (isOpen(m) && !m.contains(e.target)) set(m, false); }); });
      document.addEventListener('keydown', function (e) {
        if (e.key !== 'Escape') return;
        menus.forEach(function (m) { if (!isOpen(m)) return; var inside = m.contains(document.activeElement); set(m, false); if (inside) label(m).focus(); });
      });
    })();
  </script>
</header>"""
KATEX = """  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css" crossorigin="anonymous">
  <style>.katex { white-space: nowrap; } .katex-display { overflow-x: auto; overflow-y: hidden; padding: 2px 0; }</style>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js" crossorigin="anonymous"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js" crossorigin="anonymous"
    onload="renderMathInElement(document.body, {delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]});"></script>
"""
FOOTER = """  <footer>
    <a href="https://github.com/microprediction/browniansearch">Source</a> &middot;
    Maintained by <a href="https://github.com/microprediction">Peter Cotton</a>.
  </footer>"""

for src in sorted((ROOT / "tools" / "pages").glob("*.html")):
    text = src.read_text()
    m = re.match(r"<!-- title: (.*?)( \| math)?( \| extra: (.*?))? -->\n", text)
    title, math, extra = m.group(1), bool(m.group(2)), m.group(4) or ""
    body = text[m.end():]
    head = ('<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8" />\n'
            '  <meta name="viewport" content="width=device-width,initial-scale=1" />\n'
            f"  <title>{title}</title>\n  <link rel=\"stylesheet\" href=\"./style.css\" />\n")
    for css in [e for e in extra.split(",") if e.strip().endswith(".css")]:
        head += f'  <link rel="stylesheet" href="./{css.strip()}" />\n'
    if math:
        head += KATEX
    head += "</head>\n<body>\n"
    out = head + HEADER + "\n\n" + body.rstrip() + "\n\n" + FOOTER + "\n</body>\n</html>\n"
    (ROOT / "docs" / src.name).write_text(out)
    print("wrote docs/" + src.name)
