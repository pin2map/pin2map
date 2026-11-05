# Original-Screenshots dauerhaft archivieren

**Stand 05.11.2026:** 18 Original-PNGs wurden aus dem Chat exportiert und mit SHA-256 im lokalen Referenzpaket gesichert. **Sie sind noch nicht im GitHub-Repository enthalten.** Die textliche Spezifikation und das Register sind bereits in diesem Branch versioniert.

## Einmaliger Upload (ohne Änderungen an der Anwendung)

1. `pin2map9_routing_github_upload.zip` herunterladen und entpacken.
2. Den Ordner `docs/routing-redesign/screenshots/` mit den **18 unveränderten PNG-Dateien** sowie `docs/routing-redesign/manifest.json` in den bestehenden Dokumentationsbranch `docs/routing-dialog-spec-2026-11` hochladen. **Nicht** nach `main` und nicht nach `qs-setup`.
3. GitHub-Dateiliste gegen `SCREENSHOTS.md` (S01–S18) abgleichen. Bei lokalem Git-Checkout optional SHA-256 mit `sha256sum docs/routing-redesign/screenshots/*.png` und den Werten aus `manifest.json` vergleichen.
4. Erst nach Prüfung die Formulierung „Bilder fehlen noch in GitHub“ aus dem Register entfernen und die Spezifikation als vollständig gesichert kennzeichnen.

## Warum der Zwischenschritt notwendig ist

Die vorhandene GitHub-Anbindung unterstützt hier Textänderungen; der direkte Upload der 18 binären PNGs aus dem lokalen Archiv war in dieser Ausführung nicht möglich. Eine bloße Markdown-Liste oder ein Downloadlink zum Chat ersetzt **keine** dauerhaft gespeicherten Originalbilder in GitHub.

## Nach dem Upload

- Alle Screenshots müssen im Repository selbst erreichbar sein.
- Ein neuer Chat soll die Dokumentation allein über das GitHub-Repository rekonstruieren können.
- Anforderung, Designvorschlag, offene Entscheidung und Testnachweis bleiben getrennt.
- Der Produktionscode wird nicht verändert.
