Kurz: Starte die Streamlit-App, lade ein Avatar-SVG (1:1) und ein rechteckiges Logo (5.5:1).

Voraussetzungen
- Python 3.8+
- Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

Starten

```bash
streamlit run app.py
```

Benutzung
- Lege `template.svg` im gleichen Verzeichnis ab (eine Beispielvorlage ist enthalten).
- Lade die beiden SVG-Dateien über die Upload-Felder hoch.
- Wähle optional `Padding`.
- Vorschau wird angezeigt, fertiges SVG kann heruntergeladen werden.

Hinweise
- Platzhalter-IDs: `placeholder-avatar` und `placeholder-rect-logo` müssen in der Vorlage vorhanden sein.
- Logos werden proportional skaliert und zentriert, Verzerrung wird vermieden.
