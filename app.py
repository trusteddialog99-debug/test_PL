from pathlib import Path
import streamlit as st
from svg_utils import (
    load_svg_root,
    find_rect_by_id,
    insert_svg_into_placeholder,
    tostring_svg,
)

TEMPLATE_PATH = Path("template.svg")


def main():
    st.set_page_config(page_title="SVG Template Filler")
    st.title("SVG Template Filler")

    st.markdown("Lade eine statische SVG-Vorlage und setze zwei SVG-Uploads in Platzhalter.")

    if not TEMPLATE_PATH.exists():
        st.error(f"Vorlage {TEMPLATE_PATH} nicht gefunden. Bitte lege template.svg ins Projektverzeichnis.")
        return

    template_src = TEMPLATE_PATH.read_text(encoding="utf-8")
    template_root = load_svg_root(template_src)

    col1, col2 = st.columns(2)
    avatar_file = col1.file_uploader("Avatar-Logo (SVG, 1:1)", type=["svg"]) 
    rect_logo_file = col2.file_uploader("Rechteck-Logo (SVG, 5.5:1)", type=["svg"]) 

    padding = st.slider("Padding in px (optional)", min_value=0, max_value=100, value=4)

    # Work on a copy so the original template remains unchanged in memory
    from copy import deepcopy

    result_root = deepcopy(template_root)

    avatar_msg = "(nicht gesetzt)"
    rect_msg = "(nicht gesetzt)"

    if avatar_file is not None:
        avatar_svg = avatar_file.read().decode("utf-8")
        rect_el = find_rect_by_id(result_root, "placeholder-avatar")
        if rect_el is None:
            st.error("Kein Platzhalter mit ID 'placeholder-avatar' in der Vorlage gefunden.")
        else:
            insert_svg_into_placeholder(result_root, rect_el, avatar_svg, padding=padding)
            avatar_msg = "gesetzt"

    if rect_logo_file is not None:
        rect_svg = rect_logo_file.read().decode("utf-8")
        rect_el = find_rect_by_id(result_root, "placeholder-rect-logo")
        if rect_el is None:
            st.error("Kein Platzhalter mit ID 'placeholder-rect-logo' in der Vorlage gefunden.")
        else:
            insert_svg_into_placeholder(result_root, rect_el, rect_svg, padding=padding)
            rect_msg = "gesetzt"

    st.write(f"Avatar: {avatar_msg} — Rechteck-Logo: {rect_msg}")

    out_svg = tostring_svg(result_root)

    st.subheader("Vorschau")
    # show inline SVG inside HTML so browser renders it
    st.components.v1.html(out_svg, height=600)

    st.subheader("Herunterladen")
    st.download_button("SVG herunterladen", data=out_svg, file_name="result.svg", mime="image/svg+xml")


if __name__ == "__main__":
    main()
