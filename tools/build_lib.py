#!/usr/bin/env python3
"""Generic SVG -> draw.io mxlibrary converter for drawio-libs.

Modes:
  mono-fill    strip fill colours, inject a .shape_fill CSS class so the
               editor's editableCssRules support makes the icon recolorable
  mono-stroke  strip stroke colours, inject a .shape_outline CSS class
  color        keep the artwork as-is (sanitized), plain data-URI entries

The mono entry format matches libs/hero-icons.xml / libs/material-symbols.xml:
an uncompressed, entity-escaped mxGraphModel wrapping a single image cell with
style shape=image;editableCssRules=.*;...;image=data:image/svg+xml,<base64>.
Graph.canonicalizeSvgCssRules only rewrites fill/stroke/stop-color found in
<style> rules, so all inline colour attributes must be stripped here.

Every entry gets a title: titles are the only search signal the
drawio-icons corpus indexes for these sets (FTS name column, weight 4.0).
"""

import argparse
import base64
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = 'http://www.w3.org/2000/svg'
XLINK_NS = 'http://www.w3.org/1999/xlink'

MODEL_TEMPLATE = (
    '&lt;mxGraphModel&gt;&lt;root&gt;&lt;mxCell id="0"/&gt;'
    '&lt;mxCell id="1" parent="0"/&gt;'
    '&lt;mxCell id="2" value="" style="shape=image;editableCssRules=.*;'
    'verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;'
    'aspect=fixed;image=data:image/svg+xml,{b64};imageBackground=none;" '
    'vertex="1" parent="1"&gt;'
    '&lt;mxGeometry width="{w}" height="{h}" as="geometry"/&gt;'
    '&lt;/mxCell&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;'
)

COLOR_VALUE = re.compile(
    r'^(#[0-9a-fA-F]{3,8}|rgb|rgba|hsl|hsla|currentColor|[a-zA-Z]+)', re.I)
RESIDUAL_COLOR = re.compile(r'(#[0-9a-fA-F]{3,8}\b|rgb\s*\(|hsl\s*\()')
DROP_ATTR_PREFIXES = ('data-', 'aria-')
DROP_ATTRS = ('class', 'xml:space')
DROP_ELEMENTS = ('script', 'foreignObject', 'metadata', 'title', 'desc')


def local(tag):
    return tag.split('}')[-1] if '}' in tag else tag


def parse_svg(path):
    # Some sources carry BOMs, doctypes or comments before <svg>
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    idx = text.find('<svg')
    if idx < 0:
        raise ValueError('no <svg> element')
    return ET.fromstring(text[idx:])


def is_color(value):
    v = value.strip()
    if v in ('none', 'transparent', 'inherit', ''):
        return False
    return bool(COLOR_VALUE.match(v))


def scrub_style_attr(el, drop_props):
    style = el.attrib.get('style')
    if style is None:
        return
    kept = []
    for decl in style.split(';'):
        if ':' not in decl:
            continue
        prop, value = decl.split(':', 1)
        if prop.strip().lower() in drop_props and is_color(value):
            continue
        kept.append(decl.strip())
    if kept:
        el.set('style', ';'.join(kept))
    else:
        del el.attrib['style']


def clean_tree(root, mode, warnings):
    """Sanitize and (for mono modes) strip colours across the whole tree."""
    strip_props = ()
    if mode == 'mono-fill':
        strip_props = ('fill',)
    elif mode == 'mono-stroke':
        strip_props = ('stroke',)

    for el in list(root.iter()):
        name = local(el.tag)
        if name in DROP_ELEMENTS:
            # ET has no parent pointers; mark for removal below instead
            el.tag = '__drop__'
            continue
        for attr in list(el.attrib):
            la = local(attr)
            if la.startswith('on'):
                del el.attrib[attr]
            elif la.startswith(DROP_ATTR_PREFIXES) or la in DROP_ATTRS:
                del el.attrib[attr]
            elif la == 'href' and not el.attrib[attr].startswith('#'):
                raise ValueError('external href: ' + el.attrib[attr])
        if mode != 'color':
            if name == 'style':
                warnings.append('dropped upstream <style> element')
                el.tag = '__drop__'
                continue
            for prop in strip_props:
                value = el.attrib.get(prop)
                if value is not None and is_color(value):
                    del el.attrib[prop]
            scrub_style_attr(el, strip_props)

    def prune(parent):
        for child in list(parent):
            if child.tag == '__drop__':
                parent.remove(child)
            else:
                prune(child)
    prune(root)


def process_svg(path, mode, warnings):
    root = parse_svg(path)
    if local(root.tag) != 'svg':
        raise ValueError('root element is ' + root.tag)

    # Keep only viewBox for geometry; synthesize it when missing
    width = root.attrib.pop('width', None)
    height = root.attrib.pop('height', None)
    if 'viewBox' not in root.attrib:
        if width and height:
            w = re.sub(r'[a-z%]+$', '', width)
            h = re.sub(r'[a-z%]+$', '', height)
            root.set('viewBox', '0 0 %s %s' % (w, h))
        else:
            raise ValueError('no viewBox and no width/height')

    clean_tree(root, mode, warnings)

    if mode != 'color':
        # Residual scan must run before the #000000 rule is injected
        body = ''.join(ET.tostring(c, encoding='unicode') for c in root)
        if RESIDUAL_COLOR.search(body):
            warnings.append('residual colour values (will not fully recolor)')
        class_name = 'shape_fill' if mode == 'mono-fill' else 'shape_outline'
        css_prop = 'fill' if mode == 'mono-fill' else 'stroke'
        children = list(root)
        for child in children:
            root.remove(child)
        style = ET.SubElement(root, '{%s}style' % SVG_NS)
        style.set('type', 'text/css')
        style.text = '.%s{%s:#000000;}' % (class_name, css_prop)
        group = ET.SubElement(root, '{%s}g' % SVG_NS)
        group.set('class', class_name)
        group.extend(children)

    return ET.tostring(root, encoding='unicode')


def default_title(stem, strip_prefix, strip_suffix, capture):
    s = stem
    if capture:
        m = re.match(capture, s)
        if m and m.groups():
            s = m.group(1)
    for p in strip_prefix:
        if s.startswith(p):
            s = s[len(p):]
    for p in strip_suffix:
        if s.endswith(p):
            s = s[:-len(p)]
    words = [w for w in re.split(r'[-_\s]+', s) if w]
    return ' '.join(
        w if (w.isupper() and len(w) > 1) else w[:1].upper() + w[1:]
        for w in words)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode', required=True,
                    choices=['mono-fill', 'mono-stroke', 'color'])
    ap.add_argument('--src', required=True, help='directory of SVG files')
    ap.add_argument('--glob', default='*.svg')
    ap.add_argument('--out', required=True)
    ap.add_argument('--set-title', default=None,
                    help='mxlibrary title attribute (pretty set name for the '
                         'drawio-icons corpus; the editor ignores it)')
    ap.add_argument('--w', type=int, required=True)
    ap.add_argument('--h', type=int, required=True)
    ap.add_argument('--strip-prefix', action='append', default=[])
    ap.add_argument('--strip-suffix', action='append', default=[])
    ap.add_argument('--title-capture', default=None,
                    help='regex; group(1) of a match on the stem becomes the '
                         'title source')
    ap.add_argument('--title-map', default=None,
                    help='JSON file mapping stem -> exact title (overrides)')
    ap.add_argument('--exclude', action='append', default=[],
                    help='regex on the stem; matching files are skipped')
    ap.add_argument('--expect', type=int, default=None)
    ap.add_argument('--report', default=None, help='write stats JSON here')
    args = ap.parse_args()

    ET.register_namespace('', SVG_NS)
    ET.register_namespace('xlink', XLINK_NS)

    title_map = {}
    if args.title_map:
        title_map = json.loads(Path(args.title_map).read_text())

    files = sorted(Path(args.src).glob(args.glob))
    excludes = [re.compile(x) for x in args.exclude]
    entries = []
    all_warnings = {}
    skipped = []

    for f in files:
        stem = f.stem
        if any(x.search(stem) for x in excludes):
            skipped.append(stem)
            continue
        warnings = []
        try:
            svg = process_svg(f, args.mode, warnings)
        except ValueError as e:
            all_warnings[stem] = ['SKIPPED: ' + str(e)]
            skipped.append(stem)
            continue
        if warnings:
            all_warnings[stem] = warnings
        b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
        title = title_map.get(stem) or default_title(
            stem, args.strip_prefix, args.strip_suffix, args.title_capture)
        if args.mode == 'color':
            entries.append({
                'data': 'data:image/svg+xml;base64,' + b64,
                'w': args.w, 'h': args.h,
                'title': title, 'aspect': 'fixed'})
        else:
            entries.append({
                'xml': MODEL_TEMPLATE.format(b64=b64, w=args.w, h=args.h),
                'title': title, 'w': args.w, 'h': args.h,
                'aspect': 'fixed', 'editableCssRules': '.*'})

    entries.sort(key=lambda e: e['title'].lower())

    dupes = {}
    for e in entries:
        dupes[e['title']] = dupes.get(e['title'], 0) + 1
    dupe_titles = sorted(t for t, n in dupes.items() if n > 1)

    attr = ''
    if args.set_title:
        attr = ' title="%s"' % (args.set_title.replace('&', '&amp;')
                                .replace('"', '&quot;').replace('<', '&lt;'))
    payload = '<mxlibrary%s>\n%s\n</mxlibrary>' % (attr, json.dumps(entries))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(payload, encoding='utf-8')

    size = out.stat().st_size
    print('%s: %d entries, %.1f KB (avg %.2f KB/entry)' %
          (out, len(entries), size / 1024.0,
           size / 1024.0 / max(1, len(entries))))
    if skipped:
        print('  skipped %d: %s%s' % (len(skipped), ', '.join(skipped[:8]),
                                      '...' if len(skipped) > 8 else ''))
    if dupe_titles:
        print('  duplicate titles (%d): %s%s' %
              (len(dupe_titles), ', '.join(dupe_titles[:8]),
               '...' if len(dupe_titles) > 8 else ''))
    if all_warnings:
        print('  warnings on %d files:' % len(all_warnings))
        for stem in list(all_warnings)[:10]:
            print('    %s: %s' % (stem, '; '.join(all_warnings[stem])))
        if len(all_warnings) > 10:
            print('    ... %d more' % (len(all_warnings) - 10))
    if args.report:
        Path(args.report).write_text(json.dumps({
            'out': str(out), 'entries': len(entries), 'bytes': size,
            'skipped': skipped, 'duplicateTitles': dupe_titles,
            'warnings': all_warnings}, indent=1))
    if args.expect is not None and len(entries) != args.expect:
        print('  EXPECT MISMATCH: wanted %d, got %d' %
              (args.expect, len(entries)))
        sys.exit(1)


if __name__ == '__main__':
    main()
