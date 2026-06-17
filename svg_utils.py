from lxml import etree as ET
import re

SVG_NS = "http://www.w3.org/2000/svg"
NSMAP = {"svg": SVG_NS}


def parse_length(value):
    if value is None:
        return None
    m = re.search(r"[-+]?[0-9]*\.?[0-9]+", str(value))
    return float(m.group(0)) if m else None


def load_svg_root(svg_text):
    parser = ET.XMLParser(remove_blank_text=True)
    root = ET.fromstring(svg_text.encode("utf-8"), parser=parser)
    return root


def tostring_svg(root):
    return ET.tostring(root, encoding="unicode")


def get_svg_size(root):
    vb = root.get("viewBox")
    if vb:
        parts = vb.strip().split()
        if len(parts) == 4:
            return float(parts[2]), float(parts[3]), float(parts[0]), float(parts[1])
    w = parse_length(root.get("width"))
    h = parse_length(root.get("height"))
    if w is not None and h is not None:
        return w, h, 0.0, 0.0
    return 100.0, 100.0, 0.0, 0.0


def find_rect_by_id(root, id_):
    res = root.xpath(f"//svg:rect[@id='{id_}']", namespaces=NSMAP)
    return res[0] if res else None


def get_rect_box(rect):
    x = parse_length(rect.get("x")) or 0.0
    y = parse_length(rect.get("y")) or 0.0
    w = parse_length(rect.get("width")) or 0.0
    h = parse_length(rect.get("height")) or 0.0
    return x, y, w, h


def get_inner_svg_root(svg_text):
    root = load_svg_root(svg_text)
    return root


def insert_svg_into_placeholder(template_root, placeholder_rect, uploaded_svg_text, padding=0):
    dest_x, dest_y, dest_w, dest_h = get_rect_box(placeholder_rect)
    dest_w = float(dest_w) - 2 * padding
    dest_h = float(dest_h) - 2 * padding
    dest_x = float(dest_x) + padding
    dest_y = float(dest_y) + padding

    uploaded_root = get_inner_svg_root(uploaded_svg_text)
    src_w, src_h, src_minx, src_miny = get_svg_size(uploaded_root)

    if src_w == 0 or src_h == 0:
        return

    scale = min(dest_w / src_w, dest_h / src_h)
    new_w = src_w * scale
    new_h = src_h * scale

    tx = dest_x + (dest_w - new_w) / 2.0
    ty = dest_y + (dest_h - new_h) / 2.0

    pre_tx = -src_minx
    pre_ty = -src_miny

    g = ET.Element(f"{{{SVG_NS}}}g")
    g.set("transform", f"translate({tx:.3f},{ty:.3f}) scale({scale:.6f}) translate({pre_tx:.3f},{pre_ty:.3f})")

    for child in list(uploaded_root):
        g.append(child)

    parent = placeholder_rect.getparent()
    idx = parent.index(placeholder_rect)
    parent.insert(idx + 1, g)
