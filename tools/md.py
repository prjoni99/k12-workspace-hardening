"""Minimal, dependency-free Markdown -> HTML for this repo's dialect.

Deliberately small: it handles exactly the constructs used in these docs
(ATX headings, pipe tables, fenced code, blockquotes, nested lists, task
lists, inline emphasis/code/links, HRs) and nothing else. No dependency
means the site rebuilds on any machine with python3 and nothing installed.
"""
import html
import re


def _inline(t):
    """Inline spans. Code first so its contents are never re-parsed."""
    out, i, n = [], 0, len(t)
    while i < n:
        c = t[i]
        if c == '`':
            m = re.match(r'(`+)(.+?)\1', t[i:], re.S)
            if m:
                out.append('<code>' + html.escape(m.group(2)) + '</code>')
                i += m.end()
                continue
        if c == '[':
            m = re.match(r'\[([^\]]*)\]\(([^)\s]+)\)', t[i:])
            if m:
                label, href = m.group(1), m.group(2)
                ext = href.startswith(('http://', 'https://', 'mailto:'))
                attrs = ' target="_blank" rel="noopener noreferrer"' if ext else ''
                cls = ' class="ext"' if ext else ''
                out.append(f'<a href="{html.escape(href)}"{cls}{attrs}>{_inline(label)}</a>')
                i += m.end()
                continue
        if t.startswith('**', i):
            m = re.match(r'\*\*(.+?)\*\*', t[i:], re.S)
            if m:
                out.append('<strong>' + _inline(m.group(1)) + '</strong>')
                i += m.end()
                continue
        if c == '*':
            m = re.match(r'\*(?!\s)(.+?)(?<!\s)\*', t[i:], re.S)
            if m:
                out.append('<em>' + _inline(m.group(1)) + '</em>')
                i += m.end()
                continue
        out.append(html.escape(c))
        i += 1
    return ''.join(out)


def _cells(row):
    row = row.strip()
    if row.startswith('|'):
        row = row[1:]
    if row.endswith('|'):
        row = row[:-1]
    # split on unescaped pipes not inside inline code
    parts, buf, tick = [], [], False
    for ch in row:
        if ch == '`':
            tick = not tick
        if ch == '|' and not tick:
            parts.append(''.join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append(''.join(buf))
    return [p.strip() for p in parts]


_SEV = (
    (re.compile(r'\bhigh\b', re.I), 'sev-high'),
    (re.compile(r'\b(med|medium)\b', re.I), 'sev-med'),
    (re.compile(r'\blow\b', re.I), 'sev-low'),
)


def _severity(text):
    """Tag residual-risk cells so severity reads at a glance, not just as a word."""
    plain = re.sub(r'[*`\[\]]', '', text).strip()
    if len(plain) > 60:
        return ''
    for rx, cls in _SEV:
        if rx.match(plain):
            return cls
    return ''


def render(md, slug_prefix='', link_map=None):
    """Return (html, [(level, id, text), ...]) for a single document."""
    link_map = link_map or {}
    lines = md.split('\n')
    out, toc = [], []
    i, n = 0, len(lines)
    seen = {}

    def mk_id(text):
        base = re.sub(r'[^a-z0-9]+', '-', re.sub(r'[*`\[\]()#]', '', text).lower()).strip('-')
        base = f'{slug_prefix}-{base}' if slug_prefix else base
        seen[base] = seen.get(base, 0) + 1
        return base if seen[base] == 1 else f'{base}-{seen[base]}'

    def fix_links(chunk):
        def sub(m):
            href = m.group(2)
            if href.startswith(('http', 'mailto:', '#')):
                return m.group(0)
            key = href.split('/')[-1]
            return f'[{m.group(1)}](#{link_map[key]})' if key in link_map else f'[{m.group(1)}]()'
        return re.sub(r'\[([^\]]*)\]\(([^)\s]+)\)', sub, chunk)

    while i < n:
        line = lines[i]

        if line.startswith('```'):
            lang = line[3:].strip()
            i += 1
            body = []
            while i < n and not lines[i].startswith('```'):
                body.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{html.escape(lang)}"' if lang else ''
            label = f'<span class="code-lang">{html.escape(lang)}</span>' if lang else ''
            out.append(f'<div class="code">{label}<pre><code{cls}>'
                       + html.escape('\n'.join(body)) + '</code></pre></div>')
            continue

        if re.match(r'^\s*(---|\*\*\*|___)\s*$', line):
            out.append('<hr>')
            i += 1
            continue

        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            lvl, text = len(m.group(1)), fix_links(m.group(2).strip())
            hid = mk_id(text)
            if lvl <= 3:
                toc.append((lvl, hid, re.sub(r'[*`]', '', m.group(2)).strip()))
            out.append(f'<h{lvl} id="{hid}">{_inline(text)}</h{lvl}>')
            i += 1
            continue

        # pipe table
        if line.strip().startswith('|') and i + 1 < n and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[i + 1]):
            head = _cells(line)
            aligns = []
            for spec in _cells(lines[i + 1]):
                l, r = spec.startswith(':'), spec.endswith(':')
                aligns.append('center' if l and r else 'right' if r else 'left')
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(_cells(lines[i]))
                i += 1
            th = ''.join(
                f'<th style="text-align:{aligns[j] if j < len(aligns) else "left"}">'
                f'{_inline(fix_links(c))}</th>' for j, c in enumerate(head))
            body = []
            for r in rows:
                tds = []
                for j, c in enumerate(r):
                    sev = _severity(c)
                    cls = f' class="{sev}"' if sev else ''
                    al = aligns[j] if j < len(aligns) else 'left'
                    tds.append(f'<td{cls} style="text-align:{al}">{_inline(fix_links(c))}</td>')
                body.append('<tr>' + ''.join(tds) + '</tr>')
            out.append('<div class="table-wrap"><table><thead><tr>' + th
                       + '</tr></thead><tbody>' + ''.join(body) + '</tbody></table></div>')
            continue

        if line.startswith('>'):
            buf = []
            while i < n and (lines[i].startswith('>') or (buf and lines[i].strip() and not lines[i].startswith(('#', '-', '|', '`')))):
                buf.append(re.sub(r'^>\s?', '', lines[i]))
                i += 1
            inner, _ = render('\n'.join(buf), slug_prefix + '-q', link_map)
            joined = '\n'.join(buf)
            kind = 'warn' if ('⚠' in joined or 'Do not' in joined or 'never' in joined.lower()[:80]) else ''
            kind = 'verify' if '[VERIFY' in joined else kind
            out.append(f'<blockquote class="{kind}">{inner}</blockquote>')
            continue

        m = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', line)
        if m:
            ordered = bool(re.match(r'\d+\.', m.group(2)))
            block, base = [], len(m.group(1))
            while i < n:
                mm = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', lines[i])
                if mm and len(mm.group(1)) >= base:
                    block.append((len(mm.group(1)), mm.group(3)))
                    i += 1
                elif lines[i].strip() and lines[i].startswith(' ' * (base + 2)):
                    if block:
                        block[-1] = (block[-1][0], block[-1][1] + ' ' + lines[i].strip())
                    i += 1
                else:
                    break
            tag = 'ol' if ordered else 'ul'
            items, depth = [], base
            for ind, txt in block:
                task = re.match(r'^\[([ xX])\]\s*(.*)$', txt)
                if task:
                    done = task.group(1).lower() == 'x'
                    mark = '<span class="box' + (' done' if done else '') + '"></span>'
                    items.append(f'<li class="task">{mark}<span>{_inline(fix_links(task.group(2)))}</span></li>')
                else:
                    pad = ' style="margin-left:1.1rem"' if ind > depth else ''
                    items.append(f'<li{pad}>{_inline(fix_links(txt))}</li>')
            out.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
            continue

        if not line.strip():
            i += 1
            continue

        para = []
        while i < n and lines[i].strip() and not re.match(r'^(#{1,6}\s|```|>|\s*[-*+]\s|\s*\d+\.\s|\s*\|)', lines[i]) \
                and not re.match(r'^\s*(---|\*\*\*|___)\s*$', lines[i]):
            para.append(lines[i].strip())
            i += 1
        if para:
            # A "definition run" - every line a **Label:** pair - keeps its line
            # breaks, matching how GitHub renders these. Ordinary prose in this
            # repo is hard-wrapped, so those lines must still join with spaces.
            if len(para) > 1 and all(re.match(r'^\*\*[^*]+:\*\*', ln) for ln in para):
                joined = '<br>'.join(_inline(fix_links(ln)) for ln in para)
                out.append('<p class="defrun">' + joined + '</p>')
            else:
                out.append('<p>' + _inline(fix_links(' '.join(para))) + '</p>')

    return '\n'.join(out), toc
