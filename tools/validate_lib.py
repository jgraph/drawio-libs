#!/usr/bin/env python3
"""Validator for drawio-libs mxlibrary files.

Checks (per the conventions used across this repo):
  - file is <mxlibrary [title="..."]>[JSON array]</mxlibrary>
  - every entry has w/h > 0 and a non-empty title (titles are the search
    signal for the drawio-icons corpus; titleless entries are unindexable)
  - every entry is either a data image entry or an uncompressed
    entity-escaped mxGraphModel image entry (the editableCssRules format)
  - every embedded SVG decodes, parses, and contains no script,
    foreignObject, event handlers, or external references
  - optionally writes an HTML contact sheet for visual review

Exit code is non-zero on any structural failure.
"""

import argparse
import base64
import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

FORBIDDEN_RE = re.compile(
    r'<\s*(script|foreignObject)\b|\bon[a-zA-Z]+\s*=|javascript:', re.I)
LIB_RE = re.compile(r'^<mxlibrary(\s[^>]*)?>(.*)</mxlibrary>\s*$', re.S)
IMAGE_RE = re.compile(r'image=data:image/svg\+xml,([A-Za-z0-9+/=]+);')


def external_refs(svg_text):
    refs = []
    for m in re.finditer(r'(?:xlink:)?href\s*=\s*["\']([^"\']+)', svg_text):
        if not m.group(1).startswith(('#', 'data:')):
            refs.append(m.group(1))
    return refs


def check_svg(svg_text, errors, prefix):
    if FORBIDDEN_RE.search(svg_text):
        errors.append(prefix + ': forbidden content (script/foreignObject/'
                      'event handler/javascript:)')
    ext = external_refs(svg_text)
    if ext:
        errors.append(prefix + ': external reference ' + ext[0])
    try:
        ET.fromstring(svg_text)
    except ET.ParseError as e:
        errors.append(prefix + ': SVG parse error: %s' % e)


def validate(path, sheet_items, errors):
    text = Path(path).read_text(encoding='utf-8')
    m = LIB_RE.match(text)
    if m is None:
        errors.append('%s: not a valid <mxlibrary> wrapper' % path)
        return 0
    try:
        entries = json.loads(m.group(2))
    except json.JSONDecodeError as e:
        errors.append('%s: JSON parse error: %s' % (path, e))
        return 0
    if not isinstance(entries, list) or len(entries) == 0:
        errors.append('%s: empty or non-array library' % path)
        return 0

    untitled = 0
    for i, e in enumerate(entries):
        prefix = '%s[%d]' % (Path(path).name, i)
        title = e.get('title', '')
        if not title:
            untitled += 1
        if not (isinstance(e.get('w'), (int, float)) and e['w'] > 0 and
                isinstance(e.get('h'), (int, float)) and e['h'] > 0):
            errors.append(prefix + ': bad w/h')
            continue
        svg_text = None
        if 'data' in e:
            data = e['data']
            if not data.startswith('data:image/svg+xml;base64,'):
                errors.append(prefix + ': unexpected data URI prefix')
                continue
            try:
                svg_text = base64.b64decode(
                    data.split(',', 1)[1]).decode('utf-8')
            except Exception as ex:
                errors.append(prefix + ': base64/utf8 decode: %s' % ex)
                continue
            uri = data
        elif 'xml' in e:
            x = e['xml']
            if '&lt;mxGraphModel&gt;' not in x:
                errors.append(prefix + ': xml entry is not an uncompressed '
                              'entity-escaped mxGraphModel')
                continue
            if 'editableCssRules=.*' not in x:
                errors.append(prefix + ': missing editableCssRules in style')
                continue
            im = IMAGE_RE.search(x)
            if im is None:
                errors.append(prefix + ': no base64 SVG image in style')
                continue
            try:
                svg_text = base64.b64decode(im.group(1)).decode('utf-8')
            except Exception as ex:
                errors.append(prefix + ': base64/utf8 decode: %s' % ex)
                continue
            uri = 'data:image/svg+xml;base64,' + im.group(1)
        else:
            errors.append(prefix + ': neither data nor xml entry')
            continue
        check_svg(svg_text, errors, prefix)
        if sheet_items is not None:
            sheet_items.append((Path(path).name, title, uri))

    if untitled:
        errors.append('%s: %d entries without title (unindexable in icon '
                      'search)' % (path, untitled))
    return len(entries)


def write_sheet(items, out):
    parts = ['<meta charset="utf-8"><style>body{font:12px sans-serif;'
             'background:#fff;margin:16px}h2{margin:24px 0 8px}'
             '.g{display:flex;flex-wrap:wrap;gap:8px}'
             '.c{width:110px;text-align:center;padding:6px;'
             'border:1px solid #eee;border-radius:6px}'
             '.c img{width:48px;height:48px;object-fit:contain}'
             '.t{color:#555;word-wrap:break-word}</style>']
    current = None
    for lib, title, uri in items:
        if lib != current:
            if current is not None:
                parts.append('</div>')
            parts.append('<h2>%s</h2><div class="g">' % html.escape(lib))
            current = lib
        parts.append('<div class="c"><img src="%s" loading="lazy"/>'
                     '<div class="t">%s</div></div>' %
                     (uri, html.escape(title)))
    parts.append('</div>')
    Path(out).write_text(''.join(parts), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('files', nargs='+')
    ap.add_argument('--contact-sheet', default=None)
    args = ap.parse_args()

    errors = []
    sheet_items = [] if args.contact_sheet else None
    total = 0
    for f in args.files:
        n = validate(f, sheet_items, errors)
        print('%s: %d entries' % (f, n))
        total += n

    if args.contact_sheet and sheet_items:
        write_sheet(sheet_items, args.contact_sheet)
        print('contact sheet: %s (%d icons)' %
              (args.contact_sheet, len(sheet_items)))

    if errors:
        print('\n%d PROBLEM(S):' % len(errors))
        for e in errors[:40]:
            print('  ' + e)
        if len(errors) > 40:
            print('  ... %d more' % (len(errors) - 40))
        sys.exit(1)
    print('OK: %d total entries across %d file(s)' % (total, len(args.files)))


if __name__ == '__main__':
    main()
